"""
pdf_extractor.py
----------------
Handles everything related to reading a PDF file and pulling clean,
usable text out of it.

Why a separate file?
Keeping "PDF reading logic" away from "AI logic" and "UI logic" is called
SEPARATION OF CONCERNS. It makes the project easier to test, debug, and
explain in interviews ("I structured my code into modules...").
"""

import fitz  # this is the PyMuPDF library, imported as "fitz" for historical reasons
from typing import Tuple


# Custom exception classes make error handling readable.
# Instead of catching generic "Exception", we can catch THESE specific
# problems and show the user a helpful message instead of a scary traceback.
class EmptyPDFError(Exception):
    """Raised when a PDF has no extractable text at all."""
    pass


class CorruptPDFError(Exception):
    """Raised when the PDF file is damaged or not a valid PDF."""
    pass


class PDFTooLargeError(Exception):
    """Raised when the PDF exceeds our allowed page/size limit."""
    pass


# Configurable safety limits — tweak these as needed.
MAX_PAGES = 100          # prevents extremely long PDFs from freezing the app
MAX_FILE_SIZE_MB = 25    # prevents huge uploads from crashing memory


def validate_file_size(file_bytes: bytes) -> None:
    """
    Checks the uploaded file's size in megabytes.
    Streamlit gives us the file as raw bytes, so we convert byte-count to MB.
    """
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise PDFTooLargeError(
            f"File is {size_mb:.1f} MB. Maximum allowed is {MAX_FILE_SIZE_MB} MB."
        )


def extract_text_from_pdf(file_bytes: bytes) -> Tuple[str, int]:
    """
    Takes raw PDF bytes (from Streamlit's file_uploader) and returns:
        - the extracted text (str)
        - the number of pages (int)

    Raises:
        CorruptPDFError  -> if the file can't be opened as a PDF
        PDFTooLargeError -> if it has too many pages
        EmptyPDFError    -> if no text could be extracted (e.g. scanned images)
    """
    validate_file_size(file_bytes)

    # Try to open the PDF. If the bytes aren't a real/valid PDF,
    # PyMuPDF throws an error, which we catch and convert into our
    # own clear, custom exception.
    try:
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        raise CorruptPDFError(f"Could not open PDF — it may be corrupted. ({e})")

    num_pages = pdf_document.page_count

    if num_pages == 0:
        raise EmptyPDFError("This PDF has zero pages.")

    if num_pages > MAX_PAGES:
        pdf_document.close()
        raise PDFTooLargeError(
            f"This PDF has {num_pages} pages. Maximum allowed is {MAX_PAGES}."
        )

    # Loop through every page and pull its text, then join with newlines.
    extracted_text_parts = []
    for page_index in range(num_pages):
        page = pdf_document.load_page(page_index)
        page_text = page.get_text("text")  # "text" mode = plain reading-order text
        extracted_text_parts.append(page_text)

    pdf_document.close()

    full_text = "\n".join(extracted_text_parts).strip()

    # If a PDF is just scanned images with no real text layer,
    # extraction will return almost nothing — we treat that as "empty".
    if len(full_text) < 20:
        raise EmptyPDFError(
            "No readable text found. This PDF might be a scanned image "
            "without OCR — try a text-based PDF instead."
        )

    return full_text, num_pages


def truncate_text(text: str, max_chars: int = 30000) -> str:
    """
    Gemini (and all LLMs) have a context limit. Extremely long PDFs need
    to be trimmed before being sent to the API, otherwise the request
    fails or gets very expensive.

    This keeps the beginning and end of the document, since intros and
    conclusions usually carry the most "summary-worthy" information,
    and drops the (less critical) middle if needed.
    """
    if len(text) <= max_chars:
        return text

    half = max_chars // 2
    return (
        text[:half]
        + "\n\n... [content trimmed for length] ...\n\n"
        + text[-half:]
    )