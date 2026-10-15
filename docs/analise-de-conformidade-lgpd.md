# Análise de conformidade com a Lei nº 13.709/2018 (LGPD)

Projeto SAVITS, frente Blockchain/RBB. Documento técnico citado no Relatório final de atividades (seção 3.8).

**Classificação de maturidade: MODELADO** (relatório, seção 3.3). O mecanismo de consentimento examinado na seção 4 é **TESTADO, com ressalva jurídica** (relatório, seção 3.5).

Este documento examina implicações da Lei nº 13.709/2018 para a arquitetura proposta e registra as decisões técnicas delas decorrentes. **Não constitui parecer jurídico** nem substitui avaliação do encarregado de dados ou da assessoria jurídica do Ibict. Ao longo do texto distinguem-se três planos: o que constitui **constatação técnica**, o que constitui **interpretação da lei** e o que permanece **dependente de validação jurídica ou institucional**.

## 1. A tensão estrutural

A propriedade que confere valor probatório ao registro distribuído é a dificuldade de alterar ou remover aquilo que foi gravado. Essa mesma propriedade cria tensão com direitos assegurados ao titular pelo art. 18 da lei, entre os quais a correção de dados incompletos, inexatos ou desatualizados e a eliminação de dados tratados com base no consentimento (art. 18, VI).

Gravar dado pessoal diretamente em estrutura concebida para preservar registros estabelece, por conseguinte, incompatibilidade arquitetural relevante entre a finalidade do registro e a capacidade de atender a solicitações de alteração ou eliminação. A extensão dessa incompatibilidade em cada caso concreto depende da interpretação e da aplicação da lei; sua existência no plano técnico, contudo, é suficiente para orientar a decisão de projeto: a arquitetura adotada evita a gravação direta de dados pessoais na cadeia. Toda a modelagem deste projeto decorre dessa decisão.

## 2. Classificação dos dados tratados

A análise foi conduzida campo a campo e dela se extraiu regra única, aplicada uniformemente: dados pessoais, conteúdos, metadados descritivos e demais informações que possam vir a exigir alteração ou eliminação permanecem fora da cadeia; nesta são registrados apenas os elementos estritamente necessários à prova, à referência e à rastreabilidade. O detalhamento por campo do contrato consta de `modelo-de-dados.md` (relatório, seção 3.4).

| Dado | Natureza | Destino | Fundamento |
|---|---|---|---|
| Conteúdo de conjunto de dados de políticas públicas | Pode conter dado pessoal | **Fora da cadeia**, sob custódia do detentor | Minimização (art. 6º, III) |
| Metadados descritivos (autoria, afiliação) | Podem conter dado pessoal | **Fora da cadeia**; em cadeia apenas o `metadataHash` | Minimização |
| Termo de consentimento | Documento com dado pessoal | **Fora da cadeia**; em cadeia apenas o `termsHash` | Necessidade (art. 6º, III) |
| Identificação do titular | Dado pessoal | **Fora da cadeia**; em cadeia apenas a referência pseudonimizada `subjectRef` (derivação com chave prevista, não implementada; ver seção 3) | Pseudonimização (ver seção 3) |
| Resumo criptográfico do artefato | Não identifica pessoa por si só | Em cadeia | Finalidade: prova de integridade |
| Endereço da conta institucional | Identifica **instituição**, não pessoa | Em cadeia | Responsabilização |
| Carimbo de tempo | Não pessoal | Em cadeia | Temporalidade |

## 3. Pseudonimização: ressalvas

### 3.1 Primeira ressalva: alcance da pseudonimização

**Constatação técnica.** O modelo de consentimento prevê que a referência ao titular (`subjectRef`) seja derivada por função criptográfica com chave mantida fora da cadeia; o comentário do contrato `SavitsAssetRegistry.sol` indica HMAC com chave custodiada. **A derivação não foi implementada**: no teste T11b, a referência foi representada por valor ilustrativo (resumo de um texto fixo, em `tests/run_tests.py`). Na forma prevista, o valor registrado não revelaria o titular por si só, mas admitiria reassociação por quem detenha a chave, sendo portanto reversível por construção. Enquanto a chave existir, quem a detenha e disponha de lista de candidatos pode reassociar as referências registradas; o risco migra, assim, para a custódia da chave de vínculo.

**Interpretação da lei.** O art. 13, § 4º da lei caracteriza a pseudonimização como tratamento por meio do qual o dado perde a possibilidade de associação ao indivíduo senão mediante uso de informação adicional mantida separadamente, o que indica que o dado assim tratado não se equipara a dado sem qualquer possibilidade de reassociação.

**Dependente de validação.** Disso pode decorrer a submissão do tratamento a base legal e a registro próprios. Essa consequência depende da interpretação e da aplicação da lei ao caso concreto e requer avaliação do encarregado de dados da instituição.

### 3.2 Segunda ressalva: atendimento a solicitação de eliminação

**Constatação técnica.** O registro gravado na cadeia não é removível pelos meios ordinários da aplicação. No modelo previsto, o elemento que permaneceria sob controle institucional seria a chave de derivação mantida fora da cadeia, derivação que não foi implementada no protótipo.

**Possibilidade arquitetural a examinar.** A destruição dessa chave suprimiria a capacidade de reassociar ao titular a referência registrada, e a eliminação do termo de consentimento ocorreria fora da cadeia, no repositório em que é mantido.

**Dependente de validação.** Não se afirma que tal medida satisfaça, por si só, a solicitação de eliminação de que trata o art. 18, VI da lei. Trata-se de alternativa de projeto cuja suficiência jurídica depende de confirmação prévia da assessoria jurídica e do encarregado de dados, a ser obtida antes de qualquer uso real.

### 3.3 Terceira ressalva: pertinência do registro de consentimento na cadeia

Recomenda-se avaliar se o registro de consentimento precisa efetivamente residir na cadeia, ou se é suficiente ancorar apenas o resumo do termo (`termsHash`), sem a referência ao titular (`subjectRef`), alternativa que atenderia à prova de anterioridade sem registrar elemento passível de reassociação. O modelo implementado mantém `subjectRef` porque a atividade A3 requer rastrear concessão e revogação por titular. A definição constitui questão de arquitetura e de governança de dados e **requer validação institucional**, registrada em INFORMACOES-NECESSARIAS.md (item 11: posição do encarregado de dados sobre referência pseudonimizada em cadeia).

## 4. Revogação como transição de estado

**Classificação: TESTADO, com ressalva jurídica** (teste T11b). Em `SavitsAssetRegistry.sol`, `revokeConsent()` preenche `revokedAt` e emite o evento `ConsentRevoked`; a partir daí, `isConsentActive()` passa a retornar falso. O teste T11b verificou o ciclo: consentimento ativo após o registro e inativo após a revogação, sem que o registro anterior seja apagado. O que foi testado é a máquina de estados; a derivação da referência ao titular com chave não foi implementada (seção 3.1).

A revogação é, portanto, transição de estado, e não eliminação: o registro original permanece, pois a função apenas altera `revokedAt`. As consequências dessa distinção para o direito de eliminação estão examinadas na seção 3.2 e constituem a ressalva mais séria do trabalho (relatório, seção 3.5). Qualquer leitura segundo a qual a permanência, em cadeia, apenas de resumo criptográfico e de referência pseudonimizada, combinada com a eliminação fora da cadeia e a destruição da chave de vínculo, atenderia ao direito de eliminação é interpretação que **depende de confirmação jurídica antes de qualquer uso real**.

## 5. Matriz de princípios

A matriz abaixo registra a leitura técnica de como a arquitetura se relaciona com os princípios do art. 6º. Não constitui juízo de conformidade.

| Princípio (art. 6º) | Como a arquitetura se relaciona | Lacuna |
|---|---|---|
| Finalidade | Escopo registrado como `scopeHash`; o contrato não oferece função de alteração do consentimento registrado | Escopo em claro permanece fora da cadeia |
| Adequação | Registro de prova, não de conteúdo | (sem lacuna registrada) |
| Necessidade | Apenas o indispensável à prova vai para a cadeia | `subjectRef` é o ponto discutível (seção 3) |
| Transparência | Na rede de destino, registro de leitura pública e auditável por qualquer cidadão (propriedade da RBB; não exercitada, pois nenhuma execução ocorreu na RBB) | A leitura pública é também superfície de exposição: ver `analise-de-privacidade.md` |
| Segurança | Controle de acesso por papel implementado; recusa a conta sem papel testada no registro de ativo e na revogação de certificação (T12) | Custódia de chave em módulo de segurança **não implementada**; o protótipo usa conta de teste |
| Prevenção | Esquema do contrato sem campo destinado a dado pessoal em claro; a camada de integração aplica resumo criptográfico aos metadados antes da gravação | Validação de esquema estrita **não implementada**; o campo `pid` é textual livre |
| Responsabilização | Eventos emitidos nas funções de escrita, com remetente identificado | Imutabilidade da trilha é propriedade esperada da rede de destino, não validada no ambiente local |
| Não discriminação | Não aplicável diretamente | (sem lacuna registrada) |

## 6. Risco residual mais grave

**Gravação acidental de dado pessoal por sistema cliente.** Caso um integrador envie, por descuido, dado identificável em campo textual, esse dado passa a integrar o registro, e sua permanência cria risco arquitetural relevante, uma vez que os meios ordinários da aplicação não permitem removê-lo.

O protótipo da camada de integração (`poc/backend/gateway.py`) aplica `keccak256` aos metadados antes da gravação, de modo que o conteúdo em claro dos metadados não alcança a cadeia. A mitigação é, contudo, **parcial**: o campo `pid`, recebido na rota `POST /v1/assets`, é textual livre e é gravado como recebido.

Condição prévia a qualquer uso real: validação de esquema estrita na camada de integração, com rejeição de campos livres não previstos e testes específicos. **Não implementada neste protótipo.**

## 7. Situação e remissões

| Item | Situação | Fonte |
|---|---|---|
| Análise de conformidade | MODELADO; nível seguinte depende de parecer jurídico institucional | Relatório, seção 3.3 e matriz-de-maturidade.md |
| Máquina de estados de consentimento | TESTADO (T11b) | Relatório, seção 3.5 |
| Derivação da referência do titular com chave | Não implementada; valor ilustrativo no teste | Relatório, seções 3.3 e 3.5 |
| Validação de esquema estrita | Não implementada | Relatório, seções 3.3 e 3.11 |
| Execução na RBB | Não ocorreu; ambiente local compatível com a Máquina Virtual Ethereum | Relatório, seções 2.3 e 3.11 |

Documentos relacionados: `modelo-de-dados.md`, `analise-de-privacidade.md`, `modelo-de-ameacas.md`, `documento-de-arquitetura.md`.
