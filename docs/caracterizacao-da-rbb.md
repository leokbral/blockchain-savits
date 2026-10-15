# Caracterização da RBB

Projeto SAVITS, frente Blockchain/RBB. Documento técnico citado no Relatório final de atividades (seção 3.8).

Classificação de maturidade: INVESTIGADO (Relatório final de atividades, seção 3.7; matriz-de-maturidade.md). Para o nível seguinte faltariam acesso submissor e dados operacionais da rede.

## Fontes e regra aplicada

A caracterização apoia-se na documentação técnica oficial da Rede Blockchain Brasil: o sítio institucional da rede (REDE BLOCKCHAIN BRASIL, 2026a) e o repositório oficial de arquivos da infraestrutura (REDE BLOCKCHAIN BRASIL, [2026b]). Notícias institucionais e declarações reportadas pela imprensa foram empregadas exclusivamente para confirmação de fatos e de marcos temporais, nunca como base de afirmação técnica.

Regra aplicada: não presumir que a RBB possua determinada capacidade apenas porque redes congêneres a possuem. Para cada capacidade, o quadro distingue o que foi confirmado documentalmente, o que isso permite no contexto do SAVITS e o que permanece a validar.

## Capacidades apuradas

| Capacidade | Situação apurada | Aplicação ao SAVITS | Necessita validação |
|---|---|---|---|
| Natureza da rede | Rede público-permissionada de abrangência nacional: pública na leitura, permissionada no consenso. | Substrato de ancoragem com auditoria pública. | Nenhuma. |
| Plataforma e consenso | Hyperledger Besu com consenso QBFT. | Compatibilidade com a Máquina Virtual Ethereum; sustenta a escolha da pilha tecnológica. | Versão em produção; intervalo de bloco. |
| Permissionamento | Identificação do remetente institucional. | Pode reduzir a necessidade de camada adicional de identificação institucional. | Tratamento de transações submetidas em nome de terceiros; suficiência da identificação para o caso de uso. |
| Topologia | Nós núcleo (conectores e validadores) e nós satélite (registradores e observadores). | Pela topologia documentada, transações são submetidas por nós registradores; nós observadores apenas leem. | Existência de nó do Ibict em operação e, havendo, seu tipo. |
| Participação do Ibict | Partícipe Aderente Associado, com compromisso de operar nós de consenso e direito a voto; a operação efetiva de nó pelo Ibict não está demonstrada nas fontes abertas consultadas. | A categoria prevê a operação de nós de consenso pelo Ibict; a existência de nó do Ibict apto a submeter transações de aplicação para o caso de uso do SAVITS não está demonstrada. | Existência de nó em operação; capacidade e janela operacional para o caso de uso. |
| Governança | Comitê Executivo e Comitê Técnico; entre as competências do primeiro está definir critérios de aceitação de casos de uso. | A utilização pelo SAVITS está sujeita aos critérios de aceitação de casos de uso definidos pela governança. | Rito, critérios aplicáveis e prazo; existência de etapa formal de aprovação para o caso de uso. |
| Auditoria pública | Dados e contratos consultáveis por qualquer cidadão; explorador de blocos público operado por partícipe. | Permite a verificação independente dos registros sem depender de acesso controlado pelo Ibict. | Nenhuma. |
| Modelo econômico | A documentação oficial aponta a aquisição de criptomoedas para remuneração do processamento como barreira das redes públicas e associa o modelo público-permissionado a menor custo. | Indica redução de custo e de barreiras de entrada, e não ausência de custo financeiro. | Parâmetros de custo e de cota aplicáveis ao Ibict. |
| Ferramental | Utilitário de linha de comando, roteiros de adesão e de criação de rede de testes local, monitoramento. | Permite desenvolvimento sem acesso à produção. | Não constitui biblioteca de aplicação. |
| Intermediação de terceiros | Não confirmado nas fontes consultadas. | Determinaria a viabilidade de oferecer o serviço a instituições não partícipes. | Sim; item crítico. |

Fonte: elaboração a partir da documentação técnica oficial da rede (REDE BLOCKCHAIN BRASIL, 2026a, [2026b]).

## Observações complementares

1. Leitura pública. Como a rede é pública na leitura por desenho, a proteção de dados não pode apoiar-se em controle de acesso, mas na decisão de não gravar dado pessoal em cadeia (relatório, seção 3.3; analise-de-privacidade.md e analise-de-conformidade-lgpd.md). O endereço do registrante identifica a instituição, e não a pessoa.
2. Desempenho. Vazão, intervalo de bloco, limite de gás por bloco e latência de finalização do consenso não foram medidos, por ausência de acesso à rede (relatório, seção 3.3; analise-de-escalabilidade.md). A finalização do registro é propriedade esperada da rede, não validada experimentalmente neste trabalho.
3. Gás. Independentemente do custo financeiro, o gás permanece medida pertinente: indica a carga computacional que cada operação impõe a uma infraestrutura compartilhada e pode servir de insumo a eventual política de cota definida pela governança da rede.
4. Iniciativas equivalentes. A existência de contratos ou iniciativas equivalentes entre partícipes da RBB não foi localizada publicamente; sua verificação evitaria duplicação de esforço público (INFORMACOES-NECESSARIAS.md, item 13).

## Conclusão da caracterização

A documentação consultada confirma capacidades centrais compatíveis com a arquitetura proposta: execução de contratos inteligentes em plataforma baseada em Ethereum, permissionamento com identificação da origem das transações, leitura pública dos registros e verificação independente por meio de explorador de blocos público.

Permanecem, contudo, condicionantes a validar, que se distinguem por natureza:

- técnicos: a versão da plataforma em produção e o intervalo de bloco;
- operacionais: a existência de nó do Ibict em operação, prevista pela condição de Partícipe Aderente Associado mas não demonstrada nas fontes abertas consultadas, o tipo desse nó, sua capacidade e janela operacional para o caso de uso e os parâmetros de custo e de cota aplicáveis;
- de governança: o rito, os critérios aplicáveis e o prazo de aceitação de casos de uso, a existência de etapa formal de aprovação e o tratamento de transações submetidas em nome de terceiros.

Encaminhamento de processo: recomenda-se que a aceitação pela governança seja considerada antes das etapas de desenvolvimento que dela dependam, uma vez que seu rito e seu prazo ainda não são conhecidos, e que as etapas independentes prossigam em ambiente local. As informações correspondentes constam do INFORMACOES-NECESSARIAS.md (itens 3, 4 e 6).

Nenhuma transação deste trabalho foi submetida à rede de produção, à rede piloto ou à rede de testes da RBB; os experimentos foram executados em ambiente local compatível com a Máquina Virtual Ethereum (relatório, seção 2.3).

Documentos relacionados: caracterizacao-do-dark.md, integracao-dark-rbb.md, documento-de-arquitetura.md, analise-de-escalabilidade.md.

## Fontes

REDE BLOCKCHAIN BRASIL. Rede Blockchain Brasil: arquitetura, governança e infraestrutura. [S. l.], 2026a. Disponível em: https://redeblockchainbrasil.org/. Acesso em: 22 set. 2026.

REDE BLOCKCHAIN BRASIL. rbb: repositório de arquivos para a infraestrutura da Rede Blockchain Brasil. [S. l.]: GitHub, [2026b]. Disponível em: https://github.com/RBBNet/rbb. Acesso em: 22 set. 2026.
