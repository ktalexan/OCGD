# Plan A — Run `logging_sample.py` standalone

This document explains how to run the example script `tests/logging_sample.py` that demonstrates the `logging`-module helpers (programmatic attach/remove and context-managed file logging). It also lists available options and copy/paste commands for both Windows and Unix-like shells.

Notes
- The script writes log files under a `tests/` directory created under the process current working directory (`os.getcwd()`). Run commands from your repository root to keep logs inside the repository `tests/` folder.
- No external dependencies are required — only Python standard library (`logging`, `os`, `contextlib`).

Run the full example
- From the repository root run:

```bash
python tests/logging_sample.py
```

- This runs `main()` which executes all examples and creates these log files (under `tests/`):
  - `sample_prog.log`
  - `sample_ctx.log`
  - `worker_prog.log`
  - `worker_ctx.log`

Simple one-off examples
- Run a programmatic attach/remove example directly from the shell (one-liner):

Unix / PowerShell compatible:
```bash
python -c "from tests.logging_sample import attach_file_handler; import logging; logger=logging.getLogger('demo'); logger.setLevel(logging.INFO); h=attach_file_handler(logger,'demo.log'); logger.info('hello from one-liner');"
```

Windows cmd (escape differently):
```cmd
python -c "from tests.logging_sample import attach_file_handler; import logging; logger=logging.getLogger('demo'); logger.setLevel(logging.INFO); h=attach_file_handler(logger,'demo.log'); logger.info('hello from one-liner')"
```

Run the context-manager example from a heredoc (Unix):
```bash
python - <<'PY'
from tests.logging_sample import file_logging
import logging
logger = logging.getLogger('demo2')
logger.setLevel(logging.INFO)
with file_logging(logger, 'demo_ctx.log'):
    logger.info('logged inside context')
PY
```

Windows PowerShell equivalent:
```powershell
python - <<'PY'
from tests.logging_sample import file_logging
import logging
logger = logging.getLogger('demo2')
logger.setLevel(logging.INFO)
with file_logging(logger, 'demo_ctx.log'):
    logger.info('logged inside context')
PY
```

Invoke examples programmatically (no file edits)
- Programmatic example using the `ExampleWorker` class from the module:

```bash
python -c "from tests.logging_sample import ExampleWorker; w=ExampleWorker(); w.do_task_with_file('worker_cli.log')"
```

- Context-managed example from `ExampleWorker`:

```bash
python -c "from tests.logging_sample import ExampleWorker; w=ExampleWorker(); w.do_task_with_context('worker_cli_ctx.log')"
```

Options and customization
- Choose log filenames: each helper call accepts a filename. Files are written to `tests/<filename>` — only the basename is used.
- Change working directory: if you run the script with a different `cwd`, logs are created under that `cwd/tests/`. To force logs into repository `tests/`, `cd` to the repository root first.

Examples:
```bash
cd /path/to/OCGD
python tests/logging_sample.py
# or
python -c "from tests.logging_sample import attach_file_handler, remove_handler; ..."
```

Integration notes
- The `logging_sample.py` contains `ExampleWorker` to show how to integrate a per-class logger:
  - In `__init__`: create `self.logger = logging.getLogger(self.__class__.__name__)`
  - Use `attach_file_handler(self.logger, 'name.log')` and `remove_handler(...)` for programmatic on/off.
  - Use `with file_logging(self.logger, 'name.log'):` for scoped logging.

File locations
- Example script: `tests/logging_sample.py`
- Generated logs: `tests/*.log`

Troubleshooting
- If no log files appear: confirm you ran the script from the intended working directory (`pwd` / `cd` accordingly).
- Windows users: PowerShell and cmd quoting differ — if a `-c` one-liner fails, copy the block into a temporary Python file and run that file.

Next steps
- If you want me to wire these helpers into `ocgd.py` (Option B), I can create `scripts/logging_utils.py` and add small wrapper methods on `OCgdm` to expose per-instance logging. Ask when ready.
