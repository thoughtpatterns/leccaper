from runpy import run_module

cli = lambda: (run_module("leccaper.__main__", run_name="__main__", alter_sys=True), 0)[1]

__all__ = ["cli"]
