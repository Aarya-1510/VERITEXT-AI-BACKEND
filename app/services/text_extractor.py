from pathlib import Path

from pypdf import PdfReader
from docx import Document


def extract_text(file_path: str) -> str:
    extension = Path(file_path).suffix.lower()

    if extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    elif extension == ".pdf":
        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    elif extension == ".docx":
        document = Document(file_path)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    else:
        raise ValueError(
            "Unsupported file type. Please upload PDF, DOCX, or TXT."
        )