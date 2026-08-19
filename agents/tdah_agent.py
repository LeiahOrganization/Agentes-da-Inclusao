from .base_agent import AdaptationAgent


class TDAHAgent(AdaptationAgent):
    """Agente para estudantes com TDAH."""

    name = "Agente TDAH"
    description = "Divide atividades em etapas menores e reduz elementos de distração"
    icone = "brain-svgrepo-com.svg"
    instructions = (
        "Seu público são estudantes com déficit de atenção e hiperatividade. "
        "O objetivo é reduzir a carga de atenção exigida por questão."
    )
    adaptation_rules = {
        "segmentação": "quebrar enunciados longos em etapas curtas e numeradas",
        "foco": "destacar no início de cada questão o que exatamente se pede",
        "distrações": "remover texto supérfluo e contextos longos desnecessários",
        "ritmo": "agrupar questões em blocos curtos, com marcações de pausa entre eles",
        "organização": "espaçamento generoso entre questões e alternativas",
        "verbos de comando": "iniciar cada instrução com o verbo da ação esperada",
    }
