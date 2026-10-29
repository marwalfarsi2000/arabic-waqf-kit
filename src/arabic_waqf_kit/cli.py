"""Command-line entry point; read-only unless an output file is specified."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import strip_final_short_vowels


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Safely remove terminal Arabic short-vowel marks for TTS scripts."
    )
    parser.add_argument("--input", "-i", type=Path, help="UTF-8 input text file (default: stdin)")
    parser.add_argument("--output", "-o", type=Path, help="Write a new UTF-8 file (default: stdout)")
    parser.add_argument("--overwrite", action="store_true", help="Explicitly allow overwriting output")
    parser.add_argument("--check", action="store_true", help="Exit with 1 when changes would be made; don't write output")
    args = parser.parse_args(argv)
    if args.check and args.output:
        parser.error("--check cannot be combined with --output")
    if args.overwrite and not args.output:
        parser.error("--overwrite requires --output")
    try:
        source = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
        result = strip_final_short_vowels(source)
        if args.check:
            return 1 if source != result else 0
        if args.output:
            if args.input and args.input.resolve() == args.output.resolve() and not args.overwrite:
                parser.error("Input and output are the same file; use --overwrite explicitly")
            mode = "w" if args.overwrite else "x"
            with args.output.open(mode, encoding="utf-8", newline="") as output_file:
                output_file.write(result)
        else:
            sys.stdout.write(result)
    except (OSError, UnicodeError) as error:
        parser.exit(2, f"arabic-waqf: {error}\n")
    return 0
