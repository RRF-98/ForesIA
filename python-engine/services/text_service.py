import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TextAnalyzerService:
    """
    Detecta texto gerado por IA.
    Primario: modelo HuggingFace roberta-base-openai-detector
    Fallback: heuristicas estatisticas (sem GPU/modelo necessario)
    """

    def __init__(self):
        self._pipeline = None
        self._model_name = "openai-community/roberta-base-openai-detector"
        self._load_model()

    def _load_model(self):
        try:
            from transformers import pipeline
            self._pipeline = pipeline(
                "text-classification",
                model=self._model_name,
                truncation=True,
                max_length=512
            )
            logger.info("Modelo %s carregado com sucesso", self._model_name)
        except Exception as e:
            logger.warning("Falha ao carregar modelo transformer: %s — usando analise estatistica", e)
            self._pipeline = None

    def analyze(self, text: str) -> dict:
        if self._pipeline is not None:
            return self._analyze_with_model(text)
        return self._analyze_statistical(text)

    def _analyze_with_model(self, text: str) -> dict:
        result = self._pipeline(text)[0]
        label = result["label"]   # "Fake" = IA, "Real" = humano
        score = result["score"]
        probability = score if label == "Fake" else 1.0 - score

        return {
            "probability": round(probability, 4),
            "model_used": self._model_name,
            "method": "transformer",
            "label": label,
            "confidence": score
        }

    def _analyze_statistical(self, text: str) -> dict:
        """
        Heuristicas para deteccao de texto IA sem modelo ML.
        Baseado em: burstiness baixa, TTR alto, transicoes, ausencia de pronomes pessoais.
        """
        words = text.split()
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]

        features = {}

        # Burstiness de sentencas — IA tende a variacoes menores no tamanho
        if len(sentences) > 1:
            lengths = [len(s.split()) for s in sentences]
            mean_len = sum(lengths) / len(lengths)
            variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
            burstiness = variance / (mean_len + 1e-10)
            features["low_burstiness"] = 1.0 if burstiness < 8.0 else 0.0
        else:
            features["low_burstiness"] = 0.5

        # Type-Token Ratio — IA usa vocabulario mais diverso
        if words:
            ttr = len(set(w.lower() for w in words)) / len(words)
            features["high_ttr"] = 1.0 if ttr > 0.65 else 0.0

        # Comprimento medio de sentencas — IA escreve sentencas mais longas e completas
        if sentences:
            avg_len = sum(len(s.split()) for s in sentences) / len(sentences)
            features["long_sentences"] = 1.0 if avg_len > 18 else 0.0

        # Palavras de transicao — IA abusa de conectivos formais
        transitions = [
            "furthermore", "moreover", "additionally", "consequently",
            "nevertheless", "therefore", "importantly", "significantly",
            "notably", "in conclusion", "in summary", "it is worth noting",
            "it should be noted", "as a result", "due to this",
            "alem disso", "portanto", "consequentemente", "no entanto",
            "em conclusao", "dessa forma", "sendo assim"
        ]
        text_lower = text.lower()
        count = sum(1 for t in transitions if t in text_lower)
        features["many_transitions"] = min(1.0, count / 3.0)

        # Ausencia de pronomes pessoais — IA escreve de forma mais impessoal
        personal = ["i ", "me ", " my ", "we ", "our ", "eu ", "meu ", "nossa ", "nosso "]
        personal_found = sum(1 for p in personal if p in text_lower)
        features["no_personal_pronouns"] = 1.0 if personal_found == 0 else max(0.0, 1.0 - personal_found * 0.2)

        weights = {
            "low_burstiness": 0.30,
            "high_ttr": 0.20,
            "long_sentences": 0.15,
            "many_transitions": 0.25,
            "no_personal_pronouns": 0.10,
        }

        probability = sum(features.get(k, 0.0) * w for k, w in weights.items())

        return {
            "probability": round(probability, 4),
            "model_used": "statistical-heuristics",
            "method": "statistical",
            "features": features
        }
