# Plataforma Agentes de Inclusão

Portal para adaptação automática de avaliações escolares para estudantes com
necessidades educacionais específicas. Projeto PIBIC Jr. 2026/27 — IFCE Maranguape.

O professor envia a prova (PDF, DOCX ou TXT), escolhe o perfil de adaptação e
recebe a versão adaptada em texto e em PDF, podendo pedir ajustes por chat.

## Agentes disponíveis

| id | Agente | O que faz |
|----|--------|-----------|
| `tea` | TEA | Linguagem literal, estrutura previsível, instruções numeradas |
| `tdah` | TDAH | Quebra em etapas curtas, remove distrações, marca pausas |
| `surdez` | Surdez | Sintaxe direta e vocabulário concreto (português como L2) |
| `dislexia` | Dislexia | Blocos curtos, vocabulário frequente, espaçamento |
| `narrador` | Narrador | Prepara para leitura em voz alta, com pausas e descrições |

## Como rodar

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env      # preencha LLM_API_KEY com a chave da Groq
uvicorn main:app --reload
```

Abra <http://localhost:8000>.

## Configuração

O projeto conversa com um endpoint **compatível com a API da OpenAI**, a mesma
convenção do projeto Olhar Acessível. Para trocar de provedor, basta mudar o
`.env` — nenhuma alteração de código:

| Variável | Padrão | Para quê |
|----------|--------|----------|
| `LLM_BASE_URL` | `https://api.groq.com/openai/v1` | Endpoint do provedor |
| `LLM_MODEL` | `qwen/qwen3.6-27b` | Modelo usado |
| `LLM_API_KEY` | — | Chave da Groq (obrigatória) |
| `MAX_UPLOAD_MB` | `10` | Limite de upload |
| `CORS_ORIGINS` | `*` | Domínios liberados |

> A chave **nunca** vai para o Git. Este repositório é público: `.env` está no
> `.gitignore` e deve continuar assim. No deploy, cadastre a chave como
> variável de ambiente.

## Estrutura

```
├── main.py             # rotas FastAPI
├── config.py           # cliente do modelo e variáveis de ambiente
├── orchestrator.py     # escolhe o agente, adapta e valida o resultado
├── session_store.py    # sessões em memória (ver docs/PENDENCIAS.md)
├── agents/             # um arquivo por perfil de adaptação
├── utils/              # extração de texto e geração de PDF
├── src/                # templates Jinja2 e assets estáticos
├── tests/              # pytest (não precisa de chave de API)
└── docs/PENDENCIAS.md  # o que ainda falta
```

## Testes

```bash
pytest
```

## API

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/health` | Checagem de saúde |
| `GET` | `/api/agents` | Lista os agentes |
| `POST` | `/api/chat/init` | Apresenta o agente escolhido |
| `POST` | `/api/adapt/upload` | Envia a prova e recebe a adaptação |
| `POST` | `/api/chat` | Conversa sobre a prova adaptada |
| `GET` | `/api/adapt/pdf` | Baixa a prova adaptada em PDF |

## Como contribuir

Branches: `main` (estável), `dev` (integração), `feature/*` (uma por tarefa).

Commits no padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/):
`feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`.

Pendências abertas em [docs/PENDENCIAS.md](docs/PENDENCIAS.md).
