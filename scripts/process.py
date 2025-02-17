#!/usr/bin/env python3

import os
import sys
import re
import pdfplumber
from config import DUCKY_POND, DUCKY_NEST

# Read and extract text from a PDF.
def read_text(filename):
    filename_pdf = os.path.join(DUCKY_POND, filename)
    if not os.path.exists(filename_pdf):
        raise FileNotFoundError(f"File not found: {filename_pdf}")
    text = []
    prev_lines = set() 
    page_number = 0
    with pdfplumber.open(filename_pdf) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            extracted = page.extract_text()
            page_number += 1
            if extracted:
                lines = extracted.strip().split("\n")
                clean_lines = [line for line in lines if line not in prev_lines]
                prev_lines.update(lines[:3])
                if clean_lines:
                    text.append(f"\n".join(clean_lines))
    return "\n".join(text)

# Remove duplicate lines and fix spacing.
import re

def clean_text(text):
    text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)
    text = re.sub(r'[\u2022•*▪-]\s*', '\n', text)
    lines = text.split("\n")
    fixed_lines = []
    buffer = []
    for line in lines:
        line = line.strip()
        if line:
            if buffer and not re.match(r'[.!?]$', buffer[-1]):
                buffer[-1] += " " + line
            else:
                buffer.append(line)
    seen = set()
    cleaned_lines = []
    for line in buffer:
        line = re.sub(r'(?<=[.])\s*', '\n', line)
        if line not in seen:
            seen.add(line)
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

# Save the cleaned text to a .txt file.
def save_text(filename, text):
    if not os.path.exists(DUCKY_NEST):
        os.makedirs(DUCKY_NEST)
    filename_txt = os.path.splitext(filename)[0] + ".txt"
    output = os.path.join(DUCKY_NEST, filename_txt)
    cleaned_text = clean_text(text)
    with open(output, "w", encoding="utf-8") as file:
        file.write(cleaned_text)
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
