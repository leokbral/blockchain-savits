#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IBICT Blockchain Gateway — PROTOTIPO EXPERIMENTAL v0.1
Projeto SAVITS / frente Blockchain-RBB.

Expoe as primitivas de confianca por HTTP, de modo que sistemas institucionais
nao precisem conhecer blockchain, carteiras, chaves ou transacoes.

PRINCIPIO: o gateway NUNCA recebe o arquivo. Recebe apenas o resumo
criptografico calculado no cliente. Ver docs/architecture.md.

ATENCAO: esta instancia opera sobre EVM local (eth-tester). NAO e integracao
com a Rede Blockchain Brasil.
"""
import json, os, threading, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from web3 import Web3, EthereumTesterProvider

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = json.load(open(os.path.join(ROOT, "build", "artifacts.json")))

w3 = Web3(EthereumTesterProvider())
ACCT = w3.eth.accounts[0]
_lock = threading.Lock()

# --- chave institucional: nesta PoC e a conta 0 do ambiente de teste.
# Em producao seria custodiada em HSM e o gateway assinaria sem expor a chave.


def _deploy(name):
    a = ART[name]
    c = w3.eth.contract(abi=a["abi"], bytecode=a["bytecode"])
    r = w3.eth.wait_for_transaction_receipt(c.constructor().transact({"from": ACCT}))
    return w3.eth.contract(address=r.contractAddress, abi=a["abi"])


SAR = _deploy("SavitsAssetRegistry")
PA = _deploy("ProofAnchor")

KIND = {"DATASET": 0, "MODEL": 1, "PIPELINE": 2, "RESULT": 3, "DOCUMENT": 4, "OTHER": 5}
ETYPE = {"CREATED": 0, "INGESTED": 1, "PROCESSED": 2, "TRAINED": 3, "EVALUATED": 4,
         "DERIVED": 5, "PUBLISHED": 6, "DEPRECATED": 7, "OTHER": 8}

AUDIT = []  # trilha de auditoria do proprio gateway


def b32(h):
    h = h[2:] if h.startswith("0x") else h
    return bytes.fromhex(h)


def aid(external_id):
    """Deriva o identificador interno do ativo a partir do identificador de negocio."""
    return w3.keccak(text=external_id)


def merkle(leaves, index=None):
    level, proof, idx = list(leaves), [], index
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            if i + 1 < len(level):
                a, b = level[i], level[i + 1]
                if idx is not None and (i == idx or i + 1 == idx):
                    proof.append(b if idx == i else a)
                    idx = len(nxt)
                lo, hi = (a, b) if a <= b else (b, a)
                nxt.append(w3.keccak(lo + hi))
            else:
                if idx is not None and i == idx:
                    idx = len(nxt)
                nxt.append(level[i])
        level = nxt
    return level[0], proof


class Handler(BaseHTTPRequestHandler):
    server_version = "IbictBlockchainGateway/0.1-experimental"

    def log_message(self, *a):
        pass  # silencia log padrao; auditoria propria abaixo

    # ------------------------------------------------------------- utilidades
    def _send(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False, indent=1).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("X-Gateway-Environment", "LOCAL-EVM-NAO-E-RBB")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        AUDIT.append({"ts": time.strftime("%H:%M:%S"), "method": self.command,
                      "path": self.path, "status": code})

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def _auth(self):
        """Autenticacao institucional por token (PoC: token fixo)."""
        return self.headers.get("Authorization") == "Bearer savits-poc-token"

    # ------------------------------------------------------------------- GET
    def do_GET(self):
        u = urlparse(self.path)
        p = [x for x in u.path.split("/") if x]
        try:
            if u.path == "/v1/health":
                return self._send(200, {
                    "status": "ok", "ambiente": "EVM local (eth-tester) — NAO e a RBB",
                    "registry": SAR.address, "anchor": PA.address,
                    "bloco": w3.eth.block_number})

            if len(p) == 3 and p[:2] == ["v1", "assets"]:
                a = SAR.functions.getAsset(aid(p[2])).call()
                if not a[0]:
                    return self._send(404, {"erro": "ativo nao encontrado", "id": p[2]})
                versoes = []
                for i in range(a[5]):
                    v = SAR.functions.getVersion(aid(p[2]), i).call()
                    versoes.append({"versao": i, "contentHash": "0x" + v[0].hex(),
                                    "algoritmo": v[1].decode().rstrip("\x00"),
                                    "timestamp": v[3], "registrar": v[4]})
                return self._send(200, {
                    "id": p[2], "assetId": "0x" + aid(p[2]).hex(),
                    "tipo": [k for k, vv in KIND.items() if vv == a[1]][0],
                    "pid": a[4] or None, "criadoEm": a[3], "versoes": versoes})

            if len(p) == 4 and p[:2] == ["v1", "proofs"] and p[3] == "inclusion":
                q = parse_qs(u.query)
                leaf = b32(q["leaf"][0])
                proof = [b32(x) for x in q.get("proof", [""])[0].split(",") if x]
                ok = PA.functions.verifyInclusion(int(p[2]), leaf, proof).call()
                b = PA.functions.getBatch(int(p[2])).call()
                return self._send(200, {"batchId": int(p[2]), "incluido": ok,
                                        "raiz": "0x" + b[0].hex(), "folhas": b[1],
                                        "ancoradoEm": b[2]})
            return self._send(404, {"erro": "rota inexistente"})
        except Exception as e:
            return self._send(400, {"erro": type(e).__name__, "detalhe": str(e)[:300]})

    # ------------------------------------------------------------------ POST
    def do_POST(self):
        if not self._auth():
            return self._send(401, {"erro": "token institucional ausente ou invalido"})
        u = urlparse(self.path)
        try:
            d = self._body()
            with _lock:
                if u.path == "/v1/assets":
                    a = aid(d["id"])
                    if SAR.functions.getAsset(a).call()[0]:
                        return self._send(409, {"erro": "ativo ja registrado", "id": d["id"]})
                    r = w3.eth.wait_for_transaction_receipt(
                        SAR.functions.registerAsset(a, KIND[d["tipo"]], d.get("pid", ""))
                        .transact({"from": ACCT}))
                    return self._send(201, {"id": d["id"], "assetId": "0x" + a.hex(),
                                            "tx": r.transactionHash.hex(), "gas": r.gasUsed,
                                            "bloco": r.blockNumber})

                if u.path.startswith("/v1/assets/") and u.path.endswith("/versions"):
                    ext = u.path.split("/")[3]
                    r = w3.eth.wait_for_transaction_receipt(
                        SAR.functions.registerVersion(
                            aid(ext), b32(d["digest"]),
                            d.get("algoritmo", "sha2-256").encode()[:8].ljust(8, b"\x00"),
                            w3.keccak(text=json.dumps(d.get("metadados", {}), sort_keys=True)))
                        .transact({"from": ACCT}))
                    idxs = SAR.events.VersionRegistered().process_receipt(r)
                    return self._send(201, {
                        "id": ext, "versao": idxs[0]["args"]["versionIndex"],
                        "digest": d["digest"], "tx": r.transactionHash.hex(), "gas": r.gasUsed,
                        "aviso": "registro em EVM local; nao ancorado na RBB"})

                if u.path == "/v1/verify":
                    found, idx, ts = SAR.functions.verifyAsset(
                        aid(d["id"]), b32(d["digest"])).call()
                    return self._send(200, {
                        "id": d["id"], "digest": d["digest"], "integro": found,
                        "versao": idx if found else None,
                        "registradoEm": ts if found else None,
                        "conclusao": ("digest confere com versao registrada" if found
                                      else "digest NAO corresponde a nenhuma versao registrada")})

                if u.path == "/v1/events":
                    parents = [b32(x) for x in d.get("origens", [])]
                    r = w3.eth.wait_for_transaction_receipt(
                        SAR.functions.registerEvent(
                            aid(d["id"]), d["versao"], ETYPE[d["tipo"]],
                            w3.keccak(text=d.get("detalhe", "")), parents)
                        .transact({"from": ACCT}))
                    eid = SAR.events.ProvenanceRecorded().process_receipt(r)[0]["args"]["eventId"]
                    return self._send(201, {"eventId": eid, "tipo": d["tipo"],
                                            "origens": len(parents), "gas": r.gasUsed})

                if u.path == "/v1/proofs/batches":
                    folhas = [b32(x) for x in d["digests"]]
                    raiz, _ = merkle(folhas)
                    r = w3.eth.wait_for_transaction_receipt(
                        PA.functions.anchorBatch(raiz, len(folhas)).transact({"from": ACCT}))
                    bid = PA.events.BatchAnchored().process_receipt(r)[0]["args"]["batchId"]
                    recibos = []
                    for i, f in enumerate(folhas):
                        _, pr = merkle(folhas, i)
                        recibos.append({"folha": "0x" + f.hex(),
                                        "caminho": ["0x" + x.hex() for x in pr]})
                    return self._send(201, {"batchId": bid, "raiz": "0x" + raiz.hex(),
                                            "folhas": len(folhas), "gas": r.gasUsed,
                                            "recibos": recibos})

                if u.path == "/v1/pids":
                    # O gateway NAO cunha PID: delega ao dARK. Sem credenciais, devolve 501.
                    return self._send(501, {
                        "erro": "cunhagem de PID nao implementada nesta PoC",
                        "motivo": "sem credenciais de acesso ao dARK/Hyperdrive",
                        "encaminhamento": "ver docs/INFORMACOES-NECESSARIAS.md, item 1"})
            return self._send(404, {"erro": "rota inexistente"})
        except Exception as e:
            return self._send(400, {"erro": type(e).__name__, "detalhe": str(e)[:300]})


def serve(port=8899):
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    import sys
    serve(int(sys.argv[1]) if len(sys.argv) > 1 else 8899)
