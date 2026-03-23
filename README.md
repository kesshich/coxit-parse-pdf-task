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
- [Task](https://taskfile.dev/#/installation) (optional but recommended)
- A Unix-like shell (bash, Git Bash, WSL) to run scripts

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

### Using Taskfile (recommended)

```bash
task up        # Build and start all services (frontend + backend + mongo)
task down      # Stop containers — MongoDB volume is preserved
task restart   # Restart running containers
task logs      # Stream logs from all containers
task ps        # Show container status
task clean     # Stop containers and remove volumes (deletes Mongo history)
```

### Using Docker Compose directly

```bash
docker compose up -d           # Start all services
docker compose down            # Stop containers
docker compose logs -f         # Stream logs
docker compose build frontend  # Rebuild frontend image after code changes
```

### Services

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| MongoDB | localhost:27017 |

---

## Development workflow

| Changed | What to do |
|---|---|
| Any backend `.py` file | Nothing — uvicorn reloads automatically |
| Frontend `.tsx` / `.ts` / `.css` | `docker compose build frontend && docker compose up -d frontend` |
| Backend dependencies (`pyproject.toml`) | `task down` → rebuild backend image → `task up` |

---

## PDF Processing

The parsing strategy is controlled by the `PDF_STRATEGY` environment variable:

| Strategy | Description |
|---|---|
| `auto` | Unstructured decides per page — OCR only where needed **(recommended)** |
| `fast` | Direct text extraction only, no OCR |
| `hi_res` | Full OCR + table detection on every page |

> Poppler and Tesseract are pre-installed inside the Docker container.

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
  "summary": "The document covers..."
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
    "summary": "The document covers...",
    "created_at": "2024-06-04T12:00:00Z"
  }
]
```
