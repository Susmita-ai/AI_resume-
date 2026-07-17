import pdfplumber
import easyocr
import fitz  # PyMuPDF
from PIL import Image
import numpy as np

# Initialize OCR reader
reader = easyocr.Reader(['en'], gpu=False)


def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF using pdfplumber.
    Falls back to OCR if the PDF has no real text layer
    (e.g. scanned resumes or PDFs exported as flattened images).
    """

    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    if text.strip():
        return text

    # No text found -> likely a scanned/image-only PDF, fall back to OCR
    return _extract_text_from_scanned_pdf(pdf_path)


def _extract_text_from_scanned_pdf(pdf_path):
    """
    Renders each PDF page to an image and runs OCR on it.
    Used only when pdfplumber can't find a text layer.
    """
    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        pix = page.get_pixmap(dpi=200)
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image_array = np.array(image)

        result = reader.readtext(image_array)

        for item in result:
            text += item[1] + " "
        text += "\n"

    doc.close()

    return text


def extract_text_from_image(image_path):
    """
    Extract text from image using EasyOCR
    """

    image = np.array(Image.open(image_path))

    result = reader.readtext(image)

    text = ""

    for item in result:
        text += item[1] + " "

    return text