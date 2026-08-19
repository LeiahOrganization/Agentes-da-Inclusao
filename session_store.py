"""Armazenamento de sessões em memória.

ATENÇÃO: isto vive no processo. Em deploy serverless (Vercel) cada requisição
pode cair em uma instância diferente e a sessão se perde. Para produção,
troque por Redis ou um banco. Ver docs/PENDENCIAS.md.
"""

import time

#: session_id -> dados da sessão
sessions: dict[str, dict] = {}

#: Sessões mais antigas que isto são descartadas (evita crescer sem limite).
TTL_SEGUNDOS = 60 * 60 * 6


def get_session(session_id: str) -> dict:
    _limpar_expiradas()
    sessao = sessions.get(session_id)
    if sessao is None:
        sessao = {
            "content": None,
            "adapted_content": None,
            "explicacao": None,
            "stage": None,
            "agente": None,
            "criada_em": time.time(),
            "metadata": {},
        }
        sessions[session_id] = sessao
    return sessao


def _limpar_expiradas() -> None:
    limite = time.time() - TTL_SEGUNDOS
    expiradas = [sid for sid, s in sessions.items() if s.get("criada_em", 0) < limite]
    for sid in expiradas:
        sessions.pop(sid, None)
