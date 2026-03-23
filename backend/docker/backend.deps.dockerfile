FROM python:3.12-slim

ENV PYTHONPATH=/app

WORKDIR /app

# System-level dependencies (OCR, PDF rendering, libmagic)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy only the dependency manifest – source code is NOT needed at this stage.
# This way Docker re-uses this layer as long as pyproject.toml hasn't changed.
COPY backend/pyproject.toml ./pyproject.toml

RUN pip install --no-cache-dir ".[openai]" && pip cache purge

# Pre-download NLTK data required by unstructured at parse time
COPY backend/docker/scripts/download_nltk.sh ./download_nltk.sh
RUN chmod +x ./download_nltk.sh && ./download_nltk.sh && rm ./download_nltk.sh

