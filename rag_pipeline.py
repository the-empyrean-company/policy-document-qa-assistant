from pypdf import PdfReader
from typing import List
from dataclasses import dataclass

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

@dataclass
class Chunk:
    text: str
    source: str  # filename

def build_chunks(file_paths: List[str]) -> List[Chunk]:
    all_chunks: List[Chunk] = []

    for path in file_paths:
        lower = path.lower()
        if lower.endswith(".pdf"):
            text = read_pdf(path)
        elif lower.endswith(".txt"):
            text = read_txt(path)
        else:
            continue  # unsupported file type for now

        source = path.split("/")[-1]  # just filename
        for ch in chunk_text(text):
            all_chunks.append(Chunk(text=ch, source=source))

    return all_chunks
