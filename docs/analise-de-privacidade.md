# Análise de privacidade

Projeto SAVITS, frente Blockchain/RBB. Documento técnico citado no Relatório final de atividades (seção 3.8).

**Classificação de maturidade: MODELADO** (relatório, seção 3.3). A decisão de não gravar em cadeia dado pessoal, conteúdo de artefato, metadado descritivo ou localização está refletida na estrutura do contrato prototipado (`SavitsAssetRegistry`); a mitigação por sal na derivação do identificador interno do ativo e a derivação com chave da referência ao titular de consentimento não foram implementadas. Não houve auditoria de privacidade nem parecer jurídico.

## 1. Superfície de exposição

A RBB é **pública na leitura** por desenho: qualquer cidadão pode obter, consultar e auditar os dados e contratos nela gravados, e existe explorador de blocos público operado por partícipe da rede (relatório, seções 3.3 e 3.7; `caracterizacao-da-rbb.md`). Portanto, a análise de privacidade não pode apoiar-se em controle de acesso; deve apoiar-se na decisão de **não gravar**.

## 2. O que um observador externo consegue ver

O estudo identificou quatro superfícies principais: o resumo do conteúdo, o endereço do registrante, os carimbos de tempo e o identificador interno do ativo. As demais linhas do quadro decorrem da estrutura do contrato prototipado.

| Observável | Risco | Tratamento adotado |
|---|---|---|
| `contentHash` de um artefato | Baixo, mas permite **confirmação**: quem já possui um arquivo pode provar que ele foi registrado | Aceito; corresponde à função do sistema |
| `assetId` (`keccak256` de identificador de negócio) | **Ataque de dicionário**: identificadores previsíveis podem ser adivinhados e confirmados | Mitigação possível: sal institucional na derivação. **Não implementada**; ver seção 3 |
| `pid` (ARK) em texto | Nenhum quanto ao conteúdo: é público por definição. Por ser o único campo textual do modelo, é o canal pelo qual um integrador poderia gravar, por descuido, dado identificável | Aceito. Validação de esquema estrita, com rejeição de campos livres não previstos, não implementada; mitigação apenas parcial (relatório, seção 3.3) |
| Endereço do registrante | Identifica a instituição, não a pessoa | Aceito e desejável (responsabilização) |
| Carimbos de tempo | Revelam ritmo e volume de atividade | Aceito; risco de análise de tráfego documentado na seção 4 |
| `subjectRef` de consentimento | Referência pseudonimizada. O modelo prevê derivação com chave mantida fora da cadeia, que admitiria reassociação ao titular por quem detenha a chave | Derivação não implementada; no teste, valor ilustrativo. Ver `analise-de-conformidade-lgpd.md` |
| Padrão de eventos de proveniência | Revela a topologia do fluxo de processamento (quantos modelos, quantas versões) | Aceito; pode ser sensível em contexto de avaliação de política |

## 3. Fragilidade identificada e não corrigida

O `assetId` é derivado por `keccak256` de um identificador de negócio legível e previsível (na sessão de demonstração, `"savits:dataset:politicas"`; função `aid` em `poc/backend/gateway.py`). Como o espaço de identificadores é previsível, um observador pode testar hipóteses e confirmar a existência de determinado ativo.

**Mitigação recomendada e não implementada:** derivar `assetId` com sal institucional mantido fora da cadeia. Contrapartida: perde-se a conveniência de recalcular o `assetId` a partir do identificador de negócio sem consultar o serviço. Trata-se de compromisso entre conveniência e proteção contra inferência que depende de decisão da coordenação (relatório, seções 3.3 e 3.11).

## 4. Análise de tráfego

Mesmo sem conteúdo, a cadeia revela *quando* e *quanto* cada instituição registra. Em contexto de avaliação de políticas públicas isso pode ter sensibilidade própria (por exemplo, hipoteticamente: revelar que um município passou a ser objeto de análise antes de o estudo ser publicado). A agregação em lote reduz esse sinal, porque N objetos passam a produzir uma única transação: efeito colateral favorável da decisão D3 (`documento-de-arquitetura.md`), tomada por outra razão (custo).
