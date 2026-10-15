# Documentos técnicos da frente Blockchain/RBB

Projeto SAVITS (Sistema de Avaliação e Validação de Impactos em Tecnologias Sociais), Ibict.

Esta pasta reúne os documentos técnicos elaborados no período coberto pelo *Relatório final de atividades* da frente Blockchain/RBB, no qual são citados (seção 3.8). O relatório sintetiza os resultados; o detalhamento de cada atividade está nestes documentos, disponibilizados para apreciação e discussão com o ponto focal de Blockchain quanto às possibilidades de implementação no âmbito do SAVITS.

**Aviso de ambiente.** Os experimentos descritos foram executados em ambiente local compatível com a Máquina Virtual Ethereum. Nenhuma execução ocorreu na Rede Blockchain Brasil e nenhum identificador foi cunhado no dARK. As classificações de maturidade seguem a escala descrita em [matriz-de-maturidade.md](matriz-de-maturidade.md).

## Documentos

| Documento | Conteúdo | Atividade | Maturidade |
|---|---|---|---|
| [Documento de arquitetura](documento-de-arquitetura.md) | Requisitos, camadas, fluxos e decisões arquiteturais. | A1 | MODELADO e PROPOSTO |
| [Análise de escalabilidade](analise-de-escalabilidade.md) | Experimento de custo comparado entre registro individual e ancoragem em lote. | A1 | VALIDADO EXPERIMENTALMENTE |
| [Análise de privacidade](analise-de-privacidade.md) | Superfícies de exposição e fragilidade declarada. | A1 | MODELADO |
| [Análise de interoperabilidade](analise-de-interoperabilidade.md) | Três planos de integração. | A1 | INVESTIGADO e PROTOTIPADO |
| [Análise de conformidade com a LGPD](analise-de-conformidade-lgpd.md) | Decisão campo a campo e ressalvas. | A1 | MODELADO |
| [Modelo de ameaças](modelo-de-ameacas.md) | Ameaças identificadas e situação das mitigações. | A1 | MODELADO |
| [Modelo de dados](modelo-de-dados.md) | Entidades, destino de cada campo e custo por operação. | A2 e A3 | PROTOTIPADO |
| [Especificação da interface de serviço](especificacao-da-interface-de-servico.md) | Rotas, códigos de resposta e exemplos do protótipo da camada de integração. | A1 e A2 | MODELADO |
| [Caracterização do dARK](caracterizacao-do-dark.md) | Capacidades, fontes e limitações. | 2.3.2 | INVESTIGADO |
| [Caracterização da RBB](caracterizacao-da-rbb.md) | Capacidades, aplicação e pontos a validar. | A1 | INVESTIGADO |
| [Análise da integração entre dARK e RBB](integracao-dark-rbb.md) | Hipóteses de causa e avaliação crítica da hipótese de encapsulamento. | A1 e 2.3.2 | INVESTIGADO |
| [Catálogo de produtos e serviços](catalogo-de-produtos-e-servicos.md) | Possibilidades que satisfazem o critério discriminante e possibilidades descartadas. | Ampliação do escopo | PROPOSTO |
| [Matriz de rastreabilidade](matriz-de-rastreabilidade.md) | Caminho de cada atividade oficial até o documento ou artefato produzido e a evidência que o comprova. | A4 | Não se aplica |
| [Matriz de maturidade dos resultados](matriz-de-maturidade.md) | Escala de maturidade e nível atingido por resultado. | A4 | Não se aplica |
| [Informações necessárias à continuidade](INFORMACOES-NECESSARIAS.md) | Informações não obtíveis por fonte pública que condicionam decisões de projeto, com a alternativa adotada. | A4 | Não se aplica |

## Artefatos executáveis

Os contratos, os scripts de compilação e de execução, a suíte de testes, o protótipo da camada de integração e os registros de execução estão nas demais pastas deste repositório (ver o [README principal](../README.md)).
