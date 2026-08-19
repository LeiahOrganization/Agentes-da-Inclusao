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


# --------------------------------------------------------------------------
# Regressão: modelos de raciocínio (qwen, gpt-oss) emitem <think>.
# Esse rascunho não pode chegar à prova entregue ao aluno.
# --------------------------------------------------------------------------


def test_remove_bloco_de_raciocinio():
    from agents.base_agent import limpar_raciocinio

    bruto = "<think>Vou simplificar o vocabulário.</think>\nQuestão 1) Quanto é 2 + 2?"
    assert limpar_raciocinio(bruto) == "Questão 1) Quanto é 2 + 2?"


def test_bloco_de_raciocinio_nao_fechado_descarta_tudo():
    """Raciocínio truncado não vira prova: melhor falhar do que entregar rascunho."""
    from agents.base_agent import limpar_raciocinio

    assert limpar_raciocinio("<think>Pensando sem terminar...") == ""


def test_conteudo_antes_do_raciocinio_e_preservado():
    from agents.base_agent import limpar_raciocinio

    bruto = "Questão 1) Quanto é 2 + 2?\n<think>rascunho truncado"
    assert limpar_raciocinio(bruto) == "Questão 1) Quanto é 2 + 2?"


def test_texto_sem_raciocinio_fica_intacto():
    from agents.base_agent import limpar_raciocinio

    assert limpar_raciocinio("Questão 1) Quanto é 2 + 2?") == "Questão 1) Quanto é 2 + 2?"
