#!/usr/bin/env bash
# Deploy com health check e rollback automático.
# Uso: scripts/deploy.sh <versao-nova> [versao-anterior]
# Requer: IMAGE_NAME, DB_USER, DB_PASSWORD, JWT_SECRET no ambiente (vêm dos Secrets do CI).
# PULL_POLICY=always (padrão) ou never (simulação local com imagens locais).
set -euo pipefail

NEW="${1:?uso: deploy.sh <versao-nova> [versao-anterior]}"
PREV="${2:-}"
export PULL_POLICY="${PULL_POLICY:-always}"
CONTAINER="sgctechfix-app"
TIMEOUT_S="${HEALTH_TIMEOUT_S:-120}"

up() { # sobe a stack na versão $1
  APP_VERSION="$1" docker compose up -d --no-build --pull "$PULL_POLICY" --force-recreate
}

wait_healthy() { # espera o healthcheck do container ficar "healthy"
  local waited=0 status
  while (( waited < TIMEOUT_S )); do
    status=$(docker inspect -f '{{.State.Health.Status}}' "$CONTAINER" 2>/dev/null || echo "ausente")
    [[ "$status" == "healthy" ]] && return 0
    [[ "$status" == "unhealthy" ]] && return 1
    sleep 3; waited=$((waited + 3))
  done
  return 1
}

# Baseline: garante que a versão anterior (estável) está no ar antes de trocar.
if [[ -n "$PREV" ]]; then
  echo ">> Baseline: subindo versão anterior $PREV"
  if up "$PREV" && wait_healthy; then
    echo ">> Baseline $PREV saudável"
  else
    echo "!! Não foi possível subir a versão anterior $PREV; seguindo sem rollback disponível"
    PREV=""
  fi
fi

echo ">> Deploy da versão $NEW"
if up "$NEW" && wait_healthy; then
  echo ">> OK: $NEW saudável em homologação"
  exit 0
fi

echo "!! FALHA: $NEW não ficou saudável"
docker compose logs --tail=50 app || true

if [[ -n "$PREV" ]]; then
  echo ">> ROLLBACK para $PREV"
  up "$PREV"
  if wait_healthy; then
    echo ">> Rollback concluído: $PREV de volta ao ar"
  else
    echo "!! Rollback também falhou, intervenção manual necessária"
  fi
else
  echo "!! Sem versão anterior para rollback"
fi
exit 1 # o job fica vermelho mesmo com rollback bem-sucedido
