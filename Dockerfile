FROM python:3.12-slim

WORKDIR /app

# Ensure latest patched Debian 12 OpenSSL packages (CVE-2025-15467 clean)
RUN apt-get update && apt-get upgrade -y openssl libssl3 && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir \
    "fastapi>=0.115.0" \
    "uvicorn[standard]>=0.32.0" \
    "google-cloud-spanner>=3.49.0" \
    "google-cloud-bigquery>=3.26.0" \
    "google-cloud-discoveryengine>=0.13.0" \
    "google-cloud-storage>=2.18.0" \
    "google-genai>=1.0.0" \
    "fpdf2>=2.8.1" \
    "pydantic>=2.9.0" \
    "httpx>=0.27.0"

COPY app ./app
COPY static ./static
COPY docs ./docs

ENV PORT=8080
ENV SPANNER_ENABLE_BUILTIN_METRICS=false

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
