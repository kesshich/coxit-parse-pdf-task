from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes.history import router as history_router
from backend.api.routes.pdf import router as pdf_router
from backend.core.settings import AppSettings


def create_app() -> FastAPI:
    settings = AppSettings()

    app = FastAPI(
        title="PDF Parser API",
        description="Upload a PDF, ask a question, get an LLM-powered answer. Results are saved to history.",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(pdf_router, prefix="/api/v1")
    app.include_router(history_router, prefix="/api/v1")

    return app

