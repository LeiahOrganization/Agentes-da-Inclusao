"""Ponto de entrada da Vercel.

A Vercel executa funções a partir de api/. O app continua definido em
main.py, na raiz, para que rodar local com `uvicorn main:app` siga igual.
"""

import sys
from pathlib import Path

# Torna a raiz do projeto importável dentro da função serverless.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app  # noqa: E402

__all__ = ["app"]
