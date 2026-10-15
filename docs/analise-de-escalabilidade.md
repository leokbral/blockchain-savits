# Análise de escalabilidade

Projeto SAVITS, frente Blockchain/RBB. Documento técnico citado no Relatório final de atividades (seção 3.8).

**Classificação de maturidade: VALIDADO EXPERIMENTALMENTE** (relatório, seção 3.3), em ambiente local: o custo da ancoragem em lote foi medido; o custo do registro individual para N objetos foi calculado por extrapolação a partir de uma chamada medida. Vazão, latência, finalização e demais limites da rede real **não foram medidos**, por ausência de acesso.

## 1. O problema dimensionado

O custo em cadeia do registro individual cresce linearmente com o número de objetos. Os volumes anuais de depósito nos sistemas institucionais não são conhecidos (INFORMACOES-NECESSARIAS.md, item 8), nem os parâmetros de custo e de cota aplicáveis ao Ibict na RBB (item 4). Por isso a análise é feita por faixas paramétricas, de 1 a 100.000 objetos, e não por dimensionamento efetivo.

O requisito RNF-02 (custo por objeto compatível com acervos de 10⁵ a 10⁶ itens, `documento-de-arquitetura.md`) foi exercitado pelo experimento E2 até 10⁵ objetos; sua compatibilidade não foi verificada, por depender desses volumes e parâmetros.

A alternativa examinada e implementada no protótipo é a agregação em lote por árvore de Merkle: publica-se em cadeia a raiz do lote, com seus metadados, em vez de um registro por objeto, e emite-se, para cada objeto, um recibo com o caminho de inclusão, que permite verificação criptográfica posterior sem consulta ao serviço emissor.

## 2. Experimento E2: custo comparado

Procedimento (`tests/run_tests.py`): mediu-se o gás de uma única chamada de `registerVersion` (registro individual, 164.029, teste T02) e o gás de uma transação de `anchorBatch` (um lote inteiro) para cada valor de N. A coluna de registro individual **não foi medida com N transações**: foi calculada por extrapolação linear, multiplicando por N o gás da chamada medida. O fator de redução resulta da razão entre as duas colunas. Para N acima de 4.096, a raiz foi calculada sobre 4.096 folhas, e o valor N foi informado ao contrato como contagem de folhas.

Ambiente: local, compatível com a EVM (eth-tester sobre py-evm), compilador Solidity 0.8.26, otimizador habilitado em 200 execuções, `evmVersion: paris`. Os valores não foram aferidos na RBB. Dados brutos: `evidence/test-results/gas-benchmark.csv`.

| Objetos (N) | Registro individual, calculado (N × 164.029) | Ancoragem em lote, medida (1 transação) | Fator de redução |
|---|---|---|---|
| 1 | 164.029 | 76.571 | 2× |
| 10 | 1.640.290 | 76.571 | 21× |
| 100 | 16.402.900 | 76.571 | 214× |
| 1.000 | 164.029.000 | 76.583 | 2.142× |
| 10.000 | 1.640.290.000 | 76.583 | 21.418× |
| 100.000 | 16.402.900.000 | 76.595 | 214.151× |

O custo medido da ancoragem permanece essencialmente constante porque `anchorBatch` grava, para cada lote, a raiz, a contagem de folhas, o carimbo de tempo e o remetente, qualquer que seja o número de objetos. A verificação permanece criptográfica: o caminho de inclusão de um lote de 1.000 folhas tem 10 níveis, e foi verificado em cadeia com resultado verdadeiro para folha presente e falso para folha ausente (teste T13). Na suíte, essa primeira ancoragem (T13) consumiu 93.683 de gás; nas medições, `anchorBatch` variou de 76.571 a 93.683 de gás.

O gás expressa o custo computacional de cada operação na EVM e não se confunde com custo financeiro. No contexto da RBB, indica a carga que cada operação impõe a uma infraestrutura compartilhada e pode servir de insumo a eventual política de cota definida pela governança da rede.

## 3. Ressalva metodológica

**Os dois mecanismos não são funcionalmente equivalentes, e a tabela acima não deve ser lida como "o lote é 2.142× melhor".** O registro individual carrega identidade do ativo, índice de versão, algoritmo de resumo, resumo de metadados e vínculos de proveniência consultáveis em cadeia. A ancoragem em lote prova unicamente que um resumo existia em determinado instante; qualquer semântica adicional fica fora da cadeia, no recibo. A medição é de custo, não de função.

A leitura correta é: **registro individual quando o objeto exige identidade e versionamento consultáveis; ancoragem em lote quando exige apenas prova de existência e integridade.** Um acervo de preservação digital é caso da ancoragem em lote; um modelo de aprendizado de máquina empregado em avaliação de política pública é caso do registro individual.

## 4. Fatores não medidos

| Fator | Situação |
|---|---|
| Vazão real da RBB (transações por segundo, intervalo de bloco, limite de gás por bloco) | **Não medido**, por ausência de acesso; necessita validação (INFORMACOES-NECESSARIAS.md) |
| Latência de finalização do consenso QBFT | **Não medida**, por ausência de acesso; necessita validação |
| Crescimento do estado na ordem de milhões de ativos | **Não testado; a validar.** No código, a consulta por `_hashIndex` é um acesso direto a mapeamento, mas o estado cresce linearmente com o número de versões registradas; o comportamento nessa ordem de grandeza não foi exercitado |
| Custo de leitura em nó observador | Não medido |

## 5. Consequência de projeto

A camada de integração prototipada expõe a agregação em lote como rota própria (`POST /v1/proofs/batches`), com emissão de recibos de inclusão na resposta, e a verificação de inclusão como função pública de leitura (`GET /v1/proofs/{id}/inclusion`). A persistência dos recibos pelo serviço não foi implementada. A decisão corresponde à D3 de `documento-de-arquitetura.md` (relatório, seção 3.3).
