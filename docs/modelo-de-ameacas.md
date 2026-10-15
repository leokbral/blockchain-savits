# Modelo de ameaças

Projeto SAVITS, frente Blockchain/RBB. Documento técnico citado no Relatório final de atividades (seção 3.8).

**Classificação de maturidade: MODELADO e parcialmente TESTADO** (relatório, seção 3.3; matriz-de-maturidade.md): duas mitigações foram verificadas experimentalmente nos cenários de erro do teste T12. Não houve teste de intrusão nem auditoria de contrato.

Foram identificados seis ativos a proteger e doze ameaças. Os identificadores T-01 a T-12 designam ameaças e não se confundem com os testes T01 a T14 da suíte `tests/run_tests.py`. Todas as observações referem-se ao ambiente local compatível com a Máquina Virtual Ethereum; nenhuma execução ocorreu na RBB.

## 1. Ativos a proteger

| ID | Ativo | Por que importa |
|---|---|---|
| A1 | Chave institucional que assina transações | Quem a detém emite provas falsas em nome do Ibict |
| A2 | Integridade dos registros em cadeia | É o produto |
| A3 | Disponibilidade da camada de integração | A interrupção impede novos registros, mas não invalida provas já emitidas |
| A4 | Confidencialidade dos artefatos | Não trafegam pela camada de integração, por desenho (decisão D2); confirmado na sessão de demonstração |
| A5 | Chave de derivação da referência pseudonimizada do titular | Permitiria reassociar titulares de consentimento; a derivação com chave está prevista no modelo e não foi implementada |
| A6 | Recibos de inclusão em lote | Sem eles, a prova de um objeto ancorado em lote se perde |

## 2. Ameaças e mitigações

Para as oito ameaças de maior impacto, a coluna "Situação" segue a avaliação feita no estudo, sintetizada na seção 3.3 do relatório. Para as demais (T-08, T-09, T-11 e T-12), a situação foi conferida no código.

| ID | Ameaça | Ativo | Impacto | Mitigação | Situação |
|---|---|---|---|---|---|
| T-01 | Conta sem papel tenta registrar ou certificar | A2 | Alto | Controle de acesso por papel no contrato (modificador `only`) | Implementada; testada no registro de ativo e na revogação de certificação (T12); não exercitada na emissão de certificação |
| T-02 | Terceiro revoga certificação alheia | A2 | Médio | Verificação de emissor na função de revogação: `require(c.certifier == msg.sender, ...)` em `revokeCertification` | Implementada; não exercitada pelo teste publicado, pois o cenário do T12 foi barrado pela verificação de papel |
| T-03 | Reenvio de transação (*replay*) | A2 | Baixo | Sequencial de conta (*nonce*) da plataforma; rejeição de conteúdo duplicado por `_hashIndex` | Rejeição de conteúdo duplicado implementada e testada (T12); sequencial de conta, próprio da plataforma, não testado |
| T-04 | Comprometimento da chave institucional | A1 | Crítico | Custódia em módulo de segurança, rotação, segregação de funções, revogação registrada | Não implementada; o protótipo usa conta de teste |
| T-05 | Cliente afirma resumo que não corresponde ao arquivo que alega deter | A2 | Médio | Não mitigável: é limite intrínseco de sistemas de proveniência. O sistema prova que um agente autenticado afirmou um resumo em determinado instante | Reconhecida e declarada (decisão D2; relatório, seção 3.3) |
| T-06 | Abuso da interface para inflar a cadeia | A3, rede | Alto (rede compartilhada) | Cota por cliente, limitação de taxa, agregação em lote | Não implementada |
| T-07 | Gravação acidental de dado pessoal | Conformidade | Crítico e irreversível | Validação de esquema estrita com campos fechados | Parcial: metadados são resumidos antes da gravação |
| T-08 | Camada de integração comprometida emite registros falsos | A1, A2 | Alto | Verificação independente; a camada de integração é conveniência, não autoridade | Parcial: `verifyAsset` e `verifyInclusion` são funções públicas de leitura, chamáveis sem passar pela camada de integração (exercitadas diretamente sobre o contrato nos testes T06, T08 e T13); risco mitigado, não eliminado |
| T-09 | Perda dos recibos de inclusão | A6 | Médio | Recibos autocontidos, armazenados pelo detentor e em índice da camada de integração | Parcial: recibos emitidos na resposta de `POST /v1/proofs/batches`; persistência não implementada |
| T-10 | Descontinuidade da rede (perda de verificabilidade da prova) | A2 | Alto no longo prazo | Recibos autocontidos que permitem reancoragem em outro substrato | Modelada |
| T-11 | Vazamento da chave de derivação da referência do titular | A5 | Alto | Custódia equivalente à de credencial de produção; destruição planejada | Não implementada; a própria derivação com chave não foi implementada (no teste T11b, valor ilustrativo) |
| T-12 | Reentrância ou estouro aritmético nos contratos | A2 | Baixo | Compilador Solidity 0.8.26 verifica estouro aritmético; os contratos não fazem chamadas externas nem movimentam valor | Por construção; sem análise estática nem auditoria |

Observação sobre T-07: além dos metadados, que são resumidos antes da gravação, o campo `pid` do ativo é textual livre e é gravado como recebido pela rota `POST /v1/assets`; a validação de esquema estrita não foi implementada (ver `analise-de-conformidade-lgpd.md`, seção 6).

## 3. Cenários de erro do teste T12

O teste T12 exercitou sete cenários de erro, todos revertidos com mensagem explícita (registro em `evidence/logs/execution.log`):

| Cenário | Mensagem de reversão |
|---|---|
| Conta sem papel tenta registrar ativo | `SAR: sem permissao` |
| Registrar ativo já existente | `SAR: ativo ja registrado` |
| Registrar conteúdo duplicado no mesmo ativo | `SAR: conteudo ja registrado` |
| Evento sobre versão inexistente | `SAR: versao inexistente` |
| Revogar certificação já revogada | `SAR: certificado nao ativo` |
| Terceiro tenta revogar certificação alheia | `SAR: sem permissao` |
| Revogar consentimento já revogado | `SAR: ja revogado` |

O cenário de revogação por terceiro empregou conta sem papel de certificador e certificado já revogado, e foi barrado pela verificação de papel (`SAR: sem permissao`). A verificação de que apenas o emissor revoga a própria certificação (`SAR: apenas o emissor revoga`) está implementada no contrato, mas **não foi exercitada pelo teste publicado**. Para que fosse exercitada, o cenário precisaria empregar uma segunda conta com papel de certificador e um certificado ativo emitido por outra conta (relatório, seções 3.3 e 3.4; matriz-de-maturidade.md: "Teste da verificação de emissor na revogação").

As duas mitigações verificadas experimentalmente são, portanto: a recusa de operação a conta sem papel atribuído (T-01), exercitada no registro de ativo e na revogação de certificação, e a rejeição de registro duplicado do mesmo conteúdo (T-03).

## 4. Avaliação da superfície dos contratos

Registra-se avaliação favorável por construção: os contratos não recebem valor, não realizam chamadas externas e não delegam execução, o que elimina as classes de vulnerabilidade mais frequentes (reentrância, delegação maliciosa por `delegatecall` e manipulação de saldo). A superfície remanescente é de **controle de acesso** e de **validação de entrada**, exercitada nos sete cenários de erro do teste T12, com a ressalva da seção 3 quanto à verificação de emissor.

**O que não foi feito:** auditoria externa, análise estática (por exemplo, Slither ou Mythril), teste de perturbação aleatória (*fuzzing*) e verificação formal. Para uso institucional, ao menos análise estática e auditoria independente deveriam constituir condição de implantação. O nível seguinte de maturidade deste modelo depende de teste de intrusão e de auditoria de contratos (relatório, matriz-de-maturidade.md).

Documentos relacionados: `documento-de-arquitetura.md`, `analise-de-conformidade-lgpd.md`, `analise-de-privacidade.md`, `especificacao-da-interface-de-servico.md`.
