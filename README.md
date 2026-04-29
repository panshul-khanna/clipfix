# clipfix

Fixes text copied from a terminal by removing visual hard-wraps.

When you copy a paragraph from a terminal (e.g. Claude Code inside VS Code), the terminal's line-wrapping gets baked into the clipboard — every line ends with a newline and continuation lines have leading spaces. `clipfix` strips those out and rejoins the text into clean paragraphs, while preserving real paragraph breaks and bulleted/numbered lists.

## Install

```bash
pip install clipfix
```

> macOS only — uses `pbpaste` / `pbcopy`.

## Usage

1. Copy broken text from the terminal.
2. Run `clipfix`.
3. Paste — the clipboard now contains clean text.

```bash
clipfix          # fix clipboard in-place
clipfix --test   # run self-tests
```

## What it does

- **Merges wrapped lines** within a paragraph into a single line
- **Preserves paragraph breaks** (blank lines between blocks)
- **Preserves list structure** — bulleted (`-`, `*`, `•`) and numbered (`1.`, `2)`) lists keep each item on its own line, with any wrapped continuations merged in

## Example

**Before** (copied from terminal):

```
When you copy a long paragraph from a terminal, line breaks and leading
   spaces from the terminal's word-wrap get included in the clipboard.
   clipfix merges those back into clean paragraphs.

- First bullet point that wraps onto
  the next line
- Second bullet point
```

**After** running `clipfix`:

```
When you copy a long paragraph from a terminal, line breaks and leading spaces from the terminal's word-wrap get included in the clipboard. clipfix merges those back into clean paragraphs.

- First bullet point that wraps onto the next line
- Second bullet point
```

## License

MIT
