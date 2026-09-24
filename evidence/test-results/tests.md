# Resultados de teste — execucao automatizada

Executado em 23/09/2026 11:27:52 · ambiente: EVM local (eth-tester/py-evm) · solc 0.8.26 · evmVersion paris

**Este ambiente nao e a RBB.** Nenhum teste foi executado contra a rede de producao ou de testes da Rede Blockchain Brasil.

| ID | Atividade | Teste | Resultado esperado | Resultado obtido | Status |
|---|---|---|---|---|---|
| T01 | A2 | Registrar ativo (dataset) | ativo passa a existir e evento AssetRegistered e emitido | `exists=True; evento emitido=True; gas=97165` | PASSOU |
| T14 | A2/2.3.2 | Vincular PID ao ativo | PID armazenado e recuperavel; evento PidBound emitido | `pid lido on-chain=ark:/00000/SIMULADO-ds-politicas; gas=74926` | PASSOU |
| T02 | A2 | Registrar hash/versao inicial | versao 0 criada e contador = 1 | `versionCount=1; gas=164029` | PASSOU |
| T03 | A2 | Registrar versao de modelo | modelo registrado com 1 versao | `versionCount(modelo)=1; gas=164029` | PASSOU |
| T04 | A2/A3 | Registrar evento de proveniencia | evento registrado com vinculo ao ativo de origem | `eventId=0; parents=1; tipo=3; gas=189112` | PASSOU |
| T05 | A2 | Consultar ativo | retorna existencia, tipo, registrante, carimbo, PID e n de versoes | `exists=True kind=0 createdAt=1790173675 pid=ark:/00000/SIMULADO-ds-politicas nVersions=1` | PASSOU |
| T06 | A2 | Verificar integridade — objeto intacto | found=True apontando para a versao 0 | `found=True index=0 timestamp=1790173677` | PASSOU |
| T07 | A2 | Alterar objeto off-chain | hash diferente do registrado | `hash original=580049719a81fa607a81… / hash alterado=458ad750328bb5e00637…` | PASSOU |
| T08 | A2 | Detectar alteracao | found=False — inconsistencia detectada | `found=False` | PASSOU |
| T09 | A2 | Registrar nova versao | versao 1 criada; o novo conteudo passa a verificar | `versionCount=2; verify(novo)=True index=1` | PASSOU |
| T10 | A2 | Consultar historico de versoes | duas versoes com hashes distintos e carimbos de tempo | `2 versoes: ['580049719a81', '458ad750328b']` | PASSOU |
| T11a | A3 | Certificar e revogar certificacao | status ACTIVE(1) e depois REVOKED(2) com revokedAt preenchido | `status inicial=1 -> final=2; revokedAt=1790173683` | PASSOU |
| T11b | A3 | Registrar e revogar consentimento | consentimento ativo e depois inativo, sem apagar o registro | `ativo apos registro=True; ativo apos revogacao=False` | PASSOU |
| T12 | A3 | Cenarios de erro e controle de acesso | todas revertem com mensagem explicita | `7/7 reverteram` | PASSOU |
| T13 | A1/A2 | Ancoragem em lote e prova de inclusao | inclusao verdadeira para a folha presente e falsa para a ausente | `presente=True; ausente=False; gas da ancoragem=93683` | PASSOU |

**15/15 testes passaram.**
