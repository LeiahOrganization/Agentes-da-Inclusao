from .base_agent import AdaptationAgent


class NarradorAgent(AdaptationAgent):
    """Agente que prepara a prova para leitura em voz alta."""

    name = "Agente Narrador"
    description = "Prepara o conteúdo para narração e leitura em voz alta"
    icone = "sound-loud-svgrepo-com.svg"
    instructions = (
        "Seu público são estudantes que farão a prova ouvindo, por leitor humano "
        "ou sintetizador de voz. O texto precisa fazer sentido sem apoio visual."
    )
    adaptation_rules = {
        "pausas": "inserir [PAUSA] entre questões e antes das alternativas",
        "navegação": "anunciar posição, como 'Questão 3 de 10'",
        "elementos visuais": "descrever tabelas, gráficos e imagens por extenso",
        "siglas": "soletrar siglas na primeira ocorrência",
        "pontuação": "usar pontuação que produza ritmo natural na leitura",
        "símbolos": "escrever símbolos matemáticos por extenso, como 'maior que'",
    }
