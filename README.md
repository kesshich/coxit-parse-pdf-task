# PDF Summarizer

A web application that accepts a PDF file (up to 50 MB, 100 pages), extracts and chunks its content, sends the chunks **in parallel** to an LLM for summarization, and stores the results in MongoDB. A history of the last N summaries is available via the UI and API.

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI, LangChain, OpenAI, Unstructured, pymongo |
| **Frontend** | React 19, TypeScript, Vite |
| **Database** | MongoDB 7 |
| **Containerization** | Docker, Docker Compose |

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- An OpenAI API key
- A Unix-like shell (bash, Git Bash, WSL) to run the scripts

---

## Environment Setup

Copy the example file and fill in your values:

```bash
cp .env.example backend/.env
```

`backend/.env` reference:

```env
# OpenAI
OPENAI_API_KEY=sk-...
GENERATION_MODEL=gpt-4o
LLM_PROVIDER=chatgpt
MAX_TOKENS=2048

# MongoDB
MONGO_URI=mongodb://mongo:27017
MONGO_DB=pdf_parser
HISTORY_LIMIT=5

# PDF limits
MAX_FILE_SIZE_MB=50
MAX_PAGES=100

# Chunking
CHUNK_SIZE=2000
CHUNK_OVERLAP=200

# PDF parsing strategy: auto | fast | hi_res
PDF_STRATEGY=auto

# CORS — JSON array of allowed origins
CORS_ORIGINS=["http://localhost:5173"]
```

---

## Running with Docker

### Using scripts

All scripts are in `scripts/` and must be run from the project root.

```bash
./scripts/dev.sh       # Start all services (builds deps image on first run)
./scripts/stop.sh      # Stop containers — MongoDB volume is preserved
./scripts/rebuild.sh   # Force full rebuild with no Docker cache
```

### Using Taskfile (recommended)

If you have [Task](https://taskfile.dev) installed:

```bash
task dev        # Start all services
task stop       # Stop all containers
task rebuild    # Force full rebuild
task logs       # Stream logs from all containers
task build:deps # Rebuild only the heavy deps image
```

### Services

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| MongoDB | localhost:27017 |

---

## PDF Processing

The parsing strategy is controlled by the `PDF_STRATEGY` environment variable:

| Strategy | Description | Requirements |
|---|---|---|
| `auto` | Unstructured decides per page — OCR only where needed **(recommended)** | Poppler, Tesseract |
| `fast` | Direct text extraction only, no OCR | None |
| `hi_res` | Full OCR + table detection on every page | Poppler, Tesseract |

> Poppler and Tesseract are pre-installed inside the Docker container. For local development on Windows without those tools, use `PDF_STRATEGY=fast`.

### Processing pipeline

```
Upload PDF
    │
    ├─ Validate (size ≤ 50 MB, type = PDF)
    │
    ├─ Extract & chunk text (Unstructured + LangChain splitter)
    │   └─ Chunks: ~2000 chars with 200-char overlap
    │
    ├─ Map phase — summarize each chunk in parallel (LLM)
    │
    ├─ Reduce phase — merge chunk summaries into one final summary (LLM)
    │
    └─ Save to MongoDB history → return result
```

---

## API

### `POST /api/v1/pdf/analyze`

Upload a PDF for analysis and get back a summary.

**Request** — `multipart/form-data`:

| Field | Type | Constraints |
|---|---|---|
| `file` | file | PDF only, max 50 MB, max 100 pages |

**Response** `200 OK`:

```json
{
  "id": "665f1a2b3c4d5e6f7a8b9c0d",
  "filename": "document.pdf",
  "result": "The document covers..."
}
```

**Error responses**:

| Code | Reason |
|---|---|
| `400` | Not a PDF file / exceeds size or page limit |
| `422` | No text could be extracted from the PDF |
| `500` | LLM or internal processing error |

---

### `GET /api/v1/history`

Returns the most recent summaries (default: last 5, configurable via `HISTORY_LIMIT`).

**Response** `200 OK`:

```json
[
  {
    "id": "665f1a2b3c4d5e6f7a8b9c0d",
    "filename": "document.pdf",
    "result": "The document covers...",
    "created_at": "2024-06-04T12:00:00Z"
  }
]
```

