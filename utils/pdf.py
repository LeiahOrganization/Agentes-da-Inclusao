"""Geração do PDF da prova adaptada."""

import tempfile
import textwrap
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

MARGEM = 2 * cm
ALTURA_LINHA = 15
FONTE = "Helvetica"
TAMANHO_FONTE = 12
COLUNAS = 90


def gerar_pdf_prova(texto: str, session_id: str) -> str:
    """Escreve o PDF em diretório temporário e devolve o caminho."""
    destino = Path(tempfile.gettempdir()) / f"prova_{session_id}.pdf"

    c = canvas.Canvas(str(destino), pagesize=A4)
    largura, altura = A4
    y = altura - MARGEM
    c.setFont(FONTE, TAMANHO_FONTE)

    for linha in texto.split("\n"):
        # Linha em branco no original vira espaço em branco no PDF.
        linhas = textwrap.wrap(linha, width=COLUNAS) or [""]
        for parte in linhas:
            if y < MARGEM:
                c.showPage()
                c.setFont(FONTE, TAMANHO_FONTE)
                y = altura - MARGEM
            c.drawString(MARGEM, y, parte)
            y -= ALTURA_LINHA

    c.save()
    return str(destino)
