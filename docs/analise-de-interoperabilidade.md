# Análise de interoperabilidade

Projeto SAVITS, frente Blockchain/RBB. Documento técnico citado no Relatório final de atividades (seção 3.8).

**Classificação de maturidade: PROTOTIPADO no plano sistema-cadeia; MODELADO no plano cadeia-identificador; INVESTIGADO no plano rede-rede** (relatório, seção 3.3). Todo o trabalho experimental ocorreu em ambiente local; nenhuma execução ocorreu na RBB e nenhum identificador foi cunhado no dARK.

## 1. Três planos de interoperabilidade

| Plano | Situação | Evidência |
|---|---|---|
| **Sistema e cadeia** | PROTOTIPADO: interface de serviço web (REST) com autenticação simulada por *token* fixo de demonstração; o cliente não conhece *blockchain*, não gerencia chave e não assina transação. A autenticação por credencial institucional é proposta, não implementada | `evidence/logs/gateway-session.log` |
| **Cadeia e sistema de identificador persistente** | MODELADO, não integrado: o contrato armazena o ARK como referência externa (`bindPid`, testado em T14), mas o identificador usado é **SIMULADO**; nenhum identificador foi cunhado no dARK | T14; `/v1/pids` responde HTTP 501 |
| **Rede e rede** | INVESTIGADO apenas | Seção 4 |

## 2. Por que interface de serviço web, e não biblioteca

O próprio ecossistema dARK adota esse padrão: sua interface de cunhagem (Hyperdrive) é descrita como destinada a software de repositório que necessita obter identificadores **sem interagir diretamente com a *blockchain*** (relatório, seções 3.3 e 3.6; `caracterizacao-do-dark.md`). A interface de serviço web foi identificada, desde a fase de fundamentação, como caminho de menor acoplamento, e a camada de integração prototipada replica esse padrão para as demais primitivas.

A opção responde também a uma incompatibilidade concreta: a biblioteca de integração disponível no ecossistema dARK é escrita em Python, ao passo que os sistemas institucionais que a consumiriam são majoritariamente escritos em Java e PHP. Uma fachada HTTP elimina a necessidade de portar biblioteca para cada linguagem. A redução efetiva do custo de adoção não foi medida; sua aferição depende da integração de um sistema real (relatório, seção 3.7).

## 3. Interoperabilidade de identificadores

O resolvedor do dARK é descrito como capaz de resolver ARK e DOI, encaminhando a consulta ao resolvedor apropriado quando o identificador não pertence à sua rede, e seu modelo de dados prevê campo destinado a mapear identificadores externos já atribuídos ao mesmo registro (relatório, seções 3.3 e 3.6; `caracterizacao-do-dark.md`). Essas capacidades foram apuradas em fontes documentais e não foram exercitadas neste trabalho.

**Consequência para o SAVITS:** não é necessário nem desejável criar identificador novo. O caminho é registrar o ativo com seu ARK e mapear os identificadores externos que ele já possua.

## 4. Interoperabilidade entre redes

**Necessita validação.** A existência de instância de produção do dARK e a rede sobre a qual ela operaria não foram localizadas nas fontes consultadas (relatório, seção 3.7; INFORMACOES-NECESSARIAS.md, item 2). Formula-se a hipótese, ainda não confirmada, de que eventual instância de produção do dARK opere sobre outra rede, própria ou de consórcio, e não sobre a RBB. A resposta determina se existe problema de interoperabilidade entre redes a resolver. Caso sejam redes distintas, as opções são migração, coexistência ou ponte entre redes, cada uma com implicações técnicas, operacionais e de governança distintas. Ver `integracao-dark-rbb.md`.
