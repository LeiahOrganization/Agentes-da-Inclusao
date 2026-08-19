from .base_agent import AdaptationAgent


class DislexiaAgent(AdaptationAgent):
    """Agente para estudantes com dislexia."""

    name = "Agente Dislexia"
    description = "Reduz a carga de leitura e reorganiza enunciados de forma clara"
    icone = "eye-svgrepo-com.svg"
    instructions = (
        "Seu público são estudantes com dislexia. A decodificação da leitura já "
        "consome esforço, então o texto precisa ser curto, previsível e bem espaçado."
    )
    adaptation_rules = {
        "vocabulário": "palavras frequentes e curtas sempre que possível",
        "blocos de texto": "no máximo três linhas por parágrafo",
        "enunciado": "uma pergunta por vez, sem perguntas encadeadas",
        "alternativas": "cada alternativa em sua própria linha, com rótulos claros",
        "palavras longas": "separar em sílabas entre parênteses quando essenciais",
        "espaçamento": "linha em branco entre enunciado e alternativas",
    }
