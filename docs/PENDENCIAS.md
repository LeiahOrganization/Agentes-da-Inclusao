# Pendências conhecidas

Levantadas na auditoria do repositório original (SatiroDev/Agentes-da-Inclusao)
e no que ficou de fora desta reestruturação.

## Segurança

- [ ] **Sessões sem autenticação.** O `session_id` vem do cliente. Quem tiver o
      UUID lê a prova adaptada de outra pessoa em `/api/adapt/pdf`. Provas são
      dado sensível. Assinar o id (JWT ou cookie assinado) ou exigir login.
- [ ] **`CORS_ORIGINS=*`** no exemplo. Definir domínios reais em produção.
- [ ] Revogar as chaves Google que vazaram no histórico do repositório original
      (commits `458669e` e `18d357f`) — elas continuam recuperáveis lá.

## Arquitetura

- [ ] **Sessões em memória** (`session_store.py`). Em deploy serverless na
      Vercel, cada requisição pode cair em uma instância diferente e a sessão
      se perde entre o upload e o chat. Trocar por Redis ou banco.
- [ ] PDF gravado em diretório temporário: sobrevive só enquanto a instância viver.
- [ ] Sem OCR — PDFs digitalizados (imagem) não têm texto extraível.

## Produto

- [ ] O nível de dificuldade (`nivel`) existe na API mas o front ainda não envia.
- [ ] O front não deixa escolher o agente no upload; hoje vai `tea` por padrão.
- [ ] Falta tela de erro amigável quando o modelo falha (hoje devolve 502 cru).
