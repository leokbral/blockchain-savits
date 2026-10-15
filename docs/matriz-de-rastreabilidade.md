# Matriz de rastreabilidade

Projeto SAVITS, frente Blockchain/RBB. Documento técnico citado no Relatório final de atividades (seção 3.8).

A matriz permite percorrer, para cada atividade oficial (Quadro 1 do relatório), o caminho que vai do trabalho realizado ao documento ou artefato produzido e à evidência que o comprova. Nenhuma linha registra evidência inexistente. As identificações T01 a T14 referem-se aos testes da suíte `tests/run_tests.py`, cujos resultados estão em `evidence/test-results/`. A escala de maturidade está em [matriz-de-maturidade.md](matriz-de-maturidade.md).

| Atividade | Trabalho realizado | Artefato | Evidência | Maturidade |
|---|---|---|---|---|
| A1 | Requisitos arquiteturais | Documento de arquitetura | 14 requisitos com verificação associada | MODELADO |
| A1 | Arquitetura de referência | Documento de arquitetura | Camadas, componentes e fluxos | PROPOSTO |
| A1 | Decisões arquiteturais | Documento de arquitetura | 5 decisões com contrapartida declarada | MODELADO |
| A1 | Escalabilidade | Análise de escalabilidade e experimento E2 | Medição da ancoragem em 6 pontos, com registro individual extrapolado; arquivo de dados | VALIDADO EXPERIMENTALMENTE |
| A1 | Privacidade | Análise de privacidade | Matriz de observáveis; fragilidade declarada | MODELADO |
| A1 | Interoperabilidade | Análise de interoperabilidade e protótipo | Sessão com cliente sem chave nem carteira | PROTOTIPADO |
| A1 | Conformidade com a LGPD | Análise de conformidade com a LGPD | Decisão campo a campo; ressalvas declaradas | MODELADO |
| A1 | Segurança | Modelo de ameaças | 12 ameaças; 2 mitigações verificadas em T12 | MODELADO e parcialmente TESTADO |
| A2 | Modelo de dados | Modelo de dados e contrato de registro | Entidades do contrato e custo medido por operação | PROTOTIPADO |
| A2 | Rastreabilidade | Função de registro de evento | T04: origem verificada em cadeia | TESTADO |
| A2 | Certificação | Funções de certificação e revogação | T11a: transição de estado completa | TESTADO |
| A2 | Integridade | Função de verificação e protótipo | T06 e T08: intacto e adulterado | VALIDADO EXPERIMENTALMENTE |
| A2 | Imutabilidade | Contrato de registro | T09 e T10: nova versão sem sobrescrita | TESTADO |
| A2 | Prova de conceito | Camada de integração | Registro de sessão com dezesseis chamadas, precedidas de verificação do estado do serviço | PROTOTIPADO e TESTADO |
| A3 | Consentimento | Funções de registro e revogação | T11b: ativo e depois inativo | TESTADO |
| A3 | Certificação em contrato | Contrato de registro | T11a e cenários de erro em T12; verificação de emissor implementada, não exercitada | TESTADO |
| A3 | Rastreabilidade em contrato | Funções de evento e referência de versão | T04 e T10 | TESTADO |
| A3 | Protótipo de contrato | 2 contratos, 11.616 bytes | Compilação e 15 testes aprovados | PROTOTIPADO e TESTADO |
| 2.3.2 | Identificador para modelos e conjuntos de dados | Função de vinculação e rota de cunhagem | T14 com identificador SIMULADO; rota responde 501 | MODELADO e PARCIALMENTE PROTOTIPADO. Não integrado. |
| A4 | Consolidação | Relatório final e documentos técnicos | Relatório e documentos desta pasta | Não se aplica (entregável documental) |
