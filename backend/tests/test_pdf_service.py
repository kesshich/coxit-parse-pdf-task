from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from backend.services.pdf_service import load_and_split


def _make_doc(page_number: int, text: str = "Sample text content for testing purposes.") -> MagicMock:
    doc = MagicMock()
    doc.page_content = text
    doc.metadata = {"page_number": page_number}
    return doc


def test_raises_422_when_loader_returns_no_docs():
    with patch("backend.services.pdf_service.UnstructuredPDFLoader") as mock_loader:
        mock_loader.return_value.load.return_value = []

        with pytest.raises(HTTPException) as exc:
            load_and_split("/fake/path.pdf")

    assert exc.value.status_code == 422


def test_raises_400_when_page_limit_exceeded():
    # 101 pages exceeds the default MAX_PAGES=100
    docs = [_make_doc(i) for i in range(1, 102)]

    with patch("backend.services.pdf_service.UnstructuredPDFLoader") as mock_loader, \
         patch("backend.services.pdf_service.RecursiveCharacterTextSplitter") as mock_splitter:
        mock_loader.return_value.load.return_value = docs
        mock_splitter.return_value.split_documents.return_value = docs

        with pytest.raises(HTTPException) as exc:
            load_and_split("/fake/path.pdf")

    assert exc.value.status_code == 400


def test_returns_chunk_strings_on_success():
    docs = [_make_doc(1)]
    chunk_mocks = [MagicMock(page_content="chunk one"), MagicMock(page_content="chunk two")]

    with patch("backend.services.pdf_service.UnstructuredPDFLoader") as mock_loader, \
         patch("backend.services.pdf_service.RecursiveCharacterTextSplitter") as mock_splitter:
        mock_loader.return_value.load.return_value = docs
        mock_splitter.return_value.split_documents.return_value = chunk_mocks

        result = load_and_split("/fake/path.pdf")

    assert result == ["chunk one", "chunk two"]

