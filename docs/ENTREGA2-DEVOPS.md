# Entrega 2 – Containerização, CD, Segredos e Rollback

## 1. Dockerfile
`Dockerfile` multi-stage na raiz:
- **build**: `maven:3.9-eclipse-temurin-17`, com cache das dependências (o `pom.xml` é copiado antes do `src`).
- **runtime**: `eclipse-temurin:17-jre-alpine`, usuário não-root, `HEALTHCHECK` na porta 8080, modo `headless` (o projeto tem pacote `swing`).

```bash
docker build -t sgctechfix:dev .
```

## 2. Orquestração local (Docker Compose)
`docker-compose.yml` sobe **app + PostgreSQL**. O banco só inicia a aplicação depois de saudável (`depends_on: service_healthy`) e executa `sql/script_criação.sql` na primeira criação do volume.

```bash
cp .env.example .env      # preencher valores
docker compose up -d --build
docker compose logs -f app
docker compose down -v
```

## 3. Pipeline de CD (`.github/workflows/ci-cd.yml`)
| Evento | O que acontece |
|---|---|
| Pull request | build + testes (`mvn verify`) |
| Push na `main` | build + testes → publica imagem no **GHCR** (`sha-xxxxxxx`) → deploy em **homologação** |
| Tag `vX.Y.Z` | idem, com imagem `X.Y.Z`, `X.Y`, `latest` → deploy → **GitHub Release** |
| Manual | `Run workflow` com `rollback_version` → rollback em homologação |

O ambiente de homologação é **simulado** no runner do GitHub Actions: o job sobe a stack com `docker compose`, espera o health check e valida a versão.

## 4. Segredos e configuração
Nenhuma senha está no código-fonte.
- `GITHUB_TOKEN` (automático): login no GHCR.
- **Environment `homologacao`** (Settings → Environments → homologacao → Secrets): `DB_USER`, `DB_PASSWORD`, `JWT_SECRET`.
- O compose lê tudo de variáveis de ambiente; localmente vêm do `.env`, que está no `.gitignore`. Só o `.env.example` (valores fictícios) é versionado.
- Os segredos chegam ao Spring como variáveis de ambiente (`SPRING_DATASOURCE_*`, `JWT_SECRET`), sobrescrevendo o `application.properties`.

## 5. Versionamento semântico e rollback
**Versionamento**: `MAJOR.MINOR.PATCH`, definido por tags Git `vX.Y.Z`. Cada tag gera imagem `ghcr.io/<owner>/<repo>:X.Y.Z` e uma GitHub Release com notas automáticas.

```bash
git tag v1.0.0 && git push origin v1.0.0
```

**Rollback automático**: o `scripts/deploy.sh <nova> <anterior>`
1. sobe a versão anterior estável (baseline);
2. faz o deploy da nova e aguarda o health check;
3. se a nova não ficar `healthy`, sobe a anterior novamente e marca o job como falho.

**Rollback manual**: Actions → CI/CD → *Run workflow* → `rollback_version = 1.0.0` (ou `scripts/rollback.sh 1.0.0`).

### Simulação documentada
```bash
./scripts/simulate-rollback.sh
```
Builda a `1.0.0` (boa), cria a `1.0.1` quebrada, executa o deploy e mostra o rollback para `1.0.0`. A saída fica em `docs/evidencias/rollback-log.txt` (**rode e faça commit desse arquivo como evidência**; coloque também prints da aba Actions e da página de Releases).
