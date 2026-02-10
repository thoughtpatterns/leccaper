from leccaper.log import log
from leccaper.util import download, drive, input, leccap
from pathlib import Path

# pyright: reportAny=false

out = Path.cwd() / "leccaper" / input("enter a name for the output directory... ")
out.mkdir(parents=True, exist_ok=True)
log.info(f"output directory set to '{out}'")

session, captures = drive()
g = session.get

for i, capture in enumerate(captures):
    log.info(f"started fetch {i + 1} of {len(captures)}...")

    if not (slug := capture.get("url", "")):
        log.warning("failed to find slug; skipped")
        continue

    slug = slug.split("/")[-1]

    try:
        metadata = g(f"{leccap}/player/api/product/?rk={slug}").json()
    except Exception as e:
        log.warning(f"failed to fetch metadata: {e}; skipped")
        continue

    h = metadata.get

    if not (products := h("info", {}).get("products", [])):
        log.warning("failed to fetch products via API (not found); skipped")
        continue

    if not (tag := products[0].get("movie_exported_name")):
        log.warning("failed to fetch video from metadata; skipped")
        continue

    target = f"https:{h('mediaPrefix')}{h('sitekey')}/{tag}.mp4"
    download(session, target, out / f"{i + 1}.mp4")

    log.info("video download successful!")
    log.info("fetch for subtitles started...")

    if not (key := h("recordingkey")):
        log.warning("failed to get access to subtitles; skipped")
        continue

    try:
        if (subtitles := g(f"{leccap}/player/api/webvtt/?rk={key}")).status_code == 200:
            with (out / f"{i + 1}.vtt").open("w") as f:
                _ = f.write(subtitles.text)
                log.info("subtitle download successful!")
    except Exception:
        log.warning("failed to get subtitles; skipped")
        pass

log.info("all downloads complete!")
