#!/usr/bin/env bash
# Rollback manual para uma versão publicada. Uso: scripts/rollback.sh <versao>
set -euo pipefail

VERSION="${1:?uso: rollback.sh <versao>  (ex: 1.0.0)}"
PULL_POLICY="${PULL_POLICY:-always}"

echo ">> Rollback para $VERSION"
APP_VERSION="$VERSION" docker compose up -d --no-build --pull "$PULL_POLICY" --force-recreate app

for _ in $(seq 1 40); do
  status=$(docker inspect -f '{{.State.Health.Status}}' sgctechfix-app 2>/dev/null || echo "ausente")
  if [[ "$status" == "healthy" ]]; then
    echo ">> Rollback concluído: $VERSION saudável"
    exit 0
  fi
  sleep 3
done

echo "!! $VERSION não ficou saudável"
exit 1
