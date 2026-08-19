"""Testes que não dependem de rede nem de chave de API."""

import pytest

from agents import AGENTES


@pytest.mark.parametrize("agente_id", list(AGENTES))
def test_agente_tem_metadados(agente_id):
    """Todo agente precisa de nome, descrição, ícone e regras."""
    classe = AGENTES[agente_id]
    assert classe.name
    assert classe.description
    assert classe.icone.endswith(".svg")
    assert classe.adaptation_rules


@pytest.mark.parametrize("agente_id", list(AGENTES))
def test_prompt_de_sistema_inclui_regras(agente_id, monkeypatch):
    """O prompt de sistema deve carregar as regras do perfil."""
    classe = AGENTES[agente_id]
    monkeypatch.setattr(classe, "__init__", lambda self, model=None: None)
    agente = classe()
    agente.instructions = classe.instructions
    agente.adaptation_rules = classe.adaptation_rules

    prompt = agente._system_prompt()
    for chave in classe.adaptation_rules:
        assert chave in prompt
    assert "Não use Markdown" in prompt


def test_orquestrador_rejeita_agente_invalido():
    from orchestrator import ProvaOrchestrator

    with pytest.raises(ValueError, match="inválido"):
        ProvaOrchestrator().get_agent("inexistente")
