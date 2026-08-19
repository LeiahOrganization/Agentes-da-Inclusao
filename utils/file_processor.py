"""Extração de texto dos arquivos enviados (PDF, DOCX, TXT)."""

import io
from pathlib import Path

import PyPDF2
from docx import Document

from config import EXTENSOES_ACEITAS, MAX_UPLOAD_BYTES


class ArquivoInvalido(ValueError):
    """Arquivo rejeitado por formato, tamanho ou conteúdo ilegível."""


async def extract_content(file) -> str:
    """Lê o upload e devolve o texto. Valida extensão e tamanho no servidor."""
    extensao = Path(file.filename or "").suffix.lower()
    if extensao not in EXTENSOES_ACEITAS:
        raise ArquivoInvalido(
            f"Formato não suportado: {extensao or 'sem extensão'}. "
            f"Aceitos: {', '.join(EXTENSOES_ACEITAS)}"
        )

    conteudo = await file.read()
    if not conteudo:
        raise ArquivoInvalido("Arquivo vazio.")
    if len(conteudo) > MAX_UPLOAD_BYTES:
        limite_mb = MAX_UPLOAD_BYTES // (1024 * 1024)
        raise ArquivoInvalido(f"Arquivo maior que o limite de {limite_mb} MB.")

    if extensao == ".pdf":
        texto = _extrair_pdf(conteudo)
    elif extensao == ".docx":
        texto = _extrair_docx(conteudo)
    else:
        texto = conteudo.decode("utf-8", errors="replace")

    if not texto.strip():
        raise ArquivoInvalido(
            "Não foi possível extrair texto do arquivo. "
            "Se for um PDF digitalizado, será preciso OCR."
        )
    return texto


def _extrair_pdf(conteudo: bytes) -> str:
    try:
        leitor = PyPDF2.PdfReader(io.BytesIO(conteudo))
        partes = [pagina.extract_text() or "" for pagina in leitor.pages]
    except Exception as erro:
        raise ArquivoInvalido(f"PDF ilegível: {erro}") from erro
    return "\n".join(partes)


def _extrair_docx(conteudo: bytes) -> str:
    try:
        documento = Document(io.BytesIO(conteudo))
    except Exception as erro:
        raise ArquivoInvalido(f"DOCX ilegível: {erro}") from erro
    return "\n".join(paragrafo.text for paragrafo in documento.paragraphs)
