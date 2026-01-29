"""
logging_sample.py

Small helper utilities demonstrating how to attach a file handler to a Python
`logging.Logger` for short-lived or localized file logging. This reproduces the
"dual output" idea (terminal + file) but in a safe, non-invasive way using the
standard `logging` module.

Usage:
- Standalone: import the helpers and call `attach_file_handler` / `remove_handler`.
- Context-managed: use `file_logging(logger, filename)` as a context manager.
- Integrate in classes: create `self.logger = logging.getLogger(__class__.__name__)`
  in `__init__`, then call `attach_file_handler(self.logger, filename)` when you
  want file logging for a segment of code.

Files are written under the repository `tests/` directory (created if missing).

Examples are provided in the `main()` function and in the class `ExampleWorker`.
"""

from __future__ import annotations
import os
import logging
from contextlib import contextmanager
from typing import Optional


def _ensure_tests_dir() -> str:
    """Ensure the repository `tests/` directory exists and return its path.

    Uses the current working directory as the project root. If you run scripts
    from a different working directory, set `os.chdir()` accordingly or modify
    this helper to use a fixed repo location.
    """
    path = os.path.join(os.getcwd(), "tests")
    os.makedirs(path, exist_ok=True)
    return path


def attach_file_handler(logger: logging.Logger, filename: str) -> logging.Handler:
    """Attach a `FileHandler` that writes to `tests/<filename>`.

    Returns the handler so callers may remove it later with `remove_handler()`.
    """
    _ensure_tests_dir()
    path = os.path.join(os.getcwd(), "tests", os.path.basename(filename))
    fh = logging.FileHandler(path, encoding="utf-8", mode="a")
    fmt = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    return fh


def remove_handler(logger: logging.Logger, handler: logging.Handler) -> None:
    """Remove and close a handler previously attached to `logger`.

    Safe to call even if the handler has already been removed/closed.
    """
    try:
        logger.removeHandler(handler)
    except Exception:
        pass
    try:
        handler.close()
    except Exception:
        pass


@contextmanager
def file_logging(logger: logging.Logger, filename: str):
    """Context manager which attaches a file handler for the duration of the
    `with` block and removes it on exit.

    Example:
        with file_logging(logger, "step.log"):
            logger.info("This message goes to console + tests/step.log")
    """
    handler = attach_file_handler(logger, filename)
    try:
        yield
    finally:
        remove_handler(logger, handler)


# ----------------------- Example integration -----------------------
class ExampleWorker:
    """Simple class demonstrating how to integrate the helper into a class.

    - Create `self.logger` in `__init__`.
    - Use `attach_file_handler` / `remove_handler` for programmatic on/off.
    - Or use `file_logging()` as a context manager for localized blocks.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        # Configure logger level and console handler if necessary
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setFormatter(logging.Formatter("%(name)s: %(message)s"))
            self.logger.addHandler(ch)

    def do_task(self):
        self.logger.info("doing task (console only)")

    def do_task_with_file(self, fname: str):
        h = attach_file_handler(self.logger, fname)
        try:
            self.logger.info("doing task (also logged to file)")
        finally:
            remove_handler(self.logger, h)

    def do_task_with_context(self, fname: str):
        with file_logging(self.logger, fname):
            self.logger.info("doing task (context-managed file logging)")


# ----------------------- Standalone examples -----------------------

def main():
    # Basic logger used at module level or in scripts
    logger = logging.getLogger("sample")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(name)s: %(message)s"))
        logger.addHandler(ch)

    print("Running logging_sample examples.\nLogs will be written under tests/")

    # Programmatic attach / remove
    h = attach_file_handler(logger, "sample_prog.log")
    logger.info("programmatic: this goes to console + tests/sample_prog.log")
    remove_handler(logger, h)
    logger.info("after remove: console only")

    # Context manager
    with file_logging(logger, "sample_ctx.log"):
        logger.info("context: this goes to console + tests/sample_ctx.log")

    # Class integration
    worker = ExampleWorker()
    worker.do_task()
    worker.do_task_with_file("worker_prog.log")
    worker.do_task_with_context("worker_ctx.log")

    print("Examples complete. Check tests/ for created log files.")


if __name__ == "__main__":
    main()
