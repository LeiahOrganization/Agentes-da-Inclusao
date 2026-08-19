"""Orquestrador: escolhe o agente, adapta a prova e valida o resultado."""

import asyncio

from agents import AGENTES
from config import LLM_MAX_TOKENS, LLM_MODEL, get_client

NIVEIS = {
    "easy": "Simplifique ao máximo e use vocabulário básico.",
    "medium": "Mantenha complexidade moderada.",
    "hard": "Mantenha a complexidade original; adapte apenas o formato.",
}


class ProvaOrchestrator:
    """Coordena os agentes de adaptação e a checagem de fidelidade."""

    def __init__(self):
        # Uma instância por perfil, criadas sob demanda.
        self._instancias: dict = {}

    def get_agent(self, tipo: str):
        if tipo not in AGENTES:
            raise ValueError(
                f"Tipo de adaptação inválido: {tipo}. Use um de: {', '.join(AGENTES)}"
            )
        if tipo not in self._instancias:
            self._instancias[tipo] = AGENTES[tipo]()
        return self._instancias[tipo]

    async def process_prova(
        self,
        content: str,
        adaptation_type: str,
        difficulty_level: str = "medium",
        validar: bool = True,
    ) -> dict:
        agent = self.get_agent(adaptation_type)

        nivel = NIVEIS.get(difficulty_level, NIVEIS["medium"])
        conteudo_com_nivel = f"[NÍVEL SOLICITADO: {nivel}]\n\n{content}"

        adaptado = await agent.adapt(conteudo_com_nivel)

        if validar:
            adaptado = await self._validar(original=content, adaptado=adaptado, agent=agent)

        return {
            "adapted": adaptado,
            "adaptation_type": adaptation_type,
            "difficulty_level": difficulty_level,
            "agent_used": agent.name,
            "metadata": {
                "palavras_original": len(content.split()),
                "palavras_adaptado": len(adaptado.split()),
            },
        }

    async def _validar(self, original: str, adaptado: str, agent) -> str:
        """Segunda passagem: confere se nenhuma questão sumiu ou mudou de gabarito.

        Falha de validação não derruba a requisição — devolvemos a adaptação
        original, que já é melhor do que nenhuma resposta.
        """
        prompt = f"""Compare a prova original com a versão adaptada.

Verifique se a adaptada mantém:
1. Todas as questões do original, na mesma ordem.
2. As respostas corretas inalteradas.
3. O mesmo conteúdo avaliado (só o formato pode mudar).

Se houver problema, devolva a versão corrigida completa.
Se estiver correta, devolva a versão adaptada exatamente como está.
Responda apenas com o texto final da prova, sem comentários.

===ORIGINAL===
{original}

===ADAPTADA===
{adaptado}"""
        try:
            return await asyncio.to_thread(agent.generate, prompt)
        except RuntimeError:
            return adaptado


#: Instância única usada pelas rotas.
orchestrator = ProvaOrchestrator()
