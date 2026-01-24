FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    gcc \
    libxml2-dev \
    libxslt1-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR $APP_HOME
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p service/xml_management/app_xml_files \
             service/app_certs \
             service/crypto \
    && chown -R appuser:appuser $APP_HOME

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/liveness || exit 1

CMD ["uvicorn", "service.api.app:app", "--host", "0.0.0.0", "--port", "8000"]