"""Agentes de adaptação disponíveis na plataforma."""

from .base_agent import AdaptationAgent
from .dislexia_agent import DislexiaAgent
from .narrador_agent import NarradorAgent
from .surdez_agent import SurdezAgent
from .tdah_agent import TDAHAgent
from .tea_agent import TEAAgent

#: Registro central: id usado nas rotas -> classe do agente.
AGENTES = {
    "tea": TEAAgent,
    "surdez": SurdezAgent,
    "tdah": TDAHAgent,
    "dislexia": DislexiaAgent,
    "narrador": NarradorAgent,
}

__all__ = [
    "AdaptationAgent",
    "AGENTES",
    "DislexiaAgent",
    "NarradorAgent",
    "SurdezAgent",
    "TDAHAgent",
    "TEAAgent",
]
