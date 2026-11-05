# syntax=docker/dockerfile:1

# ---------- Estágio 1: instala as dependências num virtualenv ----------
FROM python:3.12-slim AS builder
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /build
# Só as dependências de produção; o cache só é refeito se este arquivo mudar
COPY requirements-prod.txt .
RUN pip install -r requirements-prod.txt

# ---------- Estágio 2: imagem final enxuta ----------
FROM python:3.12-slim AS runtime

ARG APP_VERSION=dev
LABEL org.opencontainers.image.title="estoque-facil" \
      org.opencontainers.image.version="${APP_VERSION}"

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_VERSION=${APP_VERSION}

RUN useradd --system --create-home app
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY --chown=app:app app ./app
COPY --chown=app:app run.py ./run.py

USER app
EXPOSE 5000

HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=5 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=2).status == 200 else 1)"

# gunicorn (servidor de produção) em vez do servidor de desenvolvimento do Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "run:app"]
