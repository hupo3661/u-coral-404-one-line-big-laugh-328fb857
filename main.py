#!/usr/bin/env python3
"""One Line, Big Laugh - writes one funny line to /output/entry.txt.

Deterministic: no randomness, no network, no clock. The line is a
single sentence of at most 200 characters. Each gate rule lives in
its own small check so a failing rule names itself in the error.
"""

import os

LINE = "My smart fridge ordered milk, my smart speaker cancelled the order, and now my appliances are in a custody battle over my breakfast."

MAX_CHARS = 200


def check_not_empty(line: str) -> None:
    """Reject blank or whitespace-only lines."""
    if not line.strip():
        raise SystemExit("Invalid line: entry must be non-empty.")


def check_no_edge_whitespace(line: str) -> None:
    """Reject leading or trailing whitespace invisible in the output."""
    if line != line.strip():
        raise SystemExit(
            "Invalid line: entry must not have leading or trailing whitespace."
        )


def check_length(line: str) -> None:
    """Enforce the competition's 200-character gate."""
    if len(line) > MAX_CHARS:
        raise SystemExit(
            f"Invalid line: {len(line)} characters, over the {MAX_CHARS} limit."
        )


def check_single_line(line: str) -> None:
    """Reject any line break: the entry must be exactly one line."""
    if "\n" in line or "\r" in line:
        raise SystemExit(
            "Invalid line: entry must be a single line with no newline characters."
        )


def check_text_safe(line: str) -> None:
    """Reject control characters and confirm valid UTF-8."""
    line.encode("utf-8")
    bad = [c for c in line if ord(c) < 0x20]
    if bad:
        raise SystemExit(
            "Invalid line: entry contains control characters: "
            + ", ".join(f"U+{ord(c):04X}" for c in bad)
        )


def check_word_count(line: str) -> None:
    """Sanity check: a one-liner needs at least two words to land."""
    if len(line.split()) < 2:
        raise SystemExit("Invalid line: entry needs at least two words.")


def validate(line: str) -> None:
    """Run every gate check in a fixed order."""
    check_not_empty(line)
    check_no_edge_whitespace(line)
    check_single_line(line)
    check_length(line)
    check_text_safe(line)
    check_word_count(line)


def resolve_output_path() -> str:
    """Return the output path, honouring OUTPUT_PATH, creating its dir.

    Also honours MAKEFUN_OUTPUT_DIR (the harness override) when
    OUTPUT_PATH is unset, so the harness and a manual run agree.
    """
    output_path = os.environ.get("OUTPUT_PATH")
    if not output_path:
        output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        output_path = os.path.join(output_dir, "entry.txt")
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    return output_path


def write_entry(line: str, output_path: str) -> None:
    """Write the line as UTF-8 text."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(line)


def verify_written(line: str, output_path: str) -> None:
    """Read the file back and prove it matches the line byte for byte."""
    with open(output_path, encoding="utf-8") as f:
        written = f.read()
    if written != line:
        raise SystemExit(
            "Write verification failed: entry file content does not match the line."
        )


def main() -> None:
    validate(LINE)
    output_path = resolve_output_path()
    write_entry(LINE, output_path)
    verify_written(LINE, output_path)
    print(f"wrote {len(LINE)} chars to {output_path}")


if __name__ == "__main__":
    main()
