#!/usr/bin/env python3

import os
import sys
import re
from PyPDF2 import PdfReader
from config import DUCKY_POND
from config import DUCKY_NEST

# Read the PDF's text and extract to plain text format.
def read_text(filename):
    # Retrieve the PDF from Ducky's pond.
    filename_pdf = os.path.join(DUCKY_POND, filename)

    if not os.path.exists(filename_pdf):
        raise FileNotFoundError(f"File not found: {filename_pdf}")

    # Get the PDF to read and create an array for the results.
    pdf = PdfReader(filename_pdf)
    result = []

    # Loop through each page in the PDF.
    for page in pdf.pages:
        text = page.extract_text()

        # Append the trimmed text to the results array.
        if text is not None:
            text = text.replace("?", "?\n")
            text = text.replace(".", ".\n")
            text = text.replace("•", "\n")
            text = text.replace("- ", "\n")
            text = text.replace("●", "\n")
            text = text.replace("◦", "\n")
            text = re.sub(r"([A-Z][A-Z\s]+)", r"\1\n", text)
            result.append("\n" + text.strip())

    return "\n".join(result)


# Save the text in a plain text file.
def save_text(filename, text):
    # Create Ducky's Nest if not already.
    if not os.path.exists(DUCKY_NEST):
        os.makedirs(DUCKY_NEST)

    # Create the file and its name.
    filename_txt = os.path.splitext(filename)[0] + ".txt"
    output = os.path.join(DUCKY_NEST, filename_txt)

    # Write the text to the file.
    with open(output, "w", encoding="utf-8") as file:
        file.write(text)

    print(f"\nText was saved to {output}\n")


# CLI execution.
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
