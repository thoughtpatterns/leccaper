from logging import basicConfig, getLogger, INFO
from collections.abc import Callable
from typing import NoReturn

basicConfig(level=INFO, format="[%(levelname)s] %(message)s")
log = getLogger(__name__)

die: Callable[[str], NoReturn] = lambda x: (log.error(x), exit(1))[1]
