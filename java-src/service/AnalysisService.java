package com.forensia.service;

import com.forensia.dto.request.TextRequest;
import com.forensia.dto.response.AnalysisResult;
import com.forensia.dto.response.ApiResponse;
import com.forensia.model.Analysis;
import com.forensia.repository.AnalysisRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.Map;

@Service
@Slf4j
@RequiredArgsConstructor
public class AnalysisService {

    private final RestTemplate restTemplate;
    private final AnalysisRepository analysisRepository;

    @Qualifier("aiEngineBaseUrl")
    private final String aiEngineBaseUrl;

    public ApiResponse<AnalysisResult> analyzeText(String username, TextRequest request) {
        log.info("Iniciando analise de texto para usuario: {}", username);

        // Chama motor Python
        Map<String, String> body = Map.of("text", request.getText());
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Map<String, String>> entity = new HttpEntity<>(body, headers);

        ResponseEntity<Map> response = restTemplate.postForEntity(
                aiEngineBaseUrl + "/analyze/text",
                entity,
                Map.class
        );

        Map<?, ?> data = response.getBody();
        if (data == null) {
            return ApiResponse.error("Motor de IA retornou resposta vazia");
        }

        double probability = ((Number) data.get("probability")).doubleValue();
        String classification = classify(probability);

        // Persiste resultado
        Analysis analysis = new Analysis();
        analysis.setUsername(username);
        analysis.setProbability(probability);
        analysis.setFile_Type("TEXT");
        analysis.setRole("USER");
        analysisRepository.save(analysis);

        // Monta resposta
        AnalysisResult result = AnalysisResult.builder()
                .Probability(probability)
                .Classification(classification)
                .File_Type("TEXT")
                .Created_at(LocalDateTime.now())
                .Warning(probability >= 0.70 ? "Alta probabilidade de conteudo gerado por IA" : null)
                .build();

        log.info("Analise concluida: probabilidade={}, classificacao={}", probability, classification);
        return ApiResponse.ok(result);
    }

    private String classify(double probability) {
        if (probability < 0.30) return "HUMANO";
        if (probability < 0.70) return "HIBRIDO";
        return "IA_GERADO";
    }
}
