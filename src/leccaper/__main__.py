from leccaper.log import log
from leccaper.util import download, drive, leccap, options
from collections.abc import Callable

# pyright: reportAny=false, reportUnknownMemberType=false, reportUnknownVariableType=false

path, start, end = options()
path.mkdir(parents=True, exist_ok=True)

session, captures = drive()
total = len(captures)

clamp: Callable[[int | None, int], int] = lambda x, y: y if x is None else max(0, total + x if x < 0 else x)

start = clamp(start, 0)
end = clamp(end, total)

captures = captures[start:end]

g = session.get

for i, capture in enumerate(captures, start=start):
    log.info(f"started fetch for capture {i} ({total} total)...")

    if not (slug := capture.get("url", None)):
        log.warning("failed to find slug; skipped")
        continue

    slug = slug.split("/")[-1]

    try:
        metadata = g(f"{leccap}/player/api/product/?rk={slug}").json()
    except Exception as e:
        log.warning(f"failed to fetch metadata: {e}; skipped")
        continue

    h = metadata.get

    if not (products := h("info", None).get("products", None)):
        log.warning("failed to fetch products via API (not found); skipped")
        continue

    if not (tag := products[0].get("movie_exported_name")):
        log.warning("failed to fetch video from metadata; skipped")
        continue

    target = f"https:{h('mediaPrefix')}{h('sitekey')}/{tag}.mp4"

    try:
        download(session, target, path / f"{i}.mp4")
    except FileExistsError:
        continue

    log.info("video download successful!")
    log.info("fetch for subtitles started...")

    if not (key := h("recordingkey")):
        log.warning("failed to get access to subtitles; skipped")
        continue

    try:
        if (subtitles := g(f"{leccap}/player/api/webvtt/?rk={key}")).status_code == 200:
            with (path / f"{i}.vtt").open("w") as f:
                _ = f.write(subtitles.text)
                log.info("subtitle download successful!")
    except Exception as e:
        log.warning(f"failed to get subtitles: {e}; skipped")
        pass

log.info("all downloads complete!")
