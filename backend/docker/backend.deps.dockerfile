FROM python:3.12-slim

ENV PYTHONPATH=/app
WORKDIR /app

# ── System packages required by unstructured / OCR ───────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# ── Python deps (cached unless pyproject.toml changes) ───────────────────
COPY backend/pyproject.toml ./pyproject.toml
COPY README.md ./README.md
RUN mkdir -p backend && touch backend/__init__.py
RUN pip install --no-cache-dir ".[openai]" && pip cache purge

