#!/usr/bin/env bash
# Recompila os contratos, executa a suíte de testes e a sessão de demonstração.
# Ambiente: EVM local (eth-tester/py-evm). Não executa nada na Rede Blockchain Brasil.
# Regrava build/artifacts.json e evidence/; use "git diff" para comparar com o registrado.
set -euo pipefail
cd "$(dirname "$0")"

npm ci
node compile.js contracts/contracts build
python3 tests/run_tests.py
python3 poc/integration/demo_session.py
