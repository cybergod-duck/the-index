import PyPDF2
from pathlib import Path

pdf_path = Path("C:/Projects/the-index/posting_guide.pdf")

try:
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            print(page.extract_text())
except Exception as e:
    print(f"Error reading PDF: {e}")
