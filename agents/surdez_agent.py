from .base_agent import AdaptationAgent


class SurdezAgent(AdaptationAgent):
    """Agente para estudantes surdos ou com deficiência auditiva."""

    name = "Agente Surdez"
    description = "Simplifica a estrutura textual para alunos surdos ou com deficiência auditiva"
    icone = "ear-svgrepo-com.svg"
    instructions = (
        "Seu público são estudantes surdos, muitos deles usuários de Libras, para quem "
        "o português escrito é segunda língua. Priorize sintaxe simples e vocabulário concreto."
    )
    adaptation_rules = {
        "sintaxe": "frases curtas na ordem direta (sujeito, verbo, objeto)",
        "vocabulário": "palavras concretas; explicar termos técnicos entre parênteses",
        "voz": "evitar voz passiva e orações subordinadas encadeadas",
        "figuras de linguagem": "substituir expressões idiomáticas por sentido literal",
        "apoio visual": "sugerir onde uma imagem ou esquema ajudaria a compreensão",
        "conteúdo sonoro": "converter qualquer referência a áudio em descrição textual",
    }
