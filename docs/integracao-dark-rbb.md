# Integração entre o dARK e a RBB

Projeto SAVITS, frente Blockchain/RBB. Documento técnico citado no Relatório final de atividades (seção 3.8).

Classificação de maturidade: INVESTIGADO; causa não determinada (Relatório final de atividades, seção 3.7). Nenhuma das hipóteses de causa foi testada.

## Questão examinada

Foi formulada à frente a questão de por que o dARK não pode ser utilizado diretamente no contexto pretendido. Regra aplicada: não afirmar causa sem evidência. O resultado é que a causa permanece não determinada, embora as hipóteses estejam delimitadas e sejam testáveis.

## Evidências disponíveis

1. O dARK é aplicação sobre nós institucionais de *blockchain*, com implementação de referência em Hyperledger Besu (dARK-PID, [2025a]).
2. A RBB é rede Besu com consenso QBFT (REDE BLOCKCHAIN BRASIL, 2026a).

Essas evidências estabelecem compatibilidade de plataforma, mas não indicam se há instância de produção do dARK nem a rede sobre a qual ela operaria, informações não localizadas nas fontes consultadas (caracterizacao-do-dark.md).

## Hipótese sobre o substrato

Formula-se a hipótese, ainda não confirmada, de que eventual instância de produção do dARK opere sobre outra rede, própria ou de consórcio, e não sobre a RBB. Essa hipótese foi originalmente motivada por declaração institucional segundo a qual a adesão à RBB poderia ser benéfica para a manutenção e o desenvolvimento da rede dARK; a fonte primária dessa declaração não foi localizada nem confirmada, razão pela qual ela não é tomada como evidência. A confirmação da hipótese depende da informação registrada no INFORMACOES-NECESSARIAS.md, item 2.

Caso a hipótese se confirme, o problema não se reduz a uma questão de interface: envolve também o substrato, e a questão muda de forma. Além de definir como integrar o dARK aos sistemas institucionais, coloca-se a decisão entre três estratégias:

- migrar a aplicação para a RBB;
- mantê-la em coexistência nas duas redes;
- preservá-la onde está, com uma ponte entre redes.

As três têm implicações distintas, e a escolha entre elas envolve dimensões técnicas, operacionais e de governança.

## Hipóteses de causa

As hipóteses não são mutuamente exclusivas, e cada uma implicaria solução diferente (seção 3.7 do relatório).

| Hipótese de causa | Solução que implicaria | Como testar |
|---|---|---|
| Substrato: dARK e RBB são redes distintas. | Decisão estratégica de migração, coexistência ou ponte; uma camada de encapsulamento, isoladamente, não a resolve. | Consulta à equipe do dARK (INFORMACOES-NECESSARIAS.md, item 2). |
| Modelo de dados centrado em publicação, com localização obrigatória, não acomoda eventos nem objetos sem localização pública. | Serviço de prova separado, com o dARK empregado apenas onde cabe identificador. | Ensaio da operação de carga associada em ambiente local. |
| Ergonomia: ausência de biblioteca nas linguagens dos sistemas institucionais. | Fachada de serviço web; hipótese endereçada pela camada de integração. | Integração de um sistema real e medição do atrito. |
| Autenticação: exigência de carteira e custódia de chave por sistema cliente. | Custódia centralizada com credencial institucional. | Exame do fluxo de credenciais da interface de cunhagem (Hyperdrive). |
| Governança: o uso da RBB para novo caso de uso está sujeito a critérios de aceitação definidos pela governança. | Atendimento aos critérios e ao rito aplicáveis; nenhuma solução técnica os supre. | Critérios confirmados na documentação; rito, prazo e eventual etapa formal de aprovação a verificar (caracterizacao-da-rbb.md). |
| Custo e cotas desconhecidos. | Dimensionamento da agregação em lote conforme a cota. | Consulta ao Comitê Técnico (INFORMACOES-NECESSARIAS.md, item 4). |
| Organizacional: co-governança do dARK com instituição parceira condiciona alterações no núcleo. | Construir ao lado, e não dentro. | Consulta à coordenação (INFORMACOES-NECESSARIAS.md, item 5). |

A hipótese de que a carga associada do dARK comporte um manifesto de integridade, e a alternativa de contrato próprio caso não comporte, são tratadas em caracterizacao-do-dark.md (INFORMACOES-NECESSARIAS.md, item 1).

Leitura com a informação disponível: nenhuma das hipóteses foi testada. A análise concentrou-se nas hipóteses de substrato, ergonomia e governança, por serem diretamente relacionadas à dificuldade de uso do dARK no contexto pretendido. Dessas três, apenas a de ergonomia é resolvida por uma camada de abstração; as de substrato e de governança dependem de decisões e de informações que uma camada técnica, isoladamente, não supre.

## Avaliação crítica da hipótese de encapsulamento

Classificação: INVESTIGADO. A hipótese discutida pela equipe consiste em criar camada de encapsulamento sobre o dARK, posicionando-o como núcleo do serviço, com a RBB como ramo paralelo:

```
Sistemas do Ibict → Camada de encapsulamento → { dARK , RBB } → Blockchain
```

A avaliação identificou um acerto e duas objeções.

O acerto: existe lacuna de camada de abstração. Integrar um sistema institucional ao dARK exige hoje conhecer sua interface de cunhagem, seu modelo de dados e a gestão de credenciais. Uma fachada institucional com interface estável, autenticação por credencial e semântica de domínio tende a reduzir o custo de adoção interna. O protótipo da camada de integração (relatório, seção 3.4; especificacao-da-interface-de-servico.md) demonstrou, em ambiente local, a viabilidade técnica dessa fachada, com autenticação simulada por *token* fixo: um cliente de demonstração exerceu registro, versionamento, proveniência, verificação e ancoragem em lote sem manipular chaves, carteiras ou transações. A redução efetiva do custo de adoção não foi medida; sua aferição depende da integração de um sistema real.

Primeira objeção, distinção de camada: a arquitetura discutida posiciona o dARK e a RBB como ramos irmãos sob uma camada comum, mas o dARK é aplicação e a RBB é rede. Essa distinção independe da hipótese sobre o substrato; suas consequências práticas, porém, dependem dela. Se o dARK operar sobre a RBB, o ramo correspondente à rede é redundante. Se, conforme a hipótese ainda não confirmada, operar em outra rede, a camada proposta passaria a atuar como roteador entre redes distintas, problema mais complexo, que implicaria duas conexões, duas carteiras, duas políticas de custo e dois modelos de finalização. Qual desses cenários se aplica depende da informação pendente registrada no INFORMACOES-NECESSARIAS.md, item 2.

Segunda objeção, risco de escopo: posicionar o dARK como núcleo do serviço pode levar à modelagem das operações de confiança como atribuição de identificador persistente. Objetos sem vocação para tanto (verificações periódicas de integridade, eventos de fluxo editorial, registros de operação) passariam a recebê-lo, com o efeito potencial de aumentar o volume de identificadores sem curadoria ou sem vocação para citabilidade. A extensão desse efeito sobre o dARK não foi avaliada; trata-se de risco de projeto, e não de dano demonstrado. Esta objeção não depende da informação pendente sobre o substrato. Ver a decisão D1 em documento-de-arquitetura.md.

Ponto único de confiança: o risco de a camada de fachada converter-se em ponto único de confiança é mitigado, mas não eliminado, pela decisão D2 (o resumo criptográfico é calculado no cliente; o serviço nunca recebe o arquivo) e pela natureza pública da função de verificação de inclusão (`verifyInclusion`), função de leitura executável sem passar pela camada de integração enquanto o registro permanecer disponível na rede. A fachada é conveniência, nunca autoridade, e qualquer evolução que a torne indispensável à verificação descaracteriza a proposta (relatório, seção 3.3; documento-de-arquitetura.md; modelo-de-ameacas.md).

## Conclusão da avaliação

Construir a camada de integração: sim, e o protótipo demonstra, em ambiente local, sua viabilidade técnica. Os resultados obtidos não sustentam, neste estágio, a caracterização do dARK como núcleo da camada. O modelo que melhor corresponde aos resultados do protótipo é aquele em que o dARK figura como um dos adaptadores da camada, o de identidade, e não como seu núcleo.

O protótipo sustenta a viabilidade dessa configuração: na sessão de demonstração, registro, versionamento, proveniência e verificação foram executados com a rota de identificador (`/v1/pids`) respondendo 501; a certificação, que não é exposta pela camada de integração, foi exercitada na suíte de testes (T11a), diretamente sobre o contrato, também sem acesso ao dARK. Esses resultados indicam, em ambiente local, que as primitivas exercitadas não dependem do dARK para funcionar.

Documentos relacionados: caracterizacao-do-dark.md, caracterizacao-da-rbb.md, documento-de-arquitetura.md, especificacao-da-interface-de-servico.md, analise-de-interoperabilidade.md.

## Fontes

dARK-PID. dARK: decentralized Archival Resource Key, core layer. [S. l.]: GitHub, [2025a]. Disponível em: https://github.com/dark-pid/dARK. Acesso em: 22 set. 2026.

dARK-PID. Hyperdrive: dARK minter API. [S. l.]: GitHub, [2025b]. Disponível em: https://github.com/dark-pid/hyperdrive. Acesso em: 22 set. 2026.

FERREIRA, L. C. A. blockchain-savits: contratos inteligentes, testes, protótipo de camada de integração e documentos técnicos da frente Blockchain/RBB do Projeto SAVITS. Versão v0.2.0. [S. l.]: GitHub, 2026. Disponível em: https://github.com/leokbral/blockchain-savits/tree/v0.2.0. Acesso em: 15 out. 2026.

REDE BLOCKCHAIN BRASIL. Rede Blockchain Brasil: arquitetura, governança e infraestrutura. [S. l.], 2026a. Disponível em: https://redeblockchainbrasil.org/. Acesso em: 22 set. 2026.

REDE BLOCKCHAIN BRASIL. rbb: repositório de arquivos para a infraestrutura da Rede Blockchain Brasil. [S. l.]: GitHub, [2026b]. Disponível em: https://github.com/RBBNet/rbb. Acesso em: 22 set. 2026.
