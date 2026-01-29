# Option B — Shared logging helper module (plan)

Purpose
- Make a small shared helper module so `ocgd.py` (and other code) can reuse the same logging/dual-output helpers.
- Two variants are presented: (1) move the existing `DualOutput` class into a shared module; (2) prefer a `logging`-module helper (recommended).

Files to add
- `scripts/logging_utils.py` — the helper module (either `DualOutput` or logging helpers)
- (optional) keep `tests/logging_sample.py` for examples (already present in this repo)

Why this pattern
- Centralizes logging code so it can be imported from anywhere.
- Keeps `ocgd.py` smaller and focused on functionality — it only imports a helper.
- Easier to test and maintain.

A. DualOutput (stdout-duplication) variant
1. Create `scripts/logging_utils.py` and add the `DualOutput` class (enable/disable/context-manager) exactly as used in `scripts/scratch_acs.py`.

Example content (DualOutput):

```python
import os
import sys
from typing import Optional

class DualOutput:
    def __init__(self, filename: Optional[str] = None):
        self._orig = None
        self._log = None
        self._filename = filename

    def _open_log(self, filename: str):
        path = os.path.join(os.getcwd(), "tests", os.path.basename(filename))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return open(path, "a", encoding="utf-8")

    def enable(self, filename: Optional[str] = None):
        if self._orig is not None:
            return
        fn = filename or self._filename or "output.log"
        self._orig = sys.stdout
        self._log = self._open_log(fn)
        sys.stdout = self

    def disable(self):
        if self._orig is None:
            return
        sys.stdout = self._orig
        try:
            if self._log:
                self._log.close()
        finally:
            self._orig = None
            self._log = None

    def __enter__(self):
        self.enable(self._filename)
        return self

    def __exit__(self, exc_type, exc, tb):
        self.disable()

    def write(self, message):
        if self._orig:
            self._orig.write(message)
        if self._log:
            try:
                self._log.write(message)
            except Exception:
                pass

    def flush(self):
        if self._orig:
            self._orig.flush()
        if self._log:
            try:
                self._log.flush()
            except Exception:
                pass
```

2. Modify `ocgd.py` (inside `OCgdm.__init__`):

```python
from scripts.logging_utils import DualOutput

class OCgdm:
    def __init__(self, ...):
        # existing init code ...
        self.dual_out = DualOutput()

    def enable_logging(self, filename: Optional[str] = None):
        self.dual_out.enable(filename)

    def disable_logging(self):
        self.dual_out.disable()
```

3. Usage in subclasses (they inherit `OCgdm`):

```python
self.enable_logging('step1.log')
print('this goes to terminal + tests/step1.log')
self.disable_logging()
```

Caveats: `DualOutput.enable()` replaces `sys.stdout` globally. Use carefully — enabling on one object affects print() calls across the whole process.


B. Recommended variant: `logging`-module helpers (per-class handlers)

1. Create `scripts/logging_utils.py` with the following helpers (or reuse the `tests/logging_sample.py` contents):

- `attach_file_handler(logger, filename)`
- `remove_handler(logger, handler)`
- `file_logging(logger, filename)` context manager

Example (simplified):

```python
import os
import logging
from contextlib import contextmanager

def _ensure_tests_dir():
    os.makedirs(os.path.join(os.getcwd(), 'tests'), exist_ok=True)

def attach_file_handler(logger: logging.Logger, filename: str):
    _ensure_tests_dir()
    path = os.path.join(os.getcwd(), 'tests', os.path.basename(filename))
    fh = logging.FileHandler(path, encoding='utf-8', mode='a')
    fmt = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    return fh

def remove_handler(logger: logging.Logger, handler: logging.Handler):
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
    h = attach_file_handler(logger, filename)
    try:
        yield
    finally:
        remove_handler(logger, h)
```

2. Modify `ocgd.py` (in `OCgdm.__init__`) to create a per-instance logger and convenience wrappers:

```python
import logging
from scripts.logging_utils import attach_file_handler, remove_handler, file_logging

class OCgdm:
    def __init__(self, ...):
        # existing init code ...
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        # add a console handler if needed

    def enable_file_logging(self, filename: str):
        # attach and return handler so caller can remove
        return attach_file_handler(self.logger, filename)

    def disable_file_logging(self, handler):
        remove_handler(self.logger, handler)

    def file_logging_context(self, filename: str):
        return file_logging(self.logger, filename)
```

3. Usage in subclasses:

Programmatic on/off:
```python
h = self.enable_file_logging('step1.log')
self.logger.info('logged to console + tests/step1.log')
self.disable_file_logging(h)
```

Context-managed:
```python
with self.file_logging_context('step2.log'):
    self.logger.info('this block logged to tests/step2.log')
```

Benefits: handlers are per-logger (not global). You can enable file logging for a single class/module without affecting other modules or `print()` calls. `logging` is thread-safe and supports rotation, levels, and formatting.


Testing & verification
- Run the provided `tests/logging_sample.py` to see examples and confirm logs are created under `tests/`:

```bash
python tests/logging_sample.py
```

- Or from Python prompt:

```bash
python -c "from scripts.logging_utils import attach_file_handler; import logging; logger=logging.getLogger('demo'); logger.setLevel(logging.INFO); h=attach_file_handler(logger,'demo.log'); logger.info('hello');"
```


Recommendation
- Prefer the `logging`-module helpers for production code and when you want localized/intermittent logging inside classes or methods.
- Only use `DualOutput` when you must capture arbitrary `print()` output globally (quick scripts or debugging), and be mindful of global side-effects.


If you want, I can implement Option B now by:
- creating `scripts/logging_utils.py` with the `logging` helpers (or the `DualOutput` class if you prefer), and
- adding small wrappers in `OCgdm` in `ocgd.py` to call these helpers.

Tell me whether to implement the `logging`-module helpers (recommended) or the `DualOutput` class in `scripts/logging_utils.py`, and I will follow up with the patch.
