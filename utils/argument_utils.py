import argparse 
import sys 
import os 
from pathlib import Path
from consts.constants import MAX_CHARACTERS

def parse_args():
    """
    Generic CLI arg parsing
    """
    parser = argparse.ArgumentParser(
        description="shuffle_shift: accepts a string input (via --text or --file), and converts to a completely different grammatically correct sentence using exact input letters"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--text",
        type=str,
        help="Input text string"
    )
    group.add_argument(
        "--file",
        type=str,
        help="Path to input file"
    )

    return parser.parse_args()

def validate_args(args): 
    """
    Validate CLI args: 
    --text: muist be non-empty 
    --file: must exist and be readable 
    Extracted text string must be under MAX_CHARACTERS length
    returns actual text string (if successful, exit if not)
    """

    text = ""

    if args.text: 
        if not args.text.strip():
            print("Error: --text cannot be empty")
            sys.exit(1)
        text = args.text

    if args.file: 
        path = Path(args.file)
        if not path.exists():
            print(f"Error: file '{args.file}' not found")
            sys.exit(1)
        if not path.is_file():
            print(f"Error: '{args.file}' is not a file")
            sys.exit(1)
        if not os.access(path, os.R_OK):
            print(f"Error: can't read '{args.file}'")
            sys.exit(1)
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file '{args.file}': {e}")
            sys.exit(1)

    if len(text) > MAX_CHARACTERS:
        print(f"Error: text size too large (must be under {MAX_CHARACTERS} characters)")
        sys.exit(1)

    return text
