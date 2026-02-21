from argparse import ArgumentParser
from builtins import input as _input
from collections.abc import Callable
from json import JSONDecodeError, loads
from leccaper.log import die, log
from pathlib import Path
from re import DOTALL, Match, compile
from requests import Session
from selenium.webdriver import Chrome, ChromeOptions
from tqdm import tqdm
from typing import Any, Final, NamedTuple, cast

leccap: Final = "https://leccap.engin.umich.edu/leccap"

type Da = dict[Any, Any]  # pyright: ignore[reportExplicitAny]
type Ds = dict[str, Any]  # pyright: ignore[reportExplicitAny]

_short = compile(r"[^\w\-\.]+")
_var = compile(r"var recordings = (\[.*?\]);")

input: Callable[[str], str] = lambda x: _input("[INPUT] " + x)
short: Callable[[str], str] = lambda x: _short.sub("_", x).strip()
var: Callable[[str], Match[str] | None] = lambda x: _var.search(x, DOTALL)


class Drive(NamedTuple):
    session: Session
    captures: list[Ds]


class Options(NamedTuple):
    path: Path
    number: int


def download(session: Session, url: str, path: Path) -> None:
    if path.exists():
        log.info(f"will not download to existing path, '{path.name}'")
        raise FileExistsError

    try:
        response = session.get(url, stream=True)
        response.raise_for_status()

        if not (total := response.headers.get("content-length")):
            log.error("failed to fetch content length; skipped")
            return

        total = int(total)
        block = 1 << 20

        with tqdm(total=total, unit="B", unit_scale=True, leave=False) as bar:
            with path.open("wb") as f:
                for data in response.iter_content(block):  # pyright: ignore[reportAny]
                    _ = bar.update(len(data))  # pyright: ignore[reportAny]
                    _ = f.write(data)  # pyright: ignore[reportAny]

    except Exception as e:
        log.error(f"failed to download '{path.name}': {e}; skipped")


def drive() -> Drive:
    _agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    f: Callable[[Session], None] = lambda x: x.headers.update({"User-Agent": _agent})
    g: Callable[[Session, Da], None] = lambda x, y: cast("None", x.cookies.set(y["name"], y["value"]))  # pyright: ignore[reportAny, reportUnknownMemberType]

    try:
        driver = Chrome(ChromeOptions())
        driver.get(leccap)

        _ = input(
            "log into the opened chrome window, then navigate to the desired course page"
            + "; when at the correct page, press the RETURN key at this prompt... "
        )

        captures = read(driver.page_source)
        log.info(f"found {len(captures)} captures...")

        f(session := Session())
        [g(session, c) for c in driver.get_cookies()]  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType, reportUnknownVariableType]

    except Exception as e:
        die(f"failed to obtain session cookie: {e}")

    driver.quit()
    return Drive(session, captures)


def options() -> Options:
    parser = ArgumentParser(prog="leccaper", description="a download tool for leccap")
    _ = parser.add_argument("-n", "--number", default=1, type=int, help="number of lectures to save, from latest")
    _ = parser.add_argument("path", type=Path, help="directory in which to save lecture captures")
    options = parser.parse_args()
    return Options(options.path, options.number)  # pyright: ignore[reportAny]


def read(html: str) -> list[Ds]:
    if not (match := var(html)):
        die("failed to find lecture capture metadata in page source")

    try:
        return cast("list[Ds]", loads(match.group(1)))
    except JSONDecodeError:
        die("failed to parse lecture capture metadata")
