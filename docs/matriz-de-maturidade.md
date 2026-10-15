# Matriz de maturidade dos resultados

Projeto SAVITS, frente Blockchain/RBB. Documento técnico citado no Relatório final de atividades (seção 3.8).

## Escala de classificação

Todo resultado recebe uma das classificações abaixo. A escala existe para que estudo não seja lido como implementação, proposta não seja lida como decisão e protótipo não seja lido como produto em operação.

| Classificação | Significado | Evidência exigida |
|---|---|---|
| INVESTIGADO | Foi realizada pesquisa documentada sobre o tema. | Registro da investigação com fontes identificadas. |
| MODELADO | Foi produzido modelo, especificação ou arquitetura. | Documento ou diagrama correspondente. |
| PROPOSTO | Foi formulada solução conceitual ainda não validada institucionalmente. | Proposta técnica justificada. |
| PROTOTIPADO | Existe implementação experimental executável. | Código-fonte que compila e executa. |
| TESTADO | Existe execução experimental documentada. | Registro de teste com resultado obtido. |
| VALIDADO EXPERIMENTALMENTE | Existe experimento com resultado medido e reprodutível. | Dados de execução e procedimento reproduzível. |
| IMPLEMENTADO | Existe implementação em ambiente institucional. | Não atribuído neste trabalho. |
| INTEGRADO | Existe integração efetiva com o sistema correspondente. | Não atribuído neste trabalho. |
| ADOTADO | Existe evidência de adoção institucional. | Não atribuído neste trabalho. |

## Nível atingido por resultado

As classificações IMPLEMENTADO, INTEGRADO e ADOTADO não foram atribuídas a nenhum resultado, por inexistência de evidência que as sustente.

| Resultado | Nível atingido | O que faltaria para o nível seguinte |
|---|---|---|
| Estado da arte e lacuna identificada | INVESTIGADO | Revisão sistemática com protocolo e bases fechadas. |
| Caracterização do dARK | INVESTIGADO | Acesso à documentação interna e ao ambiente do sistema. |
| Caracterização da RBB | INVESTIGADO | Acesso submissor e dados operacionais da rede. |
| Requisitos arquiteturais | MODELADO | Validação dos requisitos pela coordenação do projeto. |
| Arquitetura de referência | PROPOSTO | Decisão institucional e implantação em ambiente real. |
| Modelo de dados | PROTOTIPADO | Execução sobre rede real com dados institucionais. |
| Contrato de registro de ativos | PROTOTIPADO e TESTADO | Auditoria independente e implantação em rede da RBB. |
| Contrato de ancoragem de provas | PROTOTIPADO e TESTADO | Auditoria independente e implantação em rede da RBB. |
| Camada de integração institucional | PROTOTIPADO e TESTADO | Autenticação por credencial institucional, custódia de chaves, cota, persistência de recibos e uso por sistema real. |
| Mecanismo de integridade e detecção de adulteração | VALIDADO EXPERIMENTALMENTE | Execução sobre rede real e sobre acervo institucional. |
| Medição de custo e escala | VALIDADO EXPERIMENTALMENTE | Medição de vazão e latência sobre a rede real. |
| Mecanismo de rastreabilidade | TESTADO | Validação semântica com os núcleos produtores dos artefatos. |
| Mecanismo de certificação | TESTADO | Teste da verificação de emissor na revogação; definição institucional de quem certifica e sob que critério. |
| Mecanismo de consentimento | TESTADO | Implementação da derivação da referência com chave; parecer do encarregado de dados sobre o modelo adotado. |
| Análise de conformidade com a LGPD | MODELADO | Parecer jurídico institucional. |
| Modelo de ameaças | MODELADO e parcialmente TESTADO | Teste de intrusão e auditoria de contratos. |
| Vinculação de identificador persistente | MODELADO e PARCIALMENTE PROTOTIPADO. Não integrado. | Credenciais de acesso ao dARK e cunhagem real. |
| Possibilidades de produtos e serviços | PROPOSTO | Priorização institucional e prova de conceito com área demandante. |
