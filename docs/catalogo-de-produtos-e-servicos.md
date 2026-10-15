# Catálogo de possibilidades de produtos e serviços

Projeto SAVITS, frente Blockchain/RBB. Documento técnico citado no Relatório final de atividades (seção 3.8).

Classificação de maturidade: PROPOSTO (Relatório final de atividades, seção 3.9; matriz-de-maturidade.md). Para o nível seguinte faltariam priorização institucional e prova de conceito com área demandante.

## Escopo

Este catálogo registra desdobramento derivado das atividades oficiais da frente (Quadro 1 do relatório), e não objeto autônomo do trabalho. Sua inclusão justifica-se porque os mesmos artefatos produzidos para responder às atividades A1 a A3 podem apoiar aplicações institucionais mais amplas, e porque a investigação dessas aplicações foi demandada à frente em reunião da equipe de Blockchain (relatório, seção 2.2).

## Critério discriminante

Aplicou-se a cada possibilidade o critério discriminante enunciado na seção 3.2 do relatório: existe problema de integridade, proveniência, rastreabilidade ou coordenação entre múltiplas entidades que uma infraestrutura distribuída resolva melhor do que uma arquitetura centralizada convencional? O critério é discriminante por construção, e sua aplicação produziu tanto identificações quanto descartes; os descartes, com os respectivos motivos, constam do fim deste documento.

## Possibilidades que satisfazem o critério

O quadro relaciona as possibilidades que, na análise realizada, satisfazem o critério, descreve o problema específico que o mecanismo proposto resolveria e indica quais já dispõem de mecanismo prototipado neste trabalho, circunstância que tende a reduzir o esforço de uma eventual prova de conceito institucional, sem que essa redução tenha sido estimada.

| Possibilidade | Problema que resolveria | Mecanismo já prototipado |
|---|---|---|
| Serviço de prova de integridade | Permitir que terceiros verifiquem a integridade de um acervo sem depender exclusivamente da declaração de quem o custodia. | Sim: ancoragem em lote e verificação. |
| Identificador persistente com prova de integridade | O registro do identificador persistente não inclui prova da integridade do objeto identificado (relatório, seções 1.1 e 3.6). | Parcial: vinculação testada com identificador simulado. |
| Auditoria de integridade de acervo preservado | Permitir que depositantes e terceiros verifiquem a integridade do acervo preservado sem depender apenas dos registros internos do serviço de preservação. | Sim: mecanismo de ancoragem do teste T13, não aplicado a acervo real. |
| Registro de conjuntos de dados e modelos de aprendizado de máquina | A identificação persistente de modelos de aprendizado de máquina não possui prática consolidada (relatório, seção 3.1). | Sim: é o próprio protótipo. |
| Trilha de proveniência científica | Registrar de forma verificável qual versão de dado originou qual modelo e qual resultado. | Sim: eventos com relação de origem. |
| Prova de anterioridade de resultados | Comprovar, de forma verificável por terceiros, a existência de um resultado ou documento em determinada data. | Sim: mesmo mecanismo da prova de integridade. |
| Certificação institucional com revogação | Registrar a emissão e a revogação de atestados institucionais de forma verificável por terceiros. | Sim: testado em T11a. |
| Registro de eventos editoriais e de retratações | Vincular de forma verificável eventos editoriais, inclusive retratações e correções, ao identificador da publicação. | Parcial: modelo de eventos genérico, não exercitado para esse fim. |
| Prova do estado de base agregada em determinada data | Comprovar o conteúdo de uma base agregada em determinada data. | Sim: ancoragem em lote. |
| Camada institucional de integração | Permitir que sistemas institucionais utilizem as primitivas de confiança sem implementar, cada um, a interação com a cadeia. | Sim: protótipo da seção 3.4 do relatório. |

Correspondência com o código do repositório blockchain-savits (FERREIRA, 2026): a ancoragem em lote e a verificação de inclusão correspondem às funções `anchorBatch` e `verifyInclusion` do contrato `ProofAnchor`; a vinculação de identificador persistente, à função `bindPid`; os eventos com relação de origem, à função `registerEvent`; a certificação com revogação, às funções `certify` e `revokeCertification`, todas do contrato `SavitsAssetRegistry`; a camada institucional de integração, ao protótipo em `poc/backend/gateway.py`. Os mecanismos foram exercitados exclusivamente em ambiente local compatível com a Máquina Virtual Ethereum, e não na RBB.

Observações de dependência:

- A possibilidade "Identificador persistente com prova de integridade" depende da hipótese sobre a carga associada do dARK, ainda não testada (caracterizacao-do-dark.md; INFORMACOES-NECESSARIAS.md, item 1).
- A possibilidade "Auditoria de integridade de acervo preservado" tem como entrada manifestos de integridade dos acervos preservados, cuja disponibilidade não é conhecida (INFORMACOES-NECESSARIAS.md, item 9).
- A oferta de qualquer serviço a instituições não partícipes da RBB depende da confirmação de que partícipe pode intermediar transações de terceiros, não confirmada nas fontes consultadas (caracterizacao-da-rbb.md).
- A forma de apresentação pública de serviço de natureza probatória depende de parecer jurídico; o serviço é descrito como evidência técnica, nunca como ato de fé pública (INFORMACOES-NECESSARIAS.md, item 10).

## Possibilidades descartadas

Tão relevante quanto as possibilidades identificadas são as recusadas, cujo registro integra o resultado e contribui para delimitar o esforço institucional (relatório, seção 3.9).

| Possibilidade descartada | Motivo do descarte |
|---|---|
| Emissão de ativos digitais como incentivo à produção científica | Não responde a problema de integridade, proveniência, rastreabilidade ou coordenação identificado no trabalho e envolve questões jurídicas que não foram examinadas. |
| Criação de identificador próprio de pesquisador | Sobrepõe-se a esquemas de identificação de pesquisadores já existentes, com os quais a arquitetura proposta prevê vinculação por mapeamento de identificadores externos (relatório, seção 3.3; analise-de-interoperabilidade.md), e não substituição. |
| Certificação de diplomas | Situa-se fora do escopo de ativos científicos examinado neste trabalho. |
| Armazenamento de objetos em cadeia | Razões de volume e de custo (modelo-de-dados.md) e incompatibilidade arquitetural com requisitos de alteração e eliminação de dados examinada na seção 3.3 do relatório (analise-de-conformidade-lgpd.md). |
| Revisão por pares integralmente em cadeia | Envolve dados pessoais e informações sujeitas a anonimato, cuja confidencialidade não é compatível com registro de leitura pública. |
| Substituição do DOI | Não corresponde ao problema examinado, que é a ausência de prova de integridade no registro do identificador, e não a existência do esquema; e diverge do posicionamento do próprio dARK como implementação de padrão existente (relatório, seção 3.6; caracterizacao-do-dark.md). |

Documentos relacionados: caracterizacao-do-dark.md, caracterizacao-da-rbb.md, integracao-dark-rbb.md, documento-de-arquitetura.md, especificacao-da-interface-de-servico.md.

## Fontes

FERREIRA, L. C. A. blockchain-savits: contratos inteligentes, testes, protótipo de camada de integração e documentos técnicos da frente Blockchain/RBB do Projeto SAVITS. Versão v0.2.0. [S. l.]: GitHub, 2026. Disponível em: https://github.com/leokbral/blockchain-savits/tree/v0.2.0. Acesso em: 15 out. 2026.
