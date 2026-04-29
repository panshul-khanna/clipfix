"""clipfix – remove visual hard-wraps from terminal-copied text."""

import re
import subprocess
import sys


_LIST_ITEM = re.compile(r"^[ \t]*(?:[-*+•][ \t]|\d+[.)]\s)")


def fix_text(text: str) -> str:
    raw_blocks = re.split(r"(\n[ \t]*\n+)", text)
    result_parts: list[str] = []
    for chunk in raw_blocks:
        if re.fullmatch(r"\n[ \t]*\n+", chunk):
            result_parts.append(chunk)
            continue
        result_parts.append(_fix_block(chunk))
    return "".join(result_parts)


def _fix_block(block: str) -> str:
    lines = block.split("\n")

    if not any(_LIST_ITEM.match(ln) for ln in lines if ln.strip()):
        # Plain paragraph — merge all lines into one.
        parts = [ln.strip() for ln in lines if ln.strip()]
        return " ".join(parts)

    # List block — keep each item on its own line but merge wrapped
    # continuation lines (lines that don't start a new list item) into
    # the item above them.
    items: list[str] = []
    for line in lines:
        if _LIST_ITEM.match(line):
            items.append(line.rstrip())
        elif items:
            stripped = line.strip()
            if stripped:
                items[-1] += " " + stripped
        else:
            # Content before the first list item — keep as-is.
            items.append(line.rstrip())

    return "\n".join(items)


def read_clipboard() -> str:
    result = subprocess.run(["pbpaste"], capture_output=True, text=True)
    result.check_returncode()
    return result.stdout


def write_clipboard(text: str) -> None:
    subprocess.run(["pbcopy"], input=text, text=True, check=True)


def main() -> None:
    if "--test" in sys.argv:
        _run_tests()
        return

    original = read_clipboard()
    fixed = fix_text(original)
    write_clipboard(fixed)

    lines_before = original.count("\n")
    lines_after = fixed.count("\n")
    print(f"Done. Lines: {lines_before} → {lines_after}")


def _run_tests() -> None:
    cases = [
        (
            "single wrapped paragraph",
            "This is a long sentence that got\n   hard-wrapped by the terminal\nand continues here.",
            "This is a long sentence that got hard-wrapped by the terminal and continues here.",
        ),
        (
            "two paragraphs stay separate",
            "First paragraph that\nwraps here.\n\nSecond paragraph that\nalso wraps.",
            "First paragraph that wraps here.\n\nSecond paragraph that also wraps.",
        ),
        (
            "bulleted list merges continuations",
            "- First item that wraps\n  onto the next line\n- Second item",
            "- First item that wraps onto the next line\n- Second item",
        ),
        (
            "numbered list merges continuations",
            "1. Step one\n2. Step two that\n   wraps here\n3. Step three",
            "1. Step one\n2. Step two that wraps here\n3. Step three",
        ),
        (
            "paragraph then list",
            "Some intro text that\nwraps here.\n\n- bullet one\n- bullet two",
            "Some intro text that wraps here.\n\n- bullet one\n- bullet two",
        ),
    ]

    passed = failed = 0
    for desc, inp, expected in cases:
        got = fix_text(inp)
        if got == expected:
            print(f"  PASS  {desc}")
            passed += 1
        else:
            print(f"  FAIL  {desc}")
            print(f"         expected: {expected!r}")
            print(f"         got:      {got!r}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed.")
    sys.exit(0 if failed == 0 else 1)
