# Especificação da interface de serviço da camada de integração

Projeto SAVITS, frente Blockchain/RBB. Documento técnico citado no Relatório final de atividades (seção 3.8).

**Classificação de maturidade: MODELADO** para esta especificação (matriz-de-maturidade.md); o protótipo que a implementa é **PROTOTIPADO e TESTADO** em ambiente local (relatório, seção 3.4).

Versão da interface: v0.1, experimental. Implementação: `poc/backend/gateway.py`. Sessão de demonstração: `poc/integration/demo_session.py`, com registro em `evidence/logs/gateway-session.log`.

O protótipo opera sobre ambiente local compatível com a Máquina Virtual Ethereum (eth-tester), **não sobre a Rede Blockchain Brasil**. Toda resposta inclui o cabeçalho `X-Gateway-Environment: LOCAL-EVM-NAO-E-RBB`, decisão deliberada para que nenhuma saída do protótipo possa ser confundida com registro em rede real. As respostas são JSON (`Content-Type: application/json; charset=utf-8`).

Princípio de projeto (decisão D2): a camada de integração **nunca recebe o arquivo**. Recebe apenas o resumo criptográfico calculado no cliente. Na sessão de demonstração, nenhum arquivo foi transmitido ao serviço em momento algum.

## Autenticação

A autenticação é **simulada por *token* fixo de demonstração**, enviado no cabeçalho `Authorization: Bearer savits-poc-token`. A autenticação por credencial institucional, com cota e registro de auditoria por instituição, é proposta (relatório, seção 3.3) e **não foi implementada**.

Todas as rotas `POST` exigem o *token*, inclusive `POST /v1/verify`, que é operação de leitura; sem ele, a resposta é `401` com `{"erro": "token institucional ausente ou invalido"}`. As rotas `GET` não exigem *token*. Toda transação é assinada pela conta 0 do ambiente de teste; o cliente não manipula chaves, carteiras nem transações.

## Rotas

O protótipo expõe nove rotas.

| Método | Rota | Função | Códigos |
|---|---|---|---|
| GET | `/v1/health` | Estado do serviço, endereços dos contratos, bloco atual | 200 |
| POST | `/v1/assets` | Registra ativo (`id`, `tipo`, `pid` opcional) | 201 / 409 / 401 / 400 |
| GET | `/v1/assets/{id}` | Ativo e histórico completo de versões | 200 / 404 / 400 |
| POST | `/v1/assets/{id}/versions` | Registra versão a partir do `digest` | 201 / 401 / 400 |
| POST | `/v1/verify` | Verifica `digest` contra as versões registradas do ativo | 200 / 401 / 400 |
| POST | `/v1/events` | Registra evento de proveniência com origens | 201 / 401 / 400 |
| POST | `/v1/proofs/batches` | Ancora N resumos em uma transação; devolve recibos | 201 / 401 / 400 |
| GET | `/v1/proofs/{batchId}/inclusion` | Verifica caminho de inclusão em lote | 200 / 400 |
| POST | `/v1/pids` | Cunhagem de identificador persistente no dARK | **501 (não implementado)** / 401 |

Comportamentos comuns, conforme `gateway.py`: rota inexistente devolve `404` com `{"erro": "rota inexistente"}`; exceção durante o processamento (campo ausente, valor inválido ou reversão da transação no contrato) devolve `400` com os campos `erro` e `detalhe`.

### Parâmetros por rota

| Rota | Entrada | Observações de comportamento |
|---|---|---|
| `POST /v1/assets` | `id` (identificador de negócio), `tipo` (`DATASET`, `MODEL`, `PIPELINE`, `RESULT`, `DOCUMENT`, `OTHER`), `pid` opcional | O `assetId` é derivado por `keccak256(id)`. Ativo já existente devolve `409`. O `pid` é gravado como recebido, sem validação de esquema |
| `GET /v1/assets/{id}` | `id` na rota | Devolve `id`, `assetId`, `tipo`, `pid`, `criadoEm` e `versoes`; ativo inexistente devolve `404` |
| `POST /v1/assets/{id}/versions` | `digest`, `algoritmo` (padrão `sha2-256`, truncado a oito bytes), `metadados` (objeto) | Os `metadados` são serializados e reduzidos por `keccak256` ao `metadataHash`; o conteúdo em claro não vai para a cadeia. Conteúdo já registrado no mesmo ativo é rejeitado pelo contrato e devolve `400` |
| `POST /v1/verify` | `id`, `digest` | Devolve `integro`, `versao`, `registradoEm` e `conclusao` |
| `POST /v1/events` | `id`, `versao`, `tipo` (`CREATED`, `INGESTED`, `PROCESSED`, `TRAINED`, `EVALUATED`, `DERIVED`, `PUBLISHED`, `DEPRECATED`, `OTHER`), `detalhe`, `origens` (lista de referências de versão) | O `detalhe` é reduzido por `keccak256` ao `payloadHash` |
| `POST /v1/proofs/batches` | `digests` (lista) | Calcula a raiz da árvore de Merkle, ancora a raiz e a contagem de folhas em uma transação e devolve, para cada folha, o recibo com o caminho de inclusão. Os recibos não são persistidos pelo serviço |
| `GET /v1/proofs/{batchId}/inclusion` | Parâmetros de consulta `leaf` e `proof` (caminho separado por vírgulas) | Devolve `incluido`, `raiz`, `folhas` e `ancoradoEm` |
| `POST /v1/pids` | `id` | Devolve sempre `501` (ver seção própria) |

## Exemplo: verificação de integridade (resposta registrada na sessão)

Requisição (`POST /v1/verify`, chamada 7 da sessão):
```json
{ "id": "savits:dataset:politicas",
  "digest": "0x458ad750328bb5e006375e115d7f5f4da931b46989edd898bcdddf360c64ea08" }
```
Resposta `HTTP 200`:
```json
{ "id": "savits:dataset:politicas",
  "digest": "0x458ad750328bb5e006375e115d7f5f4da931b46989edd898bcdddf360c64ea08",
  "integro": true, "versao": 0, "registradoEm": 1789582924,
  "conclusao": "digest confere com versao registrada" }
```
Após a alteração de um único valor no arquivo (0,510 para 0,910), a mesma rota, com o novo resumo, retornou `"integro": false`, `"versao": null` e `"conclusao": "digest NAO corresponde a nenhuma versao registrada"` (chamada 8). Registrado o conteúdo alterado como nova versão (chamada 9), a verificação do mesmo resumo retornou `"integro": true` e `"versao": 1` (chamada 11).

## Sessão de demonstração

A sessão exercitou dezesseis chamadas sucessivas, precedidas de verificação do estado do serviço (`GET /v1/health`), cobrindo registro de ativos, registro de versões, evento de proveniência, consulta de histórico, verificação de integridade antes e depois da alteração, nova versão, ancoragem em lote de oito resumos, prova de inclusão para folha presente (`incluido: true`) e ausente (`incluido: false`), solicitação de cunhagem (`501`) e chamada sem *token* (`401`). Todas produziram o resultado esperado. Os valores de gás registrados na sessão referem-se ao ambiente local; o registro da versão 0 custou 164.041 unidades de gás.

A certificação não é exposta pela camada de integração; foi exercitada na suíte de testes (T11a), diretamente sobre o contrato. O consentimento também não é exposto por rota.

## Por que `/v1/pids` devolve 501

Não há credenciais de acesso ao dARK (componente de cunhagem Hyperdrive). A rota devolve `501` com os campos `erro`, `motivo` ("sem credenciais de acesso ao dARK/Hyperdrive") e `encaminhamento`, este remetendo à relação de informações necessárias à continuidade (INFORMACOES-NECESSARIAS.md). Devolver `501` com o motivo explícito é preferível a simular a cunhagem: um artifício que respondesse com código de sucesso e um identificador fictício seria, no registro da sessão, indistinguível de integração real, e a regra deste trabalho é que simulação nunca seja apresentada como integração. Nenhum identificador foi cunhado no dARK.

Na sessão, registro, versionamento, proveniência e verificação foram executados com esta rota respondendo `501`, o que constitui evidência empírica, em ambiente local, de que as primitivas exercitadas não dependeram do dARK para funcionar (relatório, seção 3.4).

## Propriedades ainda não implementadas

Autenticação por credencial institucional, custódia de chaves em módulo de segurança, cota por cliente, limitação de taxa, persistência do índice de recibos, validação de esquema estrita com rejeição de campos livres não previstos, idempotência por chave de requisição, versionamento por cabeçalho, paginação, assinatura das respostas e identificador de rastreamento correlacionando requisição e transação. Todas são necessárias antes de qualquer uso real. A trilha de auditoria do protótipo é mantida apenas em memória, durante a execução.

Documentos relacionados: `documento-de-arquitetura.md`, `modelo-de-dados.md`, `modelo-de-ameacas.md`, `analise-de-interoperabilidade.md`, `integracao-dark-rbb.md`.
