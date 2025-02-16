import os
import sys


NEST = os.path.abspath(os.path.join(sys.prefix, "../nest"))


def get_text(filename):
    filename_txt = os.path.splitext(filename)[0] + ".txt"
    text = os.path.join(NEST, filename_txt)
    return text


def search_text(filename, keywords):
    text  = get_text(filename)
    if not os.path.exists(text):
        raise FileNotFoundError(f"Text file not found:  {filename}")
    results = {}
    for keyword in keywords:
        results[keyword] = []
    with open(text, "r", encoding="utf-8") as file:
        for line in file:
            snippet = line.strip()
            for keyword in keywords:
                if keyword.lower() in snippet.lower():
                    results[keyword].append(snippet)
    return results


def print_text(results):
    found = False
    for keyword in results:
        matches = results[keyword]
        if matches:
            found = True
            print(f"\nMatches for '{keyword}':")
            for match in matches:
                print(f"\n -> {match}")
    if not found:
        print("\nNo matches found.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/search.py <filename> <keyword 1> <keyword 2> ...")
    filename = sys.argv[1]
    keywords = sys.argv[2:]
    try:
        results = search_text(filename, keywords)
        print_text(results)
    except FileNotFoundError as e:
        printf(f"\nFileNotFound exception: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"\nUnexcepted exception: {e}")
        sys.exit(1)

