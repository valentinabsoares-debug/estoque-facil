#!/usr/bin/env bash
# Simula localmente um deploy que falha e o rollback automático (evidência da entrega).
# Uso: scripts/simulate-rollback.sh   (precisa de Docker; gera docs/evidencias/rollback-log.txt)
#
#  1) builda a imagem real como 1.0.0 (versão "boa")
#  2) cria a 1.0.1 como cópia quebrada (container sai com erro logo ao iniciar)
#  3) roda o deploy da 1.0.1 tendo 1.0.0 como anterior -> falha -> rollback para 1.0.0
set -euo pipefail
cd "$(dirname "$0")/.."

export IMAGE_NAME="sgctechfix-local"
export PULL_POLICY="never"
export DB_USER="${DB_USER:-sgc_user}"
export DB_PASSWORD="${DB_PASSWORD:-senha-local-simulacao}"
export JWT_SECRET="${JWT_SECRET:-segredo-local-simulacao}"
export HEALTH_TIMEOUT_S=40

mkdir -p docs/evidencias
LOG=docs/evidencias/rollback-log.txt

{
  echo "== Simulação de rollback - $(date -u +%Y-%m-%dT%H:%M:%SZ) =="
  echo "== 1) Build da versão boa 1.0.0"
  docker build -t "$IMAGE_NAME:1.0.0" --build-arg APP_VERSION=1.0.0 .

  echo "== 2) Criando versão quebrada 1.0.1"
  printf 'FROM %s:1.0.0\nENTRYPOINT ["sh","-c","echo ERRO simulado na 1.0.1; sleep 2; exit 1"]\n' "$IMAGE_NAME" \
    | docker build -t "$IMAGE_NAME:1.0.1" -

  echo "== 3) Deploy da 1.0.1 (anterior: 1.0.0)"
  set +e
  ./scripts/deploy.sh 1.0.1 1.0.0
  RC=$?
  set -e
  echo "== deploy.sh terminou com código $RC (esperado: 1 = falha detectada)"

  echo "== 4) Versão rodando após o rollback:"
  docker inspect -f '{{.Config.Image}} -> {{.State.Health.Status}}' sgctechfix-app
} 2>&1 | tee "$LOG"

docker compose down -v >/dev/null 2>&1 || true
echo "Log salvo em $LOG"
