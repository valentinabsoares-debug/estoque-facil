# Changelog

Todas as mudanças notáveis neste projeto serão documentadas aqui.

O formato segue o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [Unreleased]

### Adicionado
- Dockerfile multi-stage (gunicorn, usuário não-root, healthcheck) e `docker-compose.yml`
- Rota `GET /health`
- Pipeline de CD: imagem no GHCR com versionamento semântico, deploy em homologação, rollback automático e manual
- Gestão de segredos via GitHub Secrets e `.env.example`

### Corrigido
- `app/_init_.py` → `app/__init__.py` e `app/routs.py` → `app/routes.py` (a API não importava)
- `requirements.txt` sem duplicatas; dependências de produção em `requirements-prod.txt`

### Removido
- Workflows duplicados (`ci-.yml` e `ci.yml` da raiz), unificados em `.github/workflows/ci.yml`

---

## [1.0.0] - 2025-01-01

### Adicionado
- Interface CLI completa com menu interativo
- Funcionalidade de adicionar produto (nome, quantidade, preço, categoria)
- Listagem de produtos com filtro por categoria
- Atualização de quantidade por ID
- Remoção de produto por ID
- Alerta de estoque baixo configurável
- Cálculo do valor total do estoque
- Persistência em arquivo JSON local
- Testes automatizados com Pytest (21 casos de teste)
- Linting configurado com Ruff
- Pipeline CI com GitHub Actions
