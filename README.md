# blockchain-savits

Contratos inteligentes, suíte de testes e protótipo de camada de integração (gateway
HTTP) desenvolvidos na frente Blockchain / Rede Blockchain Brasil (RBB) do Projeto
SAVITS – Sistema de Avaliação e Validação de Impactos em Tecnologias Sociais, executado
pelo Instituto Brasileiro de Informação em Ciência e Tecnologia (Ibict).

O repositório reúne os artefatos executáveis e as evidências de execução citados no
relatório técnico consolidado da frente. Os documentos analíticos (arquitetura, modelo
de ameaças, análise de conformidade com a LGPD e demais) integram o relatório e não
estão incluídos aqui.

> **Ambiente de execução — leia antes de usar os resultados**
>
> - Todos os testes, medições e a sessão de demonstração foram executados em **ambiente
>   local** compatível com a Máquina Virtual Ethereum (EVM), provido por `eth-tester`
>   sobre `py-evm`.
> - **Nada foi executado na Rede Blockchain Brasil**, nem em rede de testes, nem em
>   produção. Os valores de gás referem-se exclusivamente ao ambiente local.
> - **Nenhum identificador foi cunhado no dARK.** Os identificadores ARK que aparecem nos
>   testes são marcados como `SIMULADO`, e a rota `/v1/pids` do gateway responde
>   `HTTP 501` por ausência de credenciais de acesso.
> - Trata-se de **protótipo experimental**. Os contratos não passaram por auditoria,
>   análise estática nem verificação formal.

## Conteúdo

| Caminho | Conteúdo |
|---|---|
| `contracts/contracts/SavitsAssetRegistry.sol` | Registro de ativos (conjuntos de dados, modelos e outros), versões com resumo criptográfico, eventos de proveniência, certificação com revogação, consentimento com revogação por estado, vínculo a identificador persistente externo e controle de acesso por papéis |
| `contracts/contracts/ProofAnchor.sol` | Ancoragem em lote por raiz de árvore de Merkle e verificação de caminho de inclusão |
| `compile.js` | Compilação com `solc` 0.8.26 (otimizador ativado, 200 execuções, `evmVersion: paris`) |
| `build/artifacts.json` | ABI e bytecode resultantes da compilação, lidos pelos testes e pelo gateway |
| `tests/run_tests.py` | Suíte de 15 testes e experimento de custo comparado |
| `poc/backend/gateway.py` | Protótipo de gateway HTTP com 9 rotas sobre os dois contratos |
| `poc/integration/demo_session.py` | Sessão de demonstração que sobe o gateway e o exercita por HTTP |
| `evidence/` | Registros das execuções: log dos testes, resultados em JSON e Markdown, medição de gás em CSV, histórico de versões e log da sessão do gateway |
| `reproduzir.sh` | Executa compilação, testes e sessão de demonstração em sequência |

## Requisitos

- Node.js e npm (a reexecução de conferência usou Node.js 22)
- Python 3.11 ou superior
- Dependências Python fixadas em `requirements.txt` (`web3` 8.0.0, `eth-tester` 0.14.0b1,
  `py-evm` 0.12.1b1)
- Dependência npm fixada em `package.json` e `package-lock.json` (`solc` 0.8.26)

## Reprodução

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
./reproduzir.sh
```

O script executa, nesta ordem:

1. `npm ci` e `node compile.js contracts/contracts build` — recompila os contratos e
   regrava `build/artifacts.json`;
2. `python3 tests/run_tests.py` — gera os arquivos de trabalho em `experiments/workdir/`,
   executa os 15 testes e o experimento de custo, e regrava `evidence/logs/execution.log`,
   `evidence/test-results/` e `evidence/examples/`;
3. `python3 poc/integration/demo_session.py` — sobe o gateway na porta local 8899 e
   regrava `evidence/logs/gateway-session.log`.

**A ordem importa.** A sessão de demonstração usa o conjunto de dados sintético no
estado em que a suíte de testes o deixa, isto é, já com a alteração aplicada no teste
T07. Por isso o resumo inicial do conjunto de dados na sessão é
`0x458ad750…c64ea08`, e não o do arquivo recém-gerado.

**Conferência.** Como a execução regrava `evidence/`, `git diff evidence/` compara a
nova execução com a registrada. Na reexecução feita antes da publicação, a partir de
cópia limpa deste repositório, o `build/artifacts.json` recompilado foi idêntico byte a
byte ao registrado, e as únicas diferenças nos registros foram carimbos de data e hora
(de relógio e de bloco). Resultados dos testes, valores de gás e medição em CSV foram
idênticos.

Os arquivos de `experiments/workdir/` são sintéticos (50 linhas de indicadores fictícios
e um arquivo binário de 10.267 bytes), gerados pela própria suíte a cada execução, e por
isso não são versionados.

## Resultados registrados

Valores extraídos de `evidence/`, referentes ao ambiente local descrito acima.

**Testes** (`evidence/test-results/tests.md`): 15 de 15 aprovados.

| ID | Atividade | Teste |
|---|---|---|
| T01 | A2 | Registrar ativo (conjunto de dados) |
| T14 | A2 / 2.3.2 | Vincular identificador persistente ao ativo — identificador `SIMULADO` |
| T02 | A2 | Registrar resumo criptográfico da versão inicial |
| T03 | A2 | Registrar versão de modelo |
| T04 | A2 / A3 | Registrar evento de proveniência (conjunto de dados → modelo) |
| T05 | A2 | Consultar ativo |
| T06 | A2 | Verificar integridade — objeto intacto |
| T07 | A2 | Alterar objeto fora da cadeia (um caractere: `0.510` → `0.910`) |
| T08 | A2 | Detectar a alteração |
| T09 | A2 | Registrar nova versão |
| T10 | A2 | Consultar histórico de versões |
| T11a | A3 | Certificar e revogar certificação |
| T11b | A3 | Registrar e revogar consentimento |
| T12 | A3 | Cenários de erro e controle de acesso — 7 chamadas inválidas, todas revertidas |
| T13 | A1 / A2 | Ancoragem em lote de 1.000 folhas e prova de inclusão (verdadeira para folha presente, falsa para ausente) |

A1 a A3 designam as atividades da frente às quais cada teste se relaciona; 2.3.2 é a
atividade de identificadores persistentes via dARK.

**Tamanho em execução dos contratos** (saída de `compile.js`): `SavitsAssetRegistry`
9.653 bytes; `ProofAnchor` 1.963 bytes. Ambos abaixo do limite de 24.576 bytes do
EIP-170.

**Gás por operação** (`evidence/test-results/tests.json`):

| Operação | Gás |
|---|---:|
| Implantação de `SavitsAssetRegistry` | 2.163.202 |
| Implantação de `ProofAnchor` | 522.328 |
| `registerEvent` | 189.112 |
| `registerVersion` | 164.029 |
| `certify` | 162.783 |
| `registerConsent` | 161.118 |
| `registerAsset` | 97.165 |
| `anchorBatch` (T13, 1.000 folhas, primeiro lote) | 93.683 |
| `bindPid` | 74.926 |
| `revokeCertification` | 35.768 |
| `revokeConsent` | 33.841 |

**Custo comparado** (`evidence/test-results/gas-benchmark.csv`):

| Objetos (N) | Registro individual (N × 164.029) | Ancoragem em lote (1 transação) | Fator |
|---:|---:|---:|---:|
| 1 | 164.029 | 76.571 | 2,1 |
| 10 | 1.640.290 | 76.571 | 21,4 |
| 100 | 16.402.900 | 76.571 | 214,2 |
| 1.000 | 164.029.000 | 76.583 | 2.141,8 |
| 10.000 | 1.640.290.000 | 76.583 | 21.418,5 |
| 100.000 | 16.402.900.000 | 76.595 | 214.151,1 |

Condições de leitura desta tabela:

- **Os mecanismos não são funcionalmente equivalentes.** O registro individual grava
  identidade do ativo, índice de versão, algoritmo e vínculos de proveniência consultáveis
  em cadeia. A ancoragem em lote prova apenas que um resumo pertencia a um lote publicado
  em determinado instante. A tabela mede custo, não função.
- A coluna de registro individual é calculada (N × o gás medido de uma chamada de
  `registerVersion`), e não medida com N transações.
- O gás medido é o da publicação da raiz em cadeia. O processamento fora da cadeia
  (cálculo dos resumos e construção da árvore) não foi medido. Para N acima de 4.096, a
  raiz enviada foi calculada sobre 4.096 folhas, e o valor N foi informado ao contrato
  como contagem de folhas.

**Sessão do gateway** (`evidence/logs/gateway-session.log`): 17 requisições HTTP — uma
verificação de estado (numerada 0) seguida de 16 chamadas numeradas de 1 a 16. A sessão
registrou dois ativos, suas versões e um evento de proveniência; verificou o arquivo
intacto e o adulterado; registrou o conteúdo alterado como nova versão; ancorou 8
objetos em uma transação e verificou a inclusão de um deles e a não inclusão de um
objeto ausente; recebeu `HTTP 501` em `/v1/pids` e `HTTP 401` em chamada de escrita sem
credencial. Os arquivos não são enviados ao gateway; o cliente calcula o resumo
localmente e envia apenas o resumo.

## Gateway: rotas

| Método | Rota | Função |
|---|---|---|
| GET | `/v1/health` | Estado do serviço e endereços dos contratos |
| GET | `/v1/assets/{id}` | Ativo e histórico de versões |
| GET | `/v1/proofs/{batchId}/inclusion?leaf=…&proof=…` | Verificação de inclusão em lote |
| POST | `/v1/assets` | Registro de ativo |
| POST | `/v1/assets/{id}/versions` | Registro de versão a partir de resumo criptográfico |
| POST | `/v1/verify` | Verificação de integridade de um resumo |
| POST | `/v1/events` | Registro de evento de proveniência |
| POST | `/v1/proofs/batches` | Ancoragem de lote e emissão de recibos com caminho de inclusão |
| POST | `/v1/pids` | Cunhagem de identificador no dARK — **não implementada; responde 501** |

As rotas de escrita exigem o cabeçalho `Authorization: Bearer savits-poc-token`. Esse
valor é um marcador fixo de demonstração, não uma credencial, e não protege nada fora
do ambiente local.

## Limitações conhecidas

- Execução apenas em EVM local; vazão, latência e finalização em rede real não foram
  medidas.
- Sem cunhagem real no dARK; o vínculo de identificador foi testado com valor simulado.
- Sem custódia de chaves: o gateway assina com a primeira conta de teste do ambiente
  local.
- Autenticação do gateway por marcador fixo, adequada apenas à demonstração.
- Validação de entrada rudimentar no gateway.
- O identificador interno do ativo é derivado por `keccak256` do identificador de
  negócio, o que permite a quem conhece o identificador de negócio confirmar sua
  presença no registro.
- Contratos sem auditoria, análise estática, teste de perturbação aleatória ou
  verificação formal.

Referências a `docs/` presentes no código e nos registros de execução (por exemplo, na
resposta da rota `/v1/pids`) apontam para documentos analíticos que integram o relatório
técnico e não foram incluídos neste repositório. O texto do código e dos registros foi
mantido como executado.

## Licença

Os contratos em `contracts/contracts/` são distribuídos sob a GNU General Public License
v3.0, conforme o identificador SPDX de cada arquivo; o texto da licença está em
`LICENSES/GPL-3.0.txt`. O identificador foi mantido porque integra o código-fonte
compilado e, portanto, o bytecode ao qual se referem as medições registradas. Os demais
arquivos são distribuídos sob a licença MIT, conforme `LICENSE`.

## Citação

Os metadados de citação estão em `CITATION.cff`. Para referência ao estado exato dos
artefatos descritos no relatório técnico, cite a versão marcada `v0.1.0`.
