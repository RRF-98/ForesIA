"""
Converte implantacao_shopfacil.md -> PDF
Cores padrao: preto, branco e cinza apenas
"""
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import re

SOURCE = r"R:\Arquivos\Codigos\PROJETO_TCC\Claude_Forencia\implantacao_shopfacil.md"
OUTPUT = r"R:\Arquivos\Trabalho Rubens\implantacao_shopfacil.pdf"

FONTS = {
    ("Arial", ""):   r"C:\Windows\Fonts\arial.ttf",
    ("Arial", "B"):  r"C:\Windows\Fonts\arialbd.ttf",
    ("Arial", "I"):  r"C:\Windows\Fonts\ariali.ttf",
    ("Arial", "BI"): r"C:\Windows\Fonts\arialbi.ttf",
    ("Mono",  ""):   r"C:\Windows\Fonts\cour.ttf",
    ("Mono",  "B"):  r"C:\Windows\Fonts\courbd.ttf",
}

# Paleta: azul claro discreto para titulos e tabelas
COR = {
    "preto":        (0,   0,   0),
    "cinza_escuro": (60,  60,  60),
    "cinza_medio":  (120, 120, 120),
    "cinza_claro":  (200, 200, 200),
    "cinza_bg":     (240, 240, 240),
    "branco":       (255, 255, 255),
    # Azuis discretos
    "azul_h1_bg":   (44,  82,  130),   # azul escuro suave -- fundo H1
    "azul_h1_fg":   (255, 255, 255),   # texto branco sobre H1
    "azul_h2":      (44,  82,  130),   # azul escuro para texto H2
    "azul_h3":      (70,  110, 160),   # azul medio para H3
    "azul_tab_hdr": (44,  82,  130),   # cabecalho tabela
    "azul_tab_fg":  (255, 255, 255),   # texto cabecalho tabela
    "azul_tab_a":   (219, 232, 247),   # linha par tabela (azul bem claro)
    "azul_tab_b":   (255, 255, 255),   # linha impar tabela (branco)
    "azul_borda":   (150, 180, 220),   # borda tabela
}

CHAR_MAP = {
    "✓": "[OK]", "✔": "[OK]",
    "✗": "[X]",  "✘": "[X]",
    "▶": ">>",   "▷": ">>",
    "◆": "*",    "◇": "*",
    "—": "--",   "–": "-",
    "’": "'",    "‘": "'",
    "“": '"',    "”": '"',
    " ": " ",
}


def sanitize(text):
    for ch, rep in CHAR_MAP.items():
        text = text.replace(ch, rep)
    return text


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(20, 22, 20)
        for (fam, style), path in FONTS.items():
            try:
                self.add_font(fam, style, path)
            except Exception:
                pass

    def header(self):
        if self.page_no() <= 1:
            return
        self.set_font("Arial", "I", 8)
        self.set_text_color(*COR["cinza_medio"])
        self.cell(0, 5, "ShopFacil E-Commerce -- Implantacao Omie ERP",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*COR["cinza_claro"])
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.ln(2)

    def footer(self):
        if self.page_no() <= 1:
            return
        self.set_y(-14)
        self.set_font("Arial", "I", 8)
        self.set_text_color(*COR["cinza_medio"])
        self.cell(0, 5, f"Pagina {self.page_no()}", align="C")

    def capa(self):
        self.add_page()
        self.ln(35)

        # Linha superior
        self.set_draw_color(*COR["preto"])
        self.set_line_width(1.2)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.ln(8)

        # Titulo
        self.set_font("Arial", "B", 22)
        self.set_text_color(*COR["preto"])
        self.multi_cell(0, 12, "Projeto de Implantacao de Software ERP",
                        align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(4)

        # Empresa
        self.set_font("Arial", "I", 14)
        self.set_text_color(*COR["cinza_escuro"])
        self.cell(0, 9, "ShopFacil E-Commerce Ltda.",
                  align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.ln(6)

        # Linha inferior do bloco de titulo
        self.set_draw_color(*COR["preto"])
        self.set_line_width(1.2)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.ln(14)

        # Dados do documento
        dados = [
            ("Software Escolhido", "Omie ERP -- SaaS Cloud"),
            ("Orcamento Total",    "R$ 50.000,00"),
            ("Duracao do Projeto", "12 meses implantacao + 12 meses suporte"),
            ("Equipe",             "5 integrantes"),
            ("Emissao",            "Maio de 2026"),
        ]
        for label, valor in dados:
            self.set_font("Arial", "B", 10)
            self.set_text_color(*COR["preto"])
            self.cell(65, 7, label + ":", align="R")
            self.cell(4, 7, "")
            self.set_font("Arial", "", 10)
            self.set_text_color(*COR["cinza_escuro"])
            self.cell(90, 7, valor,
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.ln(30)

        # Rodape da capa
        self.set_draw_color(*COR["cinza_claro"])
        self.set_line_width(0.4)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.ln(4)
        self.set_font("Arial", "I", 9)
        self.set_text_color(*COR["cinza_medio"])
        self.cell(0, 5,
                  "Gestao de Projetos de Tecnologia da Informacao -- 2026",
                  align="C")


def set_text(pdf, cor):
    pdf.set_text_color(*COR[cor])


def render_inline(pdf, text, size=10):
    partes = re.split(r'(\*\*[^*]+\*\*|`[^`]+`)', text)
    for p in partes:
        if p.startswith("**") and p.endswith("**"):
            pdf.set_font("Arial", "B", size)
            pdf.write(5.5, p[2:-2])
            pdf.set_font("Arial", "", size)
        elif p.startswith("`") and p.endswith("`"):
            pdf.set_font("Mono", "", size - 1)
            pdf.write(5.5, p[1:-1])
            pdf.set_font("Arial", "", size)
        else:
            pdf.set_font("Arial", "", size)
            pdf.write(5.5, p)


def parse_table(lines, start):
    rows = []
    i = start
    while i < len(lines):
        ln = lines[i].strip()
        if not ln.startswith("|"):
            break
        if re.match(r'^\|[-|: ]+\|$', ln):
            i += 1
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        rows.append(cells)
        i += 1
    return rows, i


def calc_col_widths(pdf, rows, usable):
    """Larguras proporcionais ao conteudo maximo de cada coluna."""
    ncols = max(len(r) for r in rows)
    max_chars = [0] * ncols
    for row in rows:
        for ci, cell in enumerate(row[:ncols]):
            max_chars[ci] = max(max_chars[ci], len(cell))
    total = sum(max_chars) or 1
    min_w = 12.0
    raw = [max(min_w, usable * (mc / total)) for mc in max_chars]
    scale = usable / sum(raw)
    return [w * scale for w in raw]


def count_lines(pdf, text, width, font, style, size):
    """Conta linhas necessarias para o texto caber na largura dada."""
    pdf.set_font(font, style, size)
    effective = width - 3
    if not text or pdf.get_string_width(text) <= effective:
        return 1
    words = text.split()
    lines, cur = 1, ""
    for word in words:
        test = (cur + " " + word).strip()
        if pdf.get_string_width(test) > effective:
            lines += 1
            cur = word
        else:
            cur = test
    return lines


def draw_table(pdf, rows):
    if not rows:
        return
    ncols   = max(len(r) for r in rows)
    usable  = pdf.w - pdf.l_margin - pdf.r_margin
    col_ws  = calc_col_widths(pdf, rows, usable)
    LINE_H  = 5.0
    PAD     = 1.5

    def row_height(row, is_header):
        font, style, size = "Arial", ("B" if is_header else ""), 8.5
        maxl = 1
        for ci, cell in enumerate(row[:ncols]):
            w = col_ws[ci] if ci < len(col_ws) else col_ws[-1]
            maxl = max(maxl, count_lines(pdf, cell, w, font, style, size))
        return maxl * LINE_H + PAD * 2

    def draw_row(row, is_header, bg_key, fg_key):
        rh     = row_height(row, is_header)
        y0     = pdf.get_y()
        font   = "Arial"
        style  = "B" if is_header else ""
        size   = 8.5
        align  = "C" if is_header else "L"

        # quebra de pagina antes de comecar a linha
        if y0 + rh > pdf.h - pdf.b_margin:
            pdf.add_page()
            y0 = pdf.get_y()

        # fundo + bordas de cada celula (retangulos manuais)
        pdf.set_fill_color(*COR[bg_key])
        pdf.set_draw_color(*COR["azul_borda"])
        pdf.set_line_width(0.3)
        x = pdf.l_margin
        for ci in range(ncols):
            w = col_ws[ci] if ci < len(col_ws) else col_ws[-1]
            pdf.rect(x, y0, w, rh, "FD")
            x += w

        # texto por cima (sem borda, sem fill — retangulo ja fez isso)
        pdf.set_font(font, style, size)
        pdf.set_text_color(*COR[fg_key])
        x = pdf.l_margin
        for ci in range(ncols):
            w  = col_ws[ci] if ci < len(col_ws) else col_ws[-1]
            cell = row[ci] if ci < len(row) else ""
            pdf.set_xy(x + PAD, y0 + PAD)
            pdf.multi_cell(w - PAD * 2, LINE_H, cell,
                           border=0, fill=False, align=align)
            x += w

        pdf.set_xy(pdf.l_margin, y0 + rh)

    def draw_header():
        draw_row(rows[0], is_header=True,
                 bg_key="azul_tab_hdr", fg_key="azul_tab_fg")

    draw_header()

    for ri, row in enumerate(rows[1:], 1):
        bg = "azul_tab_a" if ri % 2 == 0 else "azul_tab_b"
        draw_row(row, is_header=False, bg_key=bg, fg_key="preto")

    pdf.ln(3)
    pdf.set_text_color(*COR["preto"])


def main():
    with open(SOURCE, encoding="utf-8") as f:
        lines = [sanitize(ln.rstrip("\n")) for ln in f]

    pdf = PDF()
    pdf.capa()
    pdf.add_page()

    skip_header = True
    skipped = 0
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Pula bloco de cabecalho do MD (ja desenhado na capa)
        if skip_header and skipped < 10:
            skipped += 1
            i += 1
            continue
        skip_header = False

        # Separador ---
        if stripped == "---":
            pdf.set_draw_color(*COR["cinza_claro"])
            pdf.set_line_width(0.4)
            pdf.line(pdf.l_margin, pdf.get_y(),
                     pdf.w - pdf.r_margin, pdf.get_y())
            pdf.ln(3)
            i += 1
            continue

        # H1 -- nova pagina, fundo azul suave
        if re.match(r'^# ', stripped):
            texto = stripped[2:]
            pdf.add_page()
            y = pdf.get_y()
            pdf.set_fill_color(*COR["azul_h1_bg"])
            pdf.rect(pdf.l_margin - 7, y - 1,
                     pdf.w - pdf.l_margin - pdf.r_margin + 14, 13, "F")
            pdf.set_font("Arial", "B", 14)
            pdf.set_text_color(*COR["azul_h1_fg"])
            pdf.set_x(pdf.l_margin)
            pdf.cell(0, 11, texto,
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(4)
            pdf.set_text_color(*COR["preto"])
            i += 1
            continue

        # H2 -- azul escuro + sublinhado azul
        if re.match(r'^## ', stripped):
            texto = stripped[3:]
            pdf.ln(4)
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(*COR["azul_h2"])
            pdf.cell(0, 8, texto,
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_draw_color(*COR["azul_borda"])
            pdf.set_line_width(0.5)
            pdf.line(pdf.l_margin, pdf.get_y(),
                     pdf.w - pdf.r_margin, pdf.get_y())
            pdf.ln(3)
            pdf.set_text_color(*COR["preto"])
            i += 1
            continue

        # H3 -- azul medio
        if re.match(r'^### ', stripped):
            texto = stripped[4:]
            pdf.ln(2)
            pdf.set_font("Arial", "B", 10.5)
            pdf.set_text_color(*COR["azul_h3"])
            pdf.cell(0, 6.5, texto,
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(*COR["preto"])
            i += 1
            continue

        # H4
        if re.match(r'^#### ', stripped):
            texto = stripped[5:]
            pdf.set_font("Arial", "BI", 10)
            pdf.set_text_color(*COR["cinza_escuro"])
            pdf.set_x(pdf.l_margin + 4)
            pdf.cell(0, 6, texto,
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(*COR["preto"])
            i += 1
            continue

        # Tabela
        if stripped.startswith("|"):
            rows, i = parse_table(lines, i)
            draw_table(pdf, rows)
            continue

        # Bloco de codigo
        if stripped.startswith("```"):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            if code_lines:
                bh = len(code_lines) * 5.5 + 8
                pdf.set_fill_color(*COR["cinza_bg"])
                pdf.rect(pdf.l_margin - 2, pdf.get_y(),
                         pdf.w - pdf.l_margin - pdf.r_margin + 4, bh, "F")
                pdf.set_draw_color(*COR["cinza_claro"])
                pdf.set_line_width(0.3)
                pdf.rect(pdf.l_margin - 2, pdf.get_y() - bh,
                         pdf.w - pdf.l_margin - pdf.r_margin + 4, bh)
                pdf.set_font("Mono", "", 8.5)
                pdf.set_text_color(*COR["cinza_escuro"])
                for cl in code_lines:
                    pdf.set_x(pdf.l_margin + 3)
                    pdf.cell(0, 5.5, cl[:90],
                             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(3)
                pdf.set_text_color(*COR["preto"])
            continue

        # Bullet
        if re.match(r'^[-*] ', stripped):
            texto = stripped[2:]
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(*COR["preto"])
            pdf.set_x(pdf.l_margin + 5)
            pdf.cell(4, 5.5, "-")
            pdf.set_x(pdf.l_margin + 9)
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 9,
                           5.5, texto,
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            i += 1
            continue

        # Lista numerada
        if re.match(r'^\d+\. ', stripped):
            m = re.match(r'^(\d+)\. (.*)', stripped)
            if m:
                num, texto = m.group(1), m.group(2)
                pdf.set_font("Arial", "B", 10)
                pdf.set_text_color(*COR["preto"])
                pdf.set_x(pdf.l_margin + 5)
                pdf.cell(7, 5.5, num + ".")
                pdf.set_font("Arial", "", 10)
                pdf.set_x(pdf.l_margin + 12)
                pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 12,
                               5.5, texto,
                               new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            i += 1
            continue

        # Linha vazia
        if not stripped:
            pdf.ln(2)
            i += 1
            continue

        # Paragrafo normal
        pdf.set_text_color(*COR["preto"])
        pdf.set_x(pdf.l_margin)
        render_inline(pdf, stripped, size=10)
        pdf.ln(5.5)
        i += 1

    pdf.output(OUTPUT)
    print("PDF gerado em: " + OUTPUT)


if __name__ == "__main__":
    main()
