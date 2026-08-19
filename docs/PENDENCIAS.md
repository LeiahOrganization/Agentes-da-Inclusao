# Pendências conhecidas

Levantadas na auditoria do repositório original (SatiroDev/Agentes-da-Inclusao)
e no que ficou de fora desta reestruturação.

## Segurança

- [ ] **Sem autenticação.** Qualquer pessoa com o endereço usa a plataforma e
      gasta a cota da chave. Para uso real com professores, exigir login.
- [ ] A rota legada `GET /api/adapt/pdf?session_id=` ainda lê da sessão pelo id
      não assinado. Só vale no uso local; remover ou assinar o id.
- [ ] **`CORS_ORIGINS=*`** no exemplo. Definir domínios reais em produção.
- [ ] Revogar as chaves Google que vazaram no histórico do repositório original
      (commits `458669e` e `18d357f`) — elas continuam recuperáveis lá.

## Arquitetura

- [x] ~~Sessões em memória quebravam o fluxo em serverless.~~ Resolvido: a prova
      adaptada fica no navegador e viaja em cada requisição. O `session_store`
      virou conveniência local; a API funciona sem ele.
- [x] ~~PDF dependia da sessão.~~ Agora `POST /api/adapt/pdf` gera a partir do
      texto enviado pelo cliente.
- [ ] **Respostas demoram.** No teste real, um ajuste no chat levou 33s. O limite
      da Vercel no plano gratuito é 60s. Implementar streaming (SSE) resolveria a
      percepção de lentidão e o risco de timeout.
- [ ] A prova fica no `localStorage`: some se o professor trocar de navegador.
- [ ] Sem OCR — PDFs digitalizados (imagem) não têm texto extraível.

## Produto

- [ ] O chat reenvia a prova inteira a cada mensagem. Funciona, mas gasta tokens;
      um identificador com a prova em cache no servidor seria mais econômico.

- [ ] O nível de dificuldade (`nivel`) existe na API mas o front ainda não envia.
- [ ] O front não deixa escolher o agente no upload; hoje vai `tea` por padrão.
- [ ] Falta tela de erro amigável quando o modelo falha (hoje devolve 502 cru).
