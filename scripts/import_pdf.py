import os
import sys
from PyPDF2 import PdfReader


POND = os.path.abspath(os.path.join(sys.prefix, "../pond"))
NEST = os.path.abspath(os.path.join(sys.prefix, "../nest"))


def read_text(filename):
    pdf_path = os.path.join(POND, filename)
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    pdf = PdfReader(pdf_path)
    result = []
    for page in pdf.pages:
        text = page.extract_text()

        if text is not None:
            result.append(text.strip())
    return "\n".join(result)


def save_text(filename, content):
    if not os.path.exists(NEST):
        os.makedirs(NEST)
    txt = os.path.splitext(filename)[0] + ".txt"
    output = os.path.join(NEST, txt)
    with open(output, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Text was saved to {output}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/import_pdf.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    try:
        save_text(filename, read_text(filename))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
