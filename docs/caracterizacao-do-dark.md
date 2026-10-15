# Caracterização do dARK

Projeto SAVITS, frente Blockchain/RBB. Documento técnico citado no Relatório final de atividades (seção 3.8).

Classificação de maturidade: INVESTIGADO (caracterização das capacidades, seção 3.6 do relatório); MODELADO (divisão de responsabilidades entre identificação e prova, seção 3.6); HIPÓTESE, a validar empiricamente (uso da carga associada como manifesto de integridade, seção 3.6).

## Fontes e regra aplicada

A caracterização apoia-se em fontes primárias: a documentação técnica oficial mantida nos repositórios do projeto dARK (camada central, interface de cunhagem Hyperdrive e resolvedor), o *whitepaper* depositado no Zenodo com DOI próprio e o artigo revisado por pares publicado na revista BiblioCanto. Notícias institucionais foram empregadas exclusivamente para confirmação de fatos e de marcos temporais, nunca como base de afirmação técnica.

Regra aplicada: não presumir que o dARK possua determinada capacidade apenas porque sistemas congêneres a possuem. Cada capacidade não confirmada é registrada como tal e remetida a INFORMACOES-NECESSARIAS.md (informações necessárias para a continuidade).

## Capacidades apuradas

| Capacidade | Descrição apurada | Limitação ou incógnita |
|---|---|---|
| Implementação descentralizada do ARK | Não constitui esquema novo de identificação: é implementação do padrão ARK sobre nós institucionais. | Depende do resolvedor global do esquema ARK. |
| Camada central em contratos inteligentes | Regras de cunhagem, gestão de metadados e permissões implementadas em Solidity sobre Máquina Virtual Ethereum, em rede permissionada Hyperledger Besu. | Custo e latência por identificador não medidos. |
| Registro por transação | A criação de identificador é transação, o que assegura unicidade e imutabilidade do registro. | Nenhuma registrada. |
| Trilha de auditoria e prova de existência | Toda operação fica registrada de forma imutável; carimbo de tempo e resumo criptográfico proveem prova de existência. | A prova aplica-se aos metadados registrados, não necessariamente ao objeto identificado. |
| Estratégia híbrida de armazenamento | Metadados essenciais e resumos em cadeia; cargas volumosas fora dela. | Limites de tamanho não documentados publicamente. |
| Esquema de metadados flexível | Atribuição de identificador a, potencialmente, qualquer objeto digital ou físico. | Flexibilidade não equivale a semântica definida. |
| Atributos do registro | O registro contempla sufixo do identificador (`noid`), identificadores externos mapeados (`external_pids`), localização (`url`) e carga associada (`payload`). | O tipo textual e a operação de atualização da carga estão documentados; os esquemas adotados e o limite de tamanho não estão especificados publicamente (ver "Achado relevante", adiante). |
| Operação de definição da carga associada | A documentação da interface de cunhagem relaciona quatro operações, entre as quais definir uma carga associada a um identificador, com a regra de negócio de que essa operação exige que o identificador possua localização previamente definida. | A hipótese de que essa exigência impeça o uso do dARK para eventos e objetos sem localização pública não foi testada (integracao-dark-rbb.md). |
| Interface de cunhagem por serviço web | Destinada a *software* de repositório que necessita obter identificadores sem interagir diretamente com a cadeia. | Exige componente cliente por plataforma. |
| Biblioteca de integração | Biblioteca em Python para cunhagem, resolução e consulta em cadeia. | Disponível apenas em Python; sistemas institucionais são majoritariamente Java e PHP. |
| Resolvedor com suporte a múltiplos esquemas | Resolve ARK e DOI, encaminhando ao resolvedor apropriado quando o identificador não pertence à sua rede. | Extensível, mas hoje restrito a esses esquemas. |
| Atribuição em lote a partir de coleta | Mapeamento e processamento em lote a partir de coleta de metadados. | Vinculada a instituição parceira; operação efetiva não verificada. |
| Versionamento de objetos | Não localizado nas fontes consultadas. | Necessita validação. |
| Registro do resumo do objeto identificado | Não localizado nas fontes consultadas. | Necessita validação; condiciona a hipótese descrita em "Achado relevante" e a possibilidade "Identificador persistente com prova de integridade" (catalogo-de-produtos-e-servicos.md). |
| Existência de instância em produção e rede sobre a qual operaria | Não localizadas nas fontes consultadas. | Necessita validação (INFORMACOES-NECESSARIAS.md, item 2; integracao-dark-rbb.md). |
| Competência decisória sobre alterações no núcleo do dARK | Não localizada nas fontes consultadas. | Necessita validação (INFORMACOES-NECESSARIAS.md, item 5). |

Fonte: elaboração a partir da documentação técnica oficial do projeto (dARK-PID, [2025a], [2025b], [2025c]), do *whitepaper* (SEGUNDO et al., 2022) e do artigo revisado por pares (SEGUNDO et al., 2023).

Não se afirma, neste documento, que o dARK opere em produção nem sobre qual rede operaria: essas informações não foram localizadas nas fontes primárias consultadas e dependem de informação institucional.

## Complementaridade entre dARK e registro distribuído

Classificação: MODELADO. A atividade 2.3.2 exige determinar, de forma inequívoca, o que cabe a cada camada. O quadro abaixo reproduz a divisão a que a investigação chegou (seção 3.6 do relatório).

| Questão | Resposta |
|---|---|
| O que o dARK resolve? | Identidade e localização: atribuir nome persistente a um objeto e resolvê-lo para onde ele está, ainda que mude de lugar. |
| O que o registro distribuído resolve? | Integridade, temporalidade e auditabilidade: provar que um conteúdo específico existia, naquele estado, naquele instante, e que o registro não foi reescrito. |
| Onde há complementaridade? | No caso de uso central, é total: o identificador diz qual é o objeto; o resumo diz se é o mesmo objeto. Um sem o outro deixa metade do problema em aberto. |
| Onde há sobreposição? | Ambos persistem registro em cadeia e oferecem prova de existência. Duplicar contratos de registro seria desperdício de esforço público. |
| O que deve permanecer no dARK? | Cunhagem, resolução, mapeamento de identificadores externos, localização e curadoria do identificador. |
| O que deve ir para contrato próprio? | Versões com resumo de conteúdo, eventos de proveniência, certificações e consentimento: tudo o que não é identidade. |
| O que deve permanecer fora da cadeia? | O artefato, os metadados descritivos, o termo de consentimento e os registros de execução. |

## Achado relevante: a carga associada como ponto de extensão

Classificação: HIPÓTESE, a validar empiricamente. Distinguem-se três planos: o que a documentação estabelece, o que se formula como hipótese técnica a partir dela e o que foi demonstrado empiricamente.

No plano documental, a documentação da interface de cunhagem (dARK-PID, [2025b]) relaciona a operação de definir uma carga associada a um identificador, que exige localização previamente definida. A documentação técnica do repositório oficial (dARK-PID, [2025a]) descreve essa carga como campo textual do registro do identificador, cujo formato é determinado por esquema definido fora do código dos contratos, tipicamente em arquivo de configuração, e prevê operação de atualização da localização e da carga de identificador existente. Registra ainda que cargas maiores podem ser mantidas fora da cadeia, com apenas o resumo da carga registrado nela. A documentação não especifica limite de tamanho para o campo, não descreve os esquemas efetivamente adotados e refere-se ao resumo da carga, isto é, dos metadados, e não ao resumo do objeto identificado.

No plano da hipótese técnica, se a carga comportar um manifesto com o resumo criptográfico do objeto, a versão e referências de proveniência, o dARK já disporia do ponto de extensão necessário para associar prova de integridade ao identificador. Como o formato da carga é definido por esquema externo ao código dos contratos, é plausível que essa extensão possa ser realizada sem alteração de contratos. Essa possibilidade, porém, não é afirmada pela documentação: depende de o esquema admitir o manifesto, de o tamanho resultante ser compatível com o registro em cadeia e de eventual instância em operação adotar configuração que o permita.

No plano empírico, nenhum desses pontos foi demonstrado: a operação de carga associada não foi exercitada.

Consequência prática. Caso a hipótese se confirme, a incorporação de prova de integridade ao identificador persistente poderá apoiar-se em convenção semântica documentada sobre funcionalidade existente, em vez de exigir alterações no núcleo de um sistema já implementado, diferença relevante em esforço de desenvolvimento e, havendo instância em operação, em risco operacional. Caso não se confirme, a alternativa é o contrato próprio já prototipado, que atende a essa necessidade sem depender do dARK. Nenhum dos dois desfechos é afirmado antes do experimento.

Encaminhamento. O comportamento do código publicado pode ser verificado em ambiente local do próprio dARK, cujo procedimento de implantação consta da documentação pública, sem depender de credenciais nem de acesso à RBB. A existência de instância em operação e sua configuração, incluindo os esquemas de carga adotados, permanecem dependentes de informação institucional. A verificação em ambiente local é o item de melhor relação entre esforço e valor informacional entre os relacionados no INFORMACOES-NECESSARIAS.md, onde figura como item 1.

## Situação da atividade 2.3.2

O modelo de dados prevê o identificador persistente como referência externa, com operação própria de vinculação (`bindPid`), testada no teste T14 com identificador explicitamente marcado como simulado. A rota correspondente da camada de integração (`/v1/pids`) responde com código 501 (não implementado), indicando o motivo e o encaminhamento. A análise de complementaridade está concluída. A atividade encontra-se modelada e parcialmente prototipada, e não integrada: não foi cunhado nenhum identificador real, não foi testada a operação de carga associada e não foi medido o custo de cunhagem.

Documentos relacionados: integracao-dark-rbb.md, caracterizacao-da-rbb.md, modelo-de-dados.md, documento-de-arquitetura.md, catalogo-de-produtos-e-servicos.md.

## Fontes

dARK-PID. dARK: decentralized Archival Resource Key, core layer. [S. l.]: GitHub, [2025a]. Disponível em: https://github.com/dark-pid/dARK. Acesso em: 22 set. 2026.

dARK-PID. Hyperdrive: dARK minter API. [S. l.]: GitHub, [2025b]. Disponível em: https://github.com/dark-pid/hyperdrive. Acesso em: 22 set. 2026.

dARK-PID. dark-resolver: dARK resolver. [S. l.]: GitHub, [2025c]. Disponível em: https://github.com/dark-pid/dark-resolver. Acesso em: 22 set. 2026.


SEGUNDO, W. et al. dARK: a decentralized blockchain implementation of ARK persistent identifiers. Zenodo, 2022. Preprint. DOI: 10.5281/zenodo.7442743.

SEGUNDO, W. et al. dARK: uma implementação descentralizada de identificadores persistentes ARK baseada em blockchain. BiblioCanto, Natal, v. 9, n. 2, p. 147-158, 2023. DOI: 10.21680/2447-7842.2023v9n2ID33759.
