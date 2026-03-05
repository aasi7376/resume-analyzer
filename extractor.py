import re
import PyPDF2

def extract_text_from_pdf(file_path):
    text = ""

    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Clean extracted text
    text = re.sub(r"\s+", " ", text)           # Remove extra spaces
    text = re.sub(r"[^\x00-\x7F]+", " ", text) # Remove non-English characters
    text = text.strip()

    return text