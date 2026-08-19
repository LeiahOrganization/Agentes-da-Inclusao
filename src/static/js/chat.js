const textarea = document.querySelector('.areaInputChat textarea')

const maxHeight = 150

let sessionId = localStorage.getItem("session_id");

if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);
}


textarea.addEventListener("input", () => {
    textarea.style.height = "auto";
    if (textarea.scrollHeight < maxHeight) {
        textarea.style.height = textarea.scrollHeight + "px"
        textarea.style.overflowY = "hidden"
    } else {
        textarea.style.height = maxHeight + "px";
        textarea.style.overflowY = "auto";
    }
})

const barraLateral = document.querySelector('.barraLateral')
const btnBarraLateral = document.querySelector('.btnBarraLateral')
const imgPainel = document.querySelector(".imgPainel")
const mainChat = document.querySelector(".mainChat")
let barraAtivada = false


btnBarraLateral.addEventListener("click", () => {
    if (barraAtivada) {
        barraLateral.classList.remove("aberta")
        barraAtivada = false
        imgPainel.src = "../static/img/pane-open-svgrepo-com.svg"

    } else {
        barraLateral.classList.add("aberta")
        barraAtivada = true
        imgPainel.src = "../static/img/pane-close-svgrepo-com.svg"
    }

})

const btnEnviar = document.querySelector(".btnEnviarMsg")

const chatArea = document.querySelector(".areaConversa")

// A prova adaptada fica no navegador e viaja junto de cada requisicao.
const provaAdaptada = () => localStorage.getItem("prova_adaptada") || "";

// O backend pede texto puro ao modelo, entao renderizamos como texto puro.
// Usar innerHTML aqui abriria espaco para injecao de HTML na resposta.
function bolhaDoAgente(texto) {
    const bolha = document.createElement("div");
    bolha.classList.add("chatMsgConversa");
    const corpo = document.createElement("div");
    corpo.classList.add("markdown");
    corpo.style.whiteSpace = "pre-wrap";
    corpo.textContent = texto;
    bolha.appendChild(corpo);
    return bolha;
}

function botaoPdf() {
    const btn = document.createElement("button");
    btn.textContent = "Baixar PDF";
    btn.classList.add("btnPdf");
    btn.addEventListener("click", async () => {
        const dados = new FormData();
        dados.append("session_id", sessionId);
        dados.append("prova", provaAdaptada());

        btn.disabled = true;
        btn.textContent = "Gerando...";
        try {
            const res = await fetch("/api/adapt/pdf", { method: "POST", body: dados });
            if (!res.ok) throw new Error("falha ao gerar o PDF");
            const url = URL.createObjectURL(await res.blob());
            const link = document.createElement("a");
            link.href = url;
            link.download = "prova_adaptada.pdf";
            link.click();
            URL.revokeObjectURL(url);
        } catch (erro) {
            alert("Nao foi possivel gerar o PDF: " + erro.message);
        } finally {
            btn.disabled = false;
            btn.textContent = "Baixar PDF";
        }
    });
    return btn;
}

window.addEventListener("DOMContentLoaded", async () => {
    const agente = document.body.dataset.agente;

    const formData = new FormData();
    formData.append("agente", agente)
    formData.append("session_id", sessionId)



    const res = await fetch("/api/chat/init", {
        method: "POST",
        body: formData
    });

    const data = await res.json();
    chatArea.appendChild(bolhaDoAgente(data.resposta || "Nao foi possivel iniciar a conversa."));

    const prova = provaAdaptada();
    if (prova) {
        const bolha = bolhaDoAgente("Esta e a prova adaptada:\n\n" + prova);
        bolha.appendChild(botaoPdf());
        chatArea.appendChild(bolha);
        chatArea.scrollTop = chatArea.scrollHeight;
    }
});


btnEnviar.addEventListener("click", async () => {
    const mensagem = textarea.value.trim();
    if (!mensagem) return;

    const usuarioMsgConversa = document.createElement("div")
    usuarioMsgConversa.classList.add("usuarioMsgConversa")
    const paragrafo = document.createElement("p")
    paragrafo.textContent = mensagem
    usuarioMsgConversa.appendChild(paragrafo)


    chatArea.appendChild(usuarioMsgConversa)

    textarea.value = ""


    const formData = new FormData()
    formData.append("mensagem", mensagem)
    formData.append("session_id", sessionId)
    formData.append("prova", provaAdaptada())
    formData.append("agente", document.body.dataset.agente || "")

    btnEnviar.disabled = true
    let data
    try {
        const res = await fetch("/api/chat", { method: "POST", body: formData })
        data = await res.json()
        if (!res.ok) throw new Error(data.detail || "erro " + res.status)
    } catch (erro) {
        chatArea.appendChild(bolhaDoAgente("Erro ao falar com o agente: " + erro.message))
        chatArea.scrollTop = chatArea.scrollHeight
        btnEnviar.disabled = false
        return
    }
    btnEnviar.disabled = false

    const bolha = bolhaDoAgente(data.resposta)

    // Se o agente devolveu a prova reajustada, ela vira a versao corrente.
    if (data.resposta && data.resposta.length > 200 && provaAdaptada()) {
        localStorage.setItem("prova_adaptada", data.resposta)
    }
    if (data.pdf_pronto || provaAdaptada()) {
        bolha.appendChild(botaoPdf())
    }

    chatArea.appendChild(bolha)
    chatArea.scrollTop = chatArea.scrollHeight
})

function atualizarDimensoes() {
    if (window.innerWidth <= 768) {
        mainChat.classList.add('mobile')
    } else {
        mainChat.classList.remove('mobile')
    }
}

atualizarDimensoes()