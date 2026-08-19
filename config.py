"""Configuração central do projeto.

Mesma convenção do projeto Olhar Acessível: falamos com um endpoint
compatível com a API da OpenAI, o que permite usar Groq, Ollama ou vLLM
apenas trocando LLM_BASE_URL e LLM_MODEL no .env.
"""

import os
from functools import lru_cache

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# --- Modelo de linguagem (endpoint compatível com OpenAI) ---
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen/qwen3.6-27b")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "4000"))
LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT", "120"))

# --- Upload ---
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_MB", "10")) * 1024 * 1024
EXTENSOES_ACEITAS = (".pdf", ".docx", ".txt")

# --- API ---
# Em produção defina CORS_ORIGINS com os domínios reais, separados por vírgula.
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    """Cliente reaproveitado entre chamadas (evita reabrir conexão a cada request)."""
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise RuntimeError(
            "LLM_API_KEY não encontrada. Copie .env.example para .env e preencha a chave. "
            "É a mesma chave da Groq usada no projeto Olhar Acessível."
        )
    return OpenAI(api_key=api_key, base_url=LLM_BASE_URL, timeout=LLM_TIMEOUT)
