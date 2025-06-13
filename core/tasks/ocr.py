# pdfplumber + pytesseract implementation
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

# Optional: Set Tesseract path if needed (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(file_path: str) -> str:
    try:
        full_text = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

        if full_text.strip():
            return full_text

        # If text-based OCR fails, use image OCR
        images = convert_from_path(file_path)
        for image in images:
            full_text += pytesseract.image_to_string(image)

        return full_text.strip()

    except Exception as e:
        logger.error(f"OCR failed for {file_path}: {str(e)}")
        return "[OCR Failed]"