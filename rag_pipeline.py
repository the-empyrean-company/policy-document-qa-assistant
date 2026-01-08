from pypdf import PdfReader
from typing import List

def read_pdf(path: str) -> str:
    """Extract text from all pages of a PDF and return it as one string."""
    reader = PdfReader(path)
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)

def read_txt(path: str) -> str:
    """Read a UTF-8 text file and return its contents."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks.

    chunk_size and overlap are measured in characters (for simplicity).
    Later we can switch to token-based chunking.

    overlap helps preserve continuity across boundaries.
    """
    # Normalize whitespace so chunk boundaries are more stable
    text = " ".join(text.split())
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])

        if end == len(text):
            break

        # Move forward but keep an overlap
        start = max(0, end - overlap)

    return chunks