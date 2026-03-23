import io
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from backend.schemas.history import HistoryRecord


def test_history_returns_200(client: TestClient):
    records = [
        HistoryRecord(
            id="507f1f77bcf86cd799439011",
            filename="report.pdf",
            result="This is a summary.",
            created_at=datetime.now(timezone.utc),
        )
    ]
    with patch(
        "backend.api.routes.history.get_latest_summaries",
        new_callable=AsyncMock,
        return_value=records,
    ):
        response = client.get("/api/v1/history")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["filename"] == "report.pdf"


def test_history_returns_empty_list(client: TestClient):
    with patch(
        "backend.api.routes.history.get_latest_summaries",
        new_callable=AsyncMock,
        return_value=[],
    ):
        response = client.get("/api/v1/history")

    assert response.status_code == 200
    assert response.json() == []


def test_analyze_rejects_non_pdf(client: TestClient):
    response = client.post(
        "/api/v1/pdf/analyze",
        files={"file": ("document.txt", io.BytesIO(b"not a pdf"), "text/plain")},
    )
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


def test_analyze_rejects_oversized_file(client: TestClient):
    # Construct a fake file just over the 50 MB limit
    large_content = b"x" * (51 * 1024 * 1024)
    response = client.post(
        "/api/v1/pdf/analyze",
        files={"file": ("big.pdf", io.BytesIO(large_content), "application/pdf")},
    )
    assert response.status_code == 400
    assert "exceeds" in response.json()["detail"]

