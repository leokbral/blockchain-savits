# Informações necessárias à continuidade

Projeto SAVITS, frente Blockchain/RBB. Documento técnico citado no Relatório final de atividades (seção 3.8), cuja seção 3.11 resume esta relação.

As informações abaixo não são obtíveis por fonte pública e condicionam decisões de projeto. Os cinco primeiros itens são bloqueantes, por alterarem o desenho da solução. Para cada um registra-se a alternativa experimental adotada na sua ausência, de modo que o trabalho não tenha sido interrompido pela pendência.

| # | Informação necessária | Por que é necessária | Alternativa adotada |
|---|---|---|---|
| 1 | Semântica, esquemas adotados e limite de tamanho do campo de carga associada do dARK; o tipo e a operação de atualização estão documentados (relatório, seção 3.6; ver caracterizacao-do-dark.md). | Determina se o identificador com prova de integridade é convenção semântica ou contrato novo. Comportamento do código publicado testável sem credenciais, em ambiente local; existência e configuração de eventual instância em operação dependentes de informação institucional. | Contrato próprio com campo de resumo de metadados. |
| 2 | Existência de instância de produção do dARK e rede sobre a qual operaria. | Define se o problema é de integração ou de substrato. | Protótipo portável para qualquer rede compatível. |
| 3 | Existência, tipo e cota de nó do Ibict na RBB. | Sem nó registrador não há submissão de transação de aplicação. | Ambiente local compatível. |
| 4 | Parâmetros do modelo de custo da RBB. | Dimensiona a agregação em lote e a política de uso. | Medição comparativa própria de gás. |
| 5 | Competência decisória sobre alterações no núcleo do dARK. | Define se é possível estender o sistema ou se é preciso construir ao lado. | Arquitetura desacoplada, com o dARK como adaptador. |
| 6 | Critérios, rito e prazo de aceitação de caso de uso pela governança da RBB, incluindo a existência de etapa formal de aprovação. | Define se e quando o caso de uso pode utilizar a rede; o prazo não é conhecido e não depende da frente. | Desenvolvimento em ambiente local em paralelo. |
| 7 | Política de custódia de chaves institucionais. | A chave é o ativo crítico do modelo de ameaças. | Conta de teste, explicitamente rotulada. |
| 8 | Volumes anuais de depósito nos sistemas institucionais. | Dimensiona lote, cota e custo. | Medição paramétrica do custo da ancoragem, de 1 a 100.000 objetos declarados, com registro individual extrapolado. |
| 9 | Disponibilidade de manifestos de integridade em acervos preservados. | É a entrada da aplicação de auditoria de acervo. | Mecanismo genérico, agnóstico à origem. |
| 10 | Parecer jurídico sobre a natureza probatória do serviço. | Define como o serviço pode ser apresentado publicamente. | O serviço é descrito como evidência técnica, nunca como ato de fé pública. |
| 11 | Posição do encarregado de dados sobre referência pseudonimizada em cadeia. | Decide se o registro de consentimento pode existir na forma modelada. | Análise documentada e alternativa proposta no relatório, seção 3.5, e em analise-de-conformidade-lgpd.md. |
| 12 | Escopo e granularidade definitivos dos artefatos do SAVITS que receberão identificador. | Define se cada reexecução de treinamento constitui versão. | Modelo genérico de ativo e versão. |
| 13 | Existência de iniciativas equivalentes entre partícipes da RBB. | Evita duplicação de esforço público. | Não se aplica |

Registra-se, como encaminhamento de melhor relação entre esforço e valor informacional, que o item 1 pode ser respondido, quanto ao comportamento do código publicado, por experimento em ambiente local do próprio dARK, sem dependência de credenciais, de acesso à RBB ou de decisão institucional; a existência e a configuração de eventual instância em operação permanecem dependentes de informação institucional (relatório, seção 3.6). Os itens 2 a 5 dependem de consulta interna, e o item 6 de verificação junto à governança da RBB, cujo rito e cujo prazo são externos ao controle da frente.
