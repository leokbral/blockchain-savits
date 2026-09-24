#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sessao de demonstracao do IBICT Blockchain Gateway (PoC).
Sobe o gateway em thread e exercita a API por HTTP real, registrando
requisicao e resposta de cada chamada como evidencia.

Ciclo demonstrado: registro -> versao -> proveniencia -> consulta ->
verificacao -> alteracao do objeto -> deteccao -> nova versao -> historico
-> ancoragem em lote -> prova de inclusao.
"""
import json, os, sys, threading, time, hashlib, urllib.request, urllib.error
from http.server import HTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "poc", "backend"))
import gateway  # noqa: E402

PORT = 8899
BASE = f"http://127.0.0.1:{PORT}"
TOKEN = "Bearer savits-poc-token"
OUT = []


def log(s=""):
    print(s)
    OUT.append(str(s))


def call(method, path, body=None, token=True, titulo=""):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", TOKEN)
    log("")
    log("=" * 76)
    log(f"### {titulo}")
    log(f"{method} {path}" + ("" if token else "   (sem cabecalho Authorization)"))
    if body is not None:
        log("requisicao:")
        log(json.dumps(body, ensure_ascii=False, indent=1)[:900])
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            code, payload = r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        code, payload = e.code, e.read().decode()
    log(f"resposta: HTTP {code}")
    log(payload[:1400])
    return code, json.loads(payload)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return "0x" + h.hexdigest()


# --------------------------------------------------------------- servidor
srv = HTTPServer(("127.0.0.1", PORT), gateway.Handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
time.sleep(0.5)

W = os.path.join(ROOT, "experiments", "workdir")
DS = os.path.join(W, "dataset_politicas_v1.csv")
MD = os.path.join(W, "modelo_impacto_v1.bin")

log("#" * 76)
log("SESSAO DE DEMONSTRACAO — IBICT Blockchain Gateway (PoC v0.1)")
log("Projeto SAVITS / frente Blockchain-RBB · " + time.strftime("%d/%m/%Y %H:%M:%S"))
log("AMBIENTE: EVM local (eth-tester). NAO e a Rede Blockchain Brasil.")
log("#" * 76)

call("GET", "/v1/health", None, False, "0. Estado do servico")

call("POST", "/v1/assets", {"id": "savits:dataset:politicas", "tipo": "DATASET"},
     titulo="1. Registrar o conjunto de dados como ativo")
call("POST", "/v1/assets", {"id": "savits:model:impacto", "tipo": "MODEL"},
     titulo="2. Registrar o modelo como ativo")

d_ok = sha256(DS)
m_ok = sha256(MD)
log("")
log(f"[cliente] sha256 do dataset calculado localmente: {d_ok}")
log(f"[cliente] sha256 do modelo  calculado localmente: {m_ok}")
log("[cliente] os arquivos NAO sao enviados ao gateway — apenas o digest.")

_, v1 = call("POST", "/v1/assets/savits:dataset:politicas/versions",
             {"digest": d_ok, "algoritmo": "sha2-256",
              "metadados": {"titulo": "Indicadores de politicas sociais",
                            "licenca": "CC-BY-4.0", "linhas": 50}},
             titulo="3. Registrar a versao 0 do dataset")
call("POST", "/v1/assets/savits:model:impacto/versions",
     {"digest": m_ok, "algoritmo": "sha2-256", "metadados": {"tipo": "experimental"}},
     titulo="4. Registrar a versao 0 do modelo")

call("POST", "/v1/events",
     {"id": "savits:model:impacto", "versao": 0, "tipo": "TRAINED",
      "detalhe": "execucao de treino 2026-09-16", "origens": []},
     titulo="5. Registrar evento de proveniencia (modelo TREINADO)")

call("GET", "/v1/assets/savits:dataset:politicas", None, False,
     "6. Consultar o ativo e seu historico de versoes")

call("POST", "/v1/verify", {"id": "savits:dataset:politicas", "digest": d_ok},
     titulo="7. Verificar integridade — arquivo INTACTO")

# --------------------------------------------------- alteracao do objeto
orig = open(DS, encoding="utf-8").read()
alterado = orig.replace("0.510", "0.910", 1)
assert alterado != orig
open(DS, "w", encoding="utf-8").write(alterado)
d_bad = sha256(DS)
log("")
log("[cliente] ALTERACAO APLICADA ao arquivo: um valor de indicador foi trocado")
log(f"[cliente] digest antes  : {d_ok}")
log(f"[cliente] digest depois : {d_bad}")

call("POST", "/v1/verify", {"id": "savits:dataset:politicas", "digest": d_bad},
     titulo="8. Verificar integridade — arquivo ADULTERADO")

call("POST", "/v1/assets/savits:dataset:politicas/versions",
     {"digest": d_bad, "algoritmo": "sha2-256",
      "metadados": {"nota": "correcao de valor do indicador", "derivadaDe": 0}},
     titulo="9. Registrar o conteudo alterado como NOVA VERSAO")

call("GET", "/v1/assets/savits:dataset:politicas", None, False,
     "10. Consultar historico apos a nova versao")

call("POST", "/v1/verify", {"id": "savits:dataset:politicas", "digest": d_bad},
     titulo="11. Verificar novamente o arquivo alterado (agora e a versao 1)")

open(DS, "w", encoding="utf-8").write(orig)  # restaura o artefato original

# ------------------------------------------------- ancoragem em lote
folhas = [gateway.w3.keccak(text=f"acervo:objeto:{i:04d}").hex() for i in range(8)]
_, lote = call("POST", "/v1/proofs/batches", {"digests": ["0x" + f for f in folhas]},
               titulo="12. Ancorar 8 objetos em UMA transacao (arvore de Merkle)")
bid = lote["batchId"]
rec = lote["recibos"][3]
call("GET", f"/v1/proofs/{bid}/inclusion?leaf={rec['folha']}&proof={','.join(rec['caminho'])}",
     None, False, "13. Provar inclusao de um objeto do lote (recibo valido)")
call("GET", f"/v1/proofs/{bid}/inclusion?leaf=0x"
     + gateway.w3.keccak(text="objeto:que:nao:esta:no:lote").hex()
     + f"&proof={','.join(rec['caminho'])}",
     None, False, "14. Tentar provar inclusao de objeto ausente do lote")

call("POST", "/v1/pids", {"id": "savits:dataset:politicas"},
     titulo="15. Solicitar cunhagem de PID no dARK (dependencia externa)")
call("POST", "/v1/assets", {"id": "x", "tipo": "OTHER"}, token=False,
     titulo="16. Chamada sem token institucional")

log("")
log("=" * 76)
log("TRILHA DE AUDITORIA DO GATEWAY (registro interno de todas as chamadas)")
log("=" * 76)
for a in gateway.AUDIT:
    log(f"  {a['ts']}  {a['method']:<5} {a['path']:<62} -> {a['status']}")

log("")
log("Fim da sessao. Nenhum arquivo foi transmitido ao gateway em nenhum momento.")

os.makedirs(os.path.join(ROOT, "evidence", "logs"), exist_ok=True)
with open(os.path.join(ROOT, "evidence", "logs", "gateway-session.log"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(OUT))
srv.shutdown()
