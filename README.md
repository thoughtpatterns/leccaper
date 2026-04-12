# leccaper

A University of Michigan lecture capture download tool, derivative of
[`leccapdl`](https://github.com/brenfwd/leccapdl). We use less automation on the
navigation to the lecture capture page, to avoid some race conditions which can
otherwise arise.

## Usage

`leccaper` requires `uv`; `pip` can likely be used, but is untested.

```bash
uv venv
. ./.venv/bin/activate
uv sync
leccaper
```

See `leccaper --help` for usage; the default is to download only the newest
lecture for a course.

## vf, vff

A couple of scripts, `vf` and `vff`, are bundled, and can be found in `./bin/`.
These are to convert a lecture video into a folder of slides, e.g.,

```bash
leccaper --number 1 ./captures/chem521/                      # Download the newest CHEM 521 lecture; say, lecture 13.
vf --width 960 ./captures/chem521/13.mp4 ./slides/chem521/13 # Split the lecture capture into deduplicated slides.
```

We use `--width 960` here, as the slideshow in the lecture capture takes up the
left 960 pixels. See `vf --help` for usage.

`vff` is simply a wrapper around `vf`, and can be used on a folder of lecture
videos, e.g.,

```bash
leccaper --number 1 ./captures/chem521/               # Download the newest CHEM 521 lecture, as before.
vff ./captures/chem521/ ./slides/chem521/ --width 960 # Convert each capture in the input. Note the new argument order!
```

`vf` uses FFmpeg's `mpdecimate` filter; you can read the documentation
at the top of the script for more information. It essentially scans for
pixel differences, to discard consecutive slides which are too similar. This
works pretty well to discard, e.g., laser pointer movements, but keeps slide
transitions (even relatively subtle ones, like an arrow's appearance). If a
video is played in the lecture slides, we cannot remove it, so this may balloon
the number of slides generated; these images should be removed manually.
