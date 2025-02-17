#!/usr/bin/env python3
import os
import sys
from config import DUCKY_NEST


# Get the text from Ducky's nest.
def get_text(filename):
    filename_txt = os.path.splitext(filename)[0] + ".txt"
    text = os.path.join(DUCKY_NEST, filename_txt)
    return text


# Search the text for the keywords
def search_text(filename, keywords):
    # Get the text from the filename.
    text  = get_text(filename)

    if not os.path.exists(text):
        raise FileNotFoundError(f"Text file not found:  {filename}")

    # Store the results as a key-pair dictionary.
    results = {}

    # Loop through the specified keywords.
    for keyword in keywords:
        # Create a new list for each keyword.
        results[keyword] = []

    # Open the file and read its lines.
    with open(text, "r", encoding="utf-8") as file:
        lines = file.readlines()

    page_number = 1
    line_number = 1

    for line in lines:
        snippet = line.strip()

        # Check if there's a page break.
        if snippet == "\n\r":
            page_number += 1        # Increase page count
            line_number = 1         # Reset line count
            continue

        # Loop through the keywords again.
        for keyword in keywords:
            # Append the result if keyword is found in snippet.
            if keyword.lower() in snippet.lower():
                title = f"In '{filename}'"
                location = f"Page {page_number}, line {line_number}"
                output = f"{title} ({location})\n{snippet}"
                results[keyword].append(output)

        line_number += 1            # Increase line count.

    return results


# Search the text in each file in the nest
def search_nest(keywords):
    if not os.path.exists(DUCKY_NEST):
        print(f"Error: DUCKY_NEST directory '{DUCKY_NEST}' doesn't exist.")
        sys.exit(1)

    # Get all the text files in the nest
    text_files = []
    for root, _, files in os.walk(DUCKY_NEST):
        for f in files:
            if f.endswith(".txt"):
                text_files.append(os.path.join(root, f))
    if not text_files:
        print("\nNo text files found in ducky's nest.")
        sys.exit(1)

    # Get the results for each search
    results = {keyword: [] for keyword in keywords}
    for file_path in text_files:
        file_name = os.path.basename(file_path)
        try:
            # Search the text file and store results
            file_results = search_text(file_name, keywords)
            for keyword, matches in file_results.items():
                results[keyword].extend(matches)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"\nError searching '{file_name}': {e}")
    return results

# Print the results to the console if found.
def print_text(results):
    found = False

    # Loop through the keywords in results.
    for keyword in results:
        # Find the matches based on the keyword.
        matches = results[keyword]

        # Print each match that's found for a keyword.
        if matches:
            found = True
            print(f"\nMatches for '{keyword}':")
            for match in matches:
                print(f"\n -> {match}")
    if not found:
        print("\nNo matches found.")


# CLI execution.
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/search.py <keyword 1> <keyword 2> ...")
    try:
        keywords = sys.argv[1:]
        results = search_nest(keywords)
        print_text(results)
    except FileNotFoundError as e:
        print(f"\nFileNotFound exception: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"\nUnexcepted exception in search: {e}")
        sys.exit(1)

