import os
import sys
from PyPDF2 import PdfReader


POND = os.path.abspath(os.path.join(sys.prefix, "../pond"))
NEST = os.path.abspath(os.path.join(sys.prefix, "../nest"))


def read_text(filename):
    filename_pdf = os.path.join(POND, filename)
    if not os.path.exists(filename_pdf):
        raise FileNotFoundError(f"File not found: {filename_pdf}")
    pdf = PdfReader(filename_pdf)
    result = []
    for page in pdf.pages:
        text = page.extract_text()
        if text is not None:
            text = text.replace("?", "?\n")
            text = text.replace(".", ".\n")
            text = text.replace("•", "\n")
            text = text.replace("- ", "\n")
            text = text.replace("●", "\n")
            text = text.replace("◦", "\n")
            result.append("\n" + text.strip())
    return "\n".join(result)


def save_text(filename, text):
    if not os.path.exists(NEST):
        os.makedirs(NEST)
    filename_txt = os.path.splitext(filename)[0] + ".txt"
    output = os.path.join(NEST, filename_txt)
    with open(output, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Text was saved to {output}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/import.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    try:
        text = read_text(filename)
        save_text(filename, text)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
