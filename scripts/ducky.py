#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
import subprocess
from config import DUCKY_POND, DUCKY_NEST
from process import read_text, save_text

def add_file(filename):
    """Adds a file to the ducky pond and processes it."""
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    destination = os.path.join(DUCKY_POND, os.path.basename(filename))

    try:
        shutil.copy(filename, destination)
        print(f"File '{filename}' added to ducky pond!")

        process_script = os.path.join(os.path.dirname(__file__), "process.py")
        subprocess.run(
            [process_script, os.path.basename(filename)],
            check=True,
            text=True,
            stdout=sys.stdout,
            stderr=sys.stderr
        )

    except subprocess.CalledProcessError as e:
        print(f"Error: process.py failed with exit code {e.returncode}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def delete_file(filename):
    """Deletes a file from the ducky pond."""
    target_file = os.path.join(DUCKY_POND, os.path.basename(filename))

    if not os.path.exists(target_file):
        print(f"Error: File '{filename}' not found in ducky pond.")
        sys.exit(1)

    try:
        os.remove(target_file)
        print(f"File '{filename}' removed from ducky pond.")
    except Exception as e:
        print(f"Error removing file: {e}")
        sys.exit(1)

def main():
    """Ducky CLI command handler."""
    parser = argparse.ArgumentParser(prog="ducky", description="Ducky CLI Command")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a file to ducky pond.")
    add_parser.add_argument("filename", help="Name of file to add.")

    # Del command
    del_parser = subparsers.add_parser("del", help="Delete a file from ducky pond.")
    del_parser.add_argument("filename", help="Name of file to delete.")

    args = parser.parse_args()

    if args.subcommand == "add":
        add_file(args.filename)
    elif args.subcommand == "del":
        delete_file(args.filename)

if __name__ == "__main__":
    main()