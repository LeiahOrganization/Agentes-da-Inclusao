from .base_agent import AdaptationAgent


class TEAAgent(AdaptationAgent):
    """Agente para estudantes com Transtorno do Espectro Autista."""

    name = "Agente TEA"
    description = "Adapta linguagem e estrutura para alunos com Transtorno do Espectro Autista"
    icone = "puzzle-piece-svgrepo-com.svg"
    instructions = (
        "Seu público são estudantes autistas. Eles interpretam a linguagem de forma "
        "literal e se beneficiam de estrutura previsível e instruções explícitas."
    )
    adaptation_rules = {
        "linguagem": "clara, direta e literal, sem metáforas ou expressões idiomáticas",
        "estrutura": "sequencial e previsível, com o mesmo formato em todas as questões",
        "instruções": "passo a passo numerado, uma ação por linha",
        "estímulos": "enunciado enxuto, sem elementos decorativos que distraiam",
        "contexto": "tornar explícita qualquer informação social ou implícita",
        "apoio visual": "descrever diagramas e imagens em texto quando existirem",
    }
