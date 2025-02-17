#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
import subprocess
from config import DUCKY_POND
from config import DUCKY_NEST
from process import read_text
from process import save_text

def add_file(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exist(1)
    destination = os.path.join(DUCKY_POND, os.path.basename(filename))
    try:
        shutil.copy(filename, destination)
        print(f"File '{filename}' added to ducky pond!")
        process_script = os.path.join(os.path.dirname(__file__), "process.py")
        result = subprocess.run(
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
        
    except Exception as e:
        print(f"Error adding file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(prog="ducky", description="Ducky CLI Command")
    subparsers = parser.add_subparsers(dest="command", required=True)
    add_parser = subparsers.add_parser("add", help="Add a file to duck pond.")
    add_parser.add_argument("filename", help="Name of file to add.")
    args = parser.parse_args()
    if args.command == "add":
        add_file(args.filename)

if __name__ == "__main__":
    main()
