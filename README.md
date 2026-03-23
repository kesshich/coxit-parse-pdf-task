# PDF Summarizer

A web application that accepts a PDF file (up to 50 MB, 100 pages), extracts and chunks its content, sends the chunks in parallel to an LLM for summarization, and stores the results in MongoDB. A history of the last 5 summaries is available via the UI and API.

## Tech Stack

- **Backend**: FastAPI, LangChain, OpenAI, PyPDF / Unstructured, pymongo
- **Frontend**: React 18, TypeScript, Vite
- **Database**: MongoDB 7
- **Containerization**: Docker, Docker Compose

---

## Prerequisites

- Docker and Docker Compose installed
- An OpenAI API key

---

## Environment Setup

Create a file at `backend/.env`:

```env
OPENAI_API_KEY=sk-...
GENERATION_MODEL=gpt-4o
LLM_PROVIDER=chatgpt

MONGO_URI=mongodb://mongo:27017
MONGO_DB_NAME=pdf_parser

MAX_FILE_SIZE_MB=50
MAX_PAGES=100
CHUNK_SIZE=2000
CHUNK_OVERLAP=200
```

> `PDF_STRATEGY` is set automatically by Docker Compose (`hi_res` inside the container). For local development without Poppler/Tesseract, it defaults to `fast`.

---

## Running with Docker

All scripts are in the `scripts/` directory and require a Unix-like shell (bash, Git Bash, WSL).

| Script | Description |
|---|---|
| `./scripts/dev.sh` | Build images and start all services, stream logs |
| `./scripts/stop.sh` | Stop containers (MongoDB volume is preserved) |
| `./scripts/rebuild.sh` | Full rebuild without Docker layer cache |

```bash
./scripts/dev.sh
```

Services:

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| MongoDB | localhost:27017 |

---

## API

### POST /api/v1/pdf/analyze

Upload a PDF file for analysis.

**Request**: `multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `file` | file | PDF file, max 50 MB, max 100 pages |

**Response** `200 OK`:

```json
{
  "id": "665f1a2b3c4d5e6f7a8b9c0d",
  "filename": "document.pdf",
  "result": "Summary of the document..."
}
```

**Error responses**:

| Code | Reason |
|---|---|
| 400 | File is not a PDF |
| 422 | File exceeds size or page limit |
| 500 | LLM or processing error |

---

### GET /api/v1/history/

Returns the last 5 analyzed documents.

**Response** `200 OK`:

```json
[
  {
    "id": "665f1a2b3c4d5e6f7a8b9c0d",
    "filename": "document.pdf",
    "result": "Summary...",
    "created_at": "2024-06-04T12:00:00"
  }
]
```

---

## PDF Processing Modes

The service supports two strategies, controlled by the `PDF_STRATEGY` environment variable:

| Strategy | Description | Requirements |
|---|---|---|
| `fast` | Text-only extraction via pdfminer (default for local dev) | None |
| `hi_res` | OCR + table detection via Unstructured (used in Docker) | Poppler, Tesseract |

In `hi_res` mode, images and scanned pages are processed with OCR so their text is included in the summary.

