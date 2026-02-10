# leccaper

A University of Michigan lecture capture download tool, derivative of
[`leccapdl`](https://github.com/brenfwd/leccapdl). We use less automation on the
navigation to the lecture capture page, to avoid some race conditions which can
otherwise arise.

## Usage

Requires `uv`; `pip` can likely be used, but is untested.

```bash
uv venv ; . ./.venv/bin/activate ; uv sync ; leccaper
```

The tool will give prompts for input as necessary (i.e., for output directory,
etc.).
