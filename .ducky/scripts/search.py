import os
import sys

# Ducky's directory for plain text files is called 'nest'
NEST = os.path.abspath(os.path.join(sys.prefix, "../nest"))


# Get the text from Ducky's nest.
def get_text(filename):
    filename_txt = os.path.splitext(filename)[0] + ".txt"
    text = os.path.join(NEST, filename_txt)
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
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/search.py <filename> <keyword 1> <keyword 2> ...")
    filename = sys.argv[1]
    keywords = sys.argv[2:]
    try:
        results = search_text(filename, keywords)
        print_text(results)
    except FileNotFoundError as e:
        print(f"\nFileNotFound exception: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"\nUnexcepted exception: {e}")
        sys.exit(1)

