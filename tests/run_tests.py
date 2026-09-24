#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite de testes experimentais — SavitsAssetRegistry e ProofAnchor.
Ambiente: EVM local (eth-tester/py-evm). NAO e integracao com a RBB.
Gera evidencias em evidence/.
"""
import json, os, hashlib, time, csv, sys
from web3 import Web3, EthereumTesterProvider

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = os.path.join(ROOT, "evidence")
os.makedirs(os.path.join(EV, "test-results"), exist_ok=True)
os.makedirs(os.path.join(EV, "logs"), exist_ok=True)
os.makedirs(os.path.join(EV, "examples"), exist_ok=True)

LOG = []


def log(msg=""):
    print(msg)
    LOG.append(str(msg))


RESULTS = []


def record(tid, activity, name, entrada, procedimento, esperado, obtido, ok, evidencia=""):
    RESULTS.append(
        dict(id=tid, atividade=activity, teste=name, entrada=entrada, procedimento=procedimento,
             resultado_esperado=esperado, resultado_obtido=obtido,
             status="PASSOU" if ok else "FALHOU", evidencia=evidencia))
    log(f"[{tid}] {'PASSOU' if ok else 'FALHOU'}  {name}")
    log(f"       esperado: {esperado}")
    log(f"       obtido  : {obtido}")


# ------------------------------------------------------------------ utilidades
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def b32(hexstr):
    return bytes.fromhex(hexstr[2:] if hexstr.startswith("0x") else hexstr)


def merkle_root_and_proof(w3, leaves, index):
    """Arvore de Merkle com pares ordenados; no impar e promovido."""
    level = list(leaves)
    proof = []
    idx = index
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            if i + 1 < len(level):
                a, b = level[i], level[i + 1]
                if i == idx or i + 1 == idx:
                    proof.append(b if idx == i else a)
                    idx = len(nxt)
                lo, hi = (a, b) if a <= b else (b, a)
                nxt.append(w3.keccak(lo + hi))
            else:
                if i == idx:
                    idx = len(nxt)
                nxt.append(level[i])
        level = nxt
    return level[0], proof


# ------------------------------------------------------------------- ambiente
log("=" * 78)
log("EXECUCAO DE TESTES — frente Blockchain/RBB — projeto SAVITS/IBICT")
log("Ambiente: EVM local (eth-tester/py-evm). NAO representa integracao com a RBB.")
log("Data/hora da execucao: " + time.strftime("%d/%m/%Y %H:%M:%S"))
log("=" * 78)

w3 = Web3(EthereumTesterProvider())
ADMIN, CURADOR, CERTIFICADOR, INTRUSO = w3.eth.accounts[:4]
ART = json.load(open(os.path.join(ROOT, "build", "artifacts.json")))


def deploy(name, sender=ADMIN):
    a = ART[name]
    c = w3.eth.contract(abi=a["abi"], bytecode=a["bytecode"])
    r = w3.eth.wait_for_transaction_receipt(c.constructor().transact({"from": sender}))
    log(f"deploy {name}: {r.contractAddress}  gas={r.gasUsed}")
    return w3.eth.contract(address=r.contractAddress, abi=a["abi"]), r.gasUsed


sar, gas_sar = deploy("SavitsAssetRegistry")
pa, gas_pa = deploy("ProofAnchor")
log("")

ROLE_REGISTRAR, ROLE_CERTIFIER, ROLE_CONSENT = 2, 4, 8
w3.eth.wait_for_transaction_receipt(
    sar.functions.setRole(CURADOR, ROLE_REGISTRAR | ROLE_CONSENT).transact({"from": ADMIN}))
w3.eth.wait_for_transaction_receipt(
    sar.functions.setRole(CERTIFICADOR, ROLE_CERTIFIER).transact({"from": ADMIN}))

GAS = {"deploy_SavitsAssetRegistry": gas_sar, "deploy_ProofAnchor": gas_pa}


def tx(fn, sender, label=None):
    r = w3.eth.wait_for_transaction_receipt(fn.transact({"from": sender}))
    if label:
        GAS[label] = r.gasUsed
    return r


# ----------------------------------------------------------- artefatos de teste
WORK = os.path.join(ROOT, "experiments", "workdir")
os.makedirs(WORK, exist_ok=True)
ds_path = os.path.join(WORK, "dataset_politicas_v1.csv")
with open(ds_path, "w", encoding="utf-8") as f:
    f.write("id_politica,municipio,ano,indicador,valor\n")
    for i in range(1, 51):
        f.write(f"P{i:03d},MUN{i % 7},2025,idh_educacao,{0.5 + (i % 30) / 100:.3f}\n")
model_path = os.path.join(WORK, "modelo_impacto_v1.bin")
with open(model_path, "wb") as f:
    f.write(b"MODELO-SAVITS-EXPERIMENTAL\n" + bytes(range(256)) * 40)

DS_ID = w3.keccak(text="savits:dataset:politicas-sociais")
MD_ID = w3.keccak(text="savits:model:impacto-idh-educacao")
KIND_DATASET, KIND_MODEL = 0, 1
ALGO = b"sha2-256"

# ================================================================= ATIVIDADE 2/3
log("-" * 78)
log("T01 — Registrar ativo")
r = tx(sar.functions.registerAsset(DS_ID, KIND_DATASET, ""), CURADOR, "registerAsset")
ev = sar.events.AssetRegistered().process_receipt(r)
exists = sar.functions.getAsset(DS_ID).call()[0]
record("T01", "A2", "Registrar ativo (dataset)",
       f"assetId={DS_ID.hex()[:18]}… kind=DATASET", "registerAsset() por conta com papel REGISTRAR",
       "ativo passa a existir e evento AssetRegistered e emitido",
       f"exists={exists}; evento emitido={len(ev) == 1}; gas={r.gasUsed}", exists and len(ev) == 1,
       "evidence/logs/execution.log")

log("-" * 78)
log("T14 — Vincular PID externo (dARK) ao ativo")
PID_SIM = "ark:/00000/SIMULADO-ds-politicas"  # SIMULADO: sem acesso ao dARK
r = tx(sar.functions.bindPid(DS_ID, PID_SIM), CURADOR, "bindPid")
pid_on = sar.functions.getAsset(DS_ID).call()[4]
record("T14", "A2/2.3.2", "Vincular PID ao ativo",
       f"pid={PID_SIM}", "bindPid(); PID cunhado fora do contrato",
       "PID armazenado e recuperavel; evento PidBound emitido",
       f"pid lido on-chain={pid_on}; gas={r.gasUsed}", pid_on == PID_SIM,
       "PID SIMULADO — nao houve cunhagem real no dARK (sem credenciais)")

log("-" * 78)
log("T02 — Registrar hash de conteudo (versao 0)")
h_ds_v1 = sha256_file(ds_path)
r = tx(sar.functions.registerVersion(DS_ID, b32(h_ds_v1), ALGO, w3.keccak(text="meta:ds:v1")),
       CURADOR, "registerVersion")
n = sar.functions.versionCount(DS_ID).call()
record("T02", "A2", "Registrar hash/versao inicial",
       f"sha256(dataset)={h_ds_v1[:24]}…", "registerVersion() com algoritmo sha2-256",
       "versao 0 criada e contador = 1",
       f"versionCount={n}; gas={r.gasUsed}", n == 1, f"arquivo: {os.path.relpath(ds_path, ROOT)}")

log("-" * 78)
log("T03 — Registrar nova versao (segundo ativo: modelo)")
tx(sar.functions.registerAsset(MD_ID, KIND_MODEL, "ark:/00000/SIMULADO-model-impacto"), CURADOR)
h_md_v1 = sha256_file(model_path)
r = tx(sar.functions.registerVersion(MD_ID, b32(h_md_v1), ALGO, w3.keccak(text="meta:model:v1")), CURADOR)
nm = sar.functions.versionCount(MD_ID).call()
record("T03", "A2", "Registrar versao de modelo",
       f"sha256(modelo)={h_md_v1[:24]}…", "registerAsset()+registerVersion() para o modelo",
       "modelo registrado com 1 versao",
       f"versionCount(modelo)={nm}; gas={r.gasUsed}", nm == 1)

log("-" * 78)
log("T04 — Registrar evento de proveniencia (dataset -> modelo)")
ref_ds_v0 = sar.functions.versionRef(DS_ID, 0).call()
EV_TRAINED = 3
r = tx(sar.functions.registerEvent(MD_ID, 0, EV_TRAINED, w3.keccak(text="run:treino:2026-09-16"),
                                   [ref_ds_v0]), CURADOR, "registerEvent")
eid = sar.events.ProvenanceRecorded().process_receipt(r)[0]["args"]["eventId"]
evd = sar.functions.getEvent(eid).call()
record("T04", "A2/A3", "Registrar evento de proveniencia",
       "modelo v0 TRAINED a partir de dataset v0", "registerEvent() com parents=[versionRef(dataset,0)]",
       "evento registrado com vinculo ao ativo de origem",
       f"eventId={eid}; parents={len(evd[4])}; tipo={evd[2]}; gas={r.gasUsed}",
       len(evd[4]) == 1 and evd[4][0] == ref_ds_v0)

log("-" * 78)
log("T05 — Consultar ativo")
a = sar.functions.getAsset(DS_ID).call()
record("T05", "A2", "Consultar ativo",
       f"assetId={DS_ID.hex()[:18]}…", "getAsset()",
       "retorna existencia, tipo, registrante, carimbo, PID e n de versoes",
       f"exists={a[0]} kind={a[1]} createdAt={a[3]} pid={a[4]} nVersions={a[5]}", a[0] and a[5] == 1)

log("-" * 78)
log("T06 — Verificar integridade (objeto intacto)")
found, idx, ts = sar.functions.verifyAsset(DS_ID, b32(sha256_file(ds_path))).call()
record("T06", "A2", "Verificar integridade — objeto intacto",
       f"hash recalculado do arquivo original", "verifyAsset(assetId, sha256(arquivo))",
       "found=True apontando para a versao 0",
       f"found={found} index={idx} timestamp={ts}", found and idx == 0)

log("-" * 78)
log("T07/T08 — Alterar objeto e detectar alteracao")
with open(ds_path, "r", encoding="utf-8") as f:
    original = f.read()
adulterado = original.replace("P001,MUN1,2025,idh_educacao,0.510", "P001,MUN1,2025,idh_educacao,0.910")
if adulterado == original:  # garante alteracao de 1 caractere
    adulterado = original[:-2] + "9\n"
with open(ds_path, "w", encoding="utf-8") as f:
    f.write(adulterado)
h_ds_alt = sha256_file(ds_path)
found2, idx2, _ = sar.functions.verifyAsset(DS_ID, b32(h_ds_alt)).call()
record("T07", "A2", "Alterar objeto off-chain",
       "alteracao minima no CSV", "reescrita do arquivo e novo sha256",
       "hash diferente do registrado",
       f"hash original={h_ds_v1[:20]}… / hash alterado={h_ds_alt[:20]}…", h_ds_alt != h_ds_v1,
       f"arquivo: {os.path.relpath(ds_path, ROOT)}")
record("T08", "A2", "Detectar alteracao",
       f"sha256(arquivo alterado)={h_ds_alt[:20]}…", "verifyAsset() com o novo hash",
       "found=False — inconsistencia detectada",
       f"found={found2}", found2 is False)

log("-" * 78)
log("T09 — Registrar nova versao do objeto alterado")
r = tx(sar.functions.registerVersion(DS_ID, b32(h_ds_alt), ALGO, w3.keccak(text="meta:ds:v2")), CURADOR)
n2 = sar.functions.versionCount(DS_ID).call()
f3, i3, _ = sar.functions.verifyAsset(DS_ID, b32(h_ds_alt)).call()
record("T09", "A2", "Registrar nova versao",
       f"novo hash={h_ds_alt[:20]}…", "registerVersion() para o conteudo alterado",
       "versao 1 criada; o novo conteudo passa a verificar",
       f"versionCount={n2}; verify(novo)={f3} index={i3}", n2 == 2 and f3 and i3 == 1)

log("-" * 78)
log("T10 — Consultar historico")
hist = []
for i in range(sar.functions.versionCount(DS_ID).call()):
    v = sar.functions.getVersion(DS_ID, i).call()
    hist.append({"versao": i, "contentHash": v[0].hex(), "algo": v[1].decode().rstrip("\x00"),
                 "timestamp": v[3], "registrar": v[4]})
record("T10", "A2", "Consultar historico de versoes",
       f"assetId={DS_ID.hex()[:18]}…", "iteracao sobre getVersion()",
       "duas versoes com hashes distintos e carimbos de tempo",
       f"{len(hist)} versoes: {[h['contentHash'][:12] for h in hist]}", len(hist) == 2,
       "evidence/examples/historico_dataset.json")
json.dump(hist, open(os.path.join(EV, "examples", "historico_dataset.json"), "w"), indent=1)

log("-" * 78)
log("T11 — Comportamento do contrato: certificacao e consentimento")
ref_md_v0 = sar.functions.versionRef(MD_ID, 0).call()
r = tx(sar.functions.certify(ref_md_v0, w3.keccak(text="parecer:tecnico:001")), CERTIFICADOR, "certify")
cid = sar.events.Certified().process_receipt(r)[0]["args"]["certId"]
c1 = sar.functions.getCertification(cid).call()
tx(sar.functions.revokeCertification(cid, w3.keccak(text="motivo:erro-metrica")), CERTIFICADOR,
   "revokeCertification")
c2 = sar.functions.getCertification(cid).call()
ok_cert = c1[5] == 1 and c2[5] == 2 and c2[4] > 0
record("T11a", "A3", "Certificar e revogar certificacao",
       f"versionRef(modelo,0)={ref_md_v0.hex()[:18]}…", "certify() e depois revokeCertification()",
       "status ACTIVE(1) e depois REVOKED(2) com revokedAt preenchido",
       f"status inicial={c1[5]} -> final={c2[5]}; revokedAt={c2[4]}", ok_cert)

CONSENT_ID = w3.keccak(text="consent:0001")
SUBJECT_REF = w3.keccak(text="HMAC(chave_off_chain, titular_0001)")  # pseudonimo
tx(sar.functions.registerConsent(CONSENT_ID, SUBJECT_REF, w3.keccak(text="termo:v1"),
                                 w3.keccak(text="escopo:pesquisa-avaliacao-impacto")), CURADOR,
   "registerConsent")
ativo1 = sar.functions.isConsentActive(CONSENT_ID).call()
tx(sar.functions.revokeConsent(CONSENT_ID, w3.keccak(text="motivo:solicitacao-titular")), CURADOR,
   "revokeConsent")
ativo2 = sar.functions.isConsentActive(CONSENT_ID).call()
record("T11b", "A3", "Registrar e revogar consentimento",
       "consentId + subjectRef pseudonimizado + hash do termo + hash do escopo",
       "registerConsent() e depois revokeConsent()",
       "consentimento ativo e depois inativo, sem apagar o registro",
       f"ativo apos registro={ativo1}; ativo apos revogacao={ativo2}", ativo1 and not ativo2,
       "revogacao e mudanca de estado, nao eliminacao — ver docs/lgpd-analysis.md")

log("-" * 78)
log("T12 — Cenarios de erro")
erros = []


def espera_falha(desc, fn, sender):
    try:
        w3.eth.wait_for_transaction_receipt(fn.transact({"from": sender}))
        erros.append((desc, "NAO REVERTEU", False))
    except Exception as e:
        msg = str(e)
        m = msg.split("revert")[-1].strip()[:70] if "revert" in msg else msg[:70]
        erros.append((desc, m, True))


espera_falha("conta sem papel tenta registrar ativo",
             sar.functions.registerAsset(w3.keccak(text="x"), 0, ""), INTRUSO)
espera_falha("registrar ativo ja existente", sar.functions.registerAsset(DS_ID, 0, ""), CURADOR)
espera_falha("registrar conteudo duplicado no mesmo ativo",
             sar.functions.registerVersion(DS_ID, b32(h_ds_alt), ALGO, b"\x00" * 32), CURADOR)
espera_falha("evento sobre versao inexistente",
             sar.functions.registerEvent(DS_ID, 99, 0, b"\x00" * 32, []), CURADOR)
espera_falha("revogar certificacao ja revogada",
             sar.functions.revokeCertification(cid, b"\x00" * 32), CERTIFICADOR)
espera_falha("terceiro tenta revogar certificacao alheia",
             sar.functions.revokeCertification(0, b"\x00" * 32), CURADOR)
espera_falha("revogar consentimento ja revogado",
             sar.functions.revokeConsent(CONSENT_ID, b"\x00" * 32), CURADOR)
for d, m, ok in erros:
    log(f"       - {d}: {'revertido' if ok else 'NAO REVERTEU'} ({m})")
record("T12", "A3", "Cenarios de erro e controle de acesso",
       "7 chamadas invalidas", "cada chamada deve reverter",
       "todas revertem com mensagem explicita",
       f"{sum(1 for _, _, o in erros if o)}/7 reverteram", all(o for _, _, o in erros),
       "; ".join(d for d, _, _ in erros))

log("-" * 78)
log("T13 — Ancoragem em lote (Merkle) e prova de inclusao")
folhas = [w3.keccak(text=f"objeto-acervo-{i:05d}") for i in range(1000)]
alvo = 777
raiz, prova = merkle_root_and_proof(w3, folhas, alvo)
r = tx(pa.functions.anchorBatch(raiz, len(folhas)), ADMIN, "anchorBatch_1000")
bid = pa.events.BatchAnchored().process_receipt(r)[0]["args"]["batchId"]
ok_in = pa.functions.verifyInclusion(bid, folhas[alvo], prova).call()
ok_out = pa.functions.verifyInclusion(bid, w3.keccak(text="objeto-que-nao-esta-no-lote"), prova).call()
record("T13", "A1/A2", "Ancoragem em lote e prova de inclusao",
       f"1000 folhas, raiz={raiz.hex()[:18]}…, prova de {len(prova)} niveis",
       "anchorBatch() e verifyInclusion() para folha presente e ausente",
       "inclusao verdadeira para a folha presente e falsa para a ausente",
       f"presente={ok_in}; ausente={ok_out}; gas da ancoragem={r.gasUsed}", ok_in and not ok_out)

# =============================================== EXPERIMENTO: custo e escala
log("")
log("=" * 78)
log("EXPERIMENTO E2 — custo comparado: registro individual vs ancoragem em lote")
log("=" * 78)
g_individual = GAS["registerVersion"]
linhas = [("N objetos", "gas registro individual (N x registerVersion)", "gas ancoragem em lote (1 tx)",
           "reducao")]
bench = []
for N in [1, 10, 100, 1000, 10000, 100000]:
    folhas_n = [w3.keccak(text=f"obj-{i}") for i in range(min(N, 4096))]
    raiz_n, _ = merkle_root_and_proof(w3, folhas_n, 0)
    rr = w3.eth.wait_for_transaction_receipt(
        pa.functions.anchorBatch(raiz_n, min(N, 4294967295)).transact({"from": ADMIN}))
    tot = g_individual * N
    red = tot / rr.gasUsed
    bench.append(dict(n=N, gas_individual=tot, gas_lote=rr.gasUsed, reducao=round(red, 1)))
    linhas.append((str(N), f"{tot:,}", f"{rr.gasUsed:,}", f"{red:,.0f}x"))
    log(f"  N={N:>6}  individual={tot:>12,}  lote={rr.gasUsed:>8,}  reducao={red:>10,.0f}x")

with open(os.path.join(EV, "test-results", "gas-benchmark.csv"), "w", newline="") as f:
    wcsv = csv.writer(f)
    wcsv.writerow(["n_objetos", "gas_registro_individual", "gas_ancoragem_lote", "fator_reducao"])
    for b in bench:
        wcsv.writerow([b["n"], b["gas_individual"], b["gas_lote"], b["reducao"]])

log("")
log("Custo por operacao (gas medido nesta execucao):")
for k, v in sorted(GAS.items(), key=lambda x: -x[1]):
    log(f"  {k:<32} {v:>10,}")

# --------------------------------------------------------------------- saidas
passou = sum(1 for r_ in RESULTS if r_["status"] == "PASSOU")
log("")
log("=" * 78)
log(f"RESULTADO: {passou}/{len(RESULTS)} testes passaram")
log("=" * 78)

json.dump({"executado_em": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "ambiente": "EVM local (eth-tester/py-evm) — NAO e a RBB",
           "solc": "0.8.26", "evmVersion": "paris",
           "testes": RESULTS, "gas": GAS, "benchmark": bench},
          open(os.path.join(EV, "test-results", "tests.json"), "w"), indent=1, ensure_ascii=False)

with open(os.path.join(EV, "logs", "execution.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(LOG))

# tabela markdown dos testes
with open(os.path.join(EV, "test-results", "tests.md"), "w", encoding="utf-8") as f:
    f.write("# Resultados de teste — execucao automatizada\n\n")
    f.write(f"Executado em {time.strftime('%d/%m/%Y %H:%M:%S')} · ambiente: EVM local "
            "(eth-tester/py-evm) · solc 0.8.26 · evmVersion paris\n\n")
    f.write("**Este ambiente nao e a RBB.** Nenhum teste foi executado contra a rede de "
            "producao ou de testes da Rede Blockchain Brasil.\n\n")
    f.write("| ID | Atividade | Teste | Resultado esperado | Resultado obtido | Status |\n")
    f.write("|---|---|---|---|---|---|\n")
    for r_ in RESULTS:
        f.write(f"| {r_['id']} | {r_['atividade']} | {r_['teste']} | {r_['resultado_esperado']} | "
                f"`{r_['resultado_obtido']}` | {r_['status']} |\n")
    f.write(f"\n**{passou}/{len(RESULTS)} testes passaram.**\n")

sys.exit(0 if passou == len(RESULTS) else 1)
