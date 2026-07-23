"""
Extracts text from a PDF, page by page, preserving page number metadata.
Page numbers matter a lot for clinical documents - we need to be able
to cite "this criterion is from page 12" later in the RAG pipeline.
"""

import fitz  # PyMuPDF


def extract_pdf_text(filepath: str) -> list[dict]:
    """
    Returns a list of dicts, one per page:
    [{"page_number": 1, "text": "..."}, {"page_number": 2, "text": "..."}, ...]
    Keeping this page-structured (not one giant string) from the very
    start is what makes citation-with-page-numbers possible later.
    """
    doc = fitz.open(filepath)
    pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        pages.append({
            "page_number": page_num + 1,  # 1-indexed, matches how humans reference pages
            "text": text,
        })

    doc.close()
    return pages


if __name__ == "__main__":
    pages = extract_pdf_text("data/raw/protocols/sample_protocol.pdf")

    print(f"Total pages: {len(pages)}")
    print(f"\n--- Page 1 preview (first 500 chars) ---")
    print(pages[0]["text"][:500])
