"""API da Plataforma Agentes de Inclusão."""

import asyncio
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from agents import AGENTES
from config import CORS_ORIGINS
from orchestrator import orchestrator
from session_store import get_session
from utils.file_processor import ArquivoInvalido, extract_content
from utils.pdf import gerar_pdf_prova

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="API de Adaptação de Provas", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "src" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "src" / "templates"))


def listar_agentes() -> list[dict]:
    """Catálogo dos agentes, montado a partir das próprias classes."""
    return [
        {
            "id": agente_id,
            "name": classe.name,
            "description": classe.description,
            "url": classe.icone,
        }
        for agente_id, classe in AGENTES.items()
    ]


# --------------------------------------------------------------------------
# Páginas
# --------------------------------------------------------------------------


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "agentes": listar_agentes()}
    )


@app.get("/upload", name="upload")
async def upload_page(request: Request, agente: str | None = None):
    return templates.TemplateResponse("upload.html", {"request": request, "agente": agente})


@app.get("/chat", name="chat")
async def chat_page(request: Request, agente: str | None = None):
    return templates.TemplateResponse("chat.html", {"request": request, "agente": agente})


# --------------------------------------------------------------------------
# API
# --------------------------------------------------------------------------


@app.get("/api/health")
async def health():
    """Checagem rápida usada no deploy."""
    return {"status": "ok", "agentes": list(AGENTES)}


@app.get("/api/agents")
async def list_agents():
    return {"agents": listar_agentes()}


@app.post("/api/chat/init")
async def chat_init(agente: str = Form(...), session_id: str = Form(...)):
    """Abre a conversa apresentando o agente escolhido."""
    if agente not in AGENTES:
        raise HTTPException(status_code=400, detail=f"Agente desconhecido: {agente}")

    sessao = get_session(session_id)
    sessao["agente"] = agente
    sessao["stage"] = "init"

    instancia = orchestrator.get_agent(agente)
    regras = ", ".join(instancia.adaptation_rules)
    prompt = (
        f"Apresente-se em no máximo três frases como {instancia.name}. "
        f"Explique que você adapta provas ajustando: {regras}. "
        "Termine perguntando se o professor deseja alguma adaptação específica."
    )

    try:
        resposta = await asyncio.to_thread(instancia.generate, prompt)
    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro

    return {"resposta": resposta}


@app.post("/api/adapt/upload")
async def upload_prova(
    session_id: str = Form(...),
    file: UploadFile = File(...),
    agente: str = Form("tea"),
    nivel: str = Form("medium"),
):
    """Recebe a prova, adapta com o agente escolhido e prepara o PDF."""
    if agente not in AGENTES:
        raise HTTPException(status_code=400, detail=f"Agente desconhecido: {agente}")

    sessao = get_session(session_id)

    try:
        conteudo = await extract_content(file)
    except ArquivoInvalido as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro

    sessao["content"] = conteudo
    sessao["agente"] = agente

    try:
        resultado = await orchestrator.process_prova(
            content=conteudo, adaptation_type=agente, difficulty_level=nivel
        )
    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro

    sessao["adapted_content"] = resultado["adapted"]
    sessao["metadata"] = resultado["metadata"]
    sessao["stage"] = "chatting"

    return {
        "message": "Prova adaptada com sucesso.",
        "adapted": resultado["adapted"],
        "agent_used": resultado["agent_used"],
        "metadata": resultado["metadata"],
        "pdf_url": f"/api/adapt/pdf?session_id={session_id}",
    }


@app.post("/api/chat")
async def chat_api(session_id: str = Form(...), mensagem: str = Form(...)):
    """Conversa sobre a prova já adaptada."""
    sessao = get_session(session_id)
    conteudo = sessao.get("adapted_content") or sessao.get("content")

    if not conteudo:
        return {"resposta": "Envie uma prova primeiro para que eu possa adaptá-la."}

    texto = mensagem.lower()
    if any(palavra in texto for palavra in ("pdf", "baixar", "download")):
        if not sessao.get("adapted_content"):
            return {"resposta": "Ainda não há uma prova adaptada nesta sessão."}
        return {
            "resposta": "Sua prova adaptada está pronta para download.",
            "pdf_url": f"/api/adapt/pdf?session_id={session_id}",
        }

    agente = sessao.get("agente") or "tea"
    instancia = orchestrator.get_agent(agente)
    prompt = (
        "Responda à pergunta do professor sobre a prova adaptada abaixo. "
        "Se ele pedir um ajuste, devolva a prova inteira já ajustada.\n\n"
        f"===PROVA===\n{conteudo}\n\n===PERGUNTA===\n{mensagem}"
    )

    try:
        resposta = await asyncio.to_thread(instancia.generate, prompt)
    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro

    return {"resposta": resposta}


@app.get("/api/adapt/pdf")
async def baixar_pdf(session_id: str):
    sessao = get_session(session_id)
    adaptada = sessao.get("adapted_content")
    if not adaptada:
        raise HTTPException(status_code=404, detail="Prova adaptada não encontrada nesta sessão.")

    caminho = gerar_pdf_prova(adaptada, session_id)
    return FileResponse(caminho, media_type="application/pdf", filename="prova_adaptada.pdf")
