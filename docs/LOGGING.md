# Logging in `ruf_common`

`ruf_common` uses the Python standard-library `logging` module and follows the
standard "library" contract:

- Every module logs to a named logger obtained with `logging.getLogger(__name__)`
  (e.g. `ruf_common.network`, `ruf_common.data`, `ruf_common.lfs`, ...). These are
  all descendants of the top-level `ruf_common` logger.
- The package installs a single `logging.NullHandler` on the `ruf_common` logger.
  The library **never** adds a real handler, never writes to a file, never calls
  `logging.basicConfig()`, and never touches the root logger.

The practical consequences:

- The library is **silent by default**. `INFO` and `DEBUG` messages are suppressed
  unless you opt in.
- `WARNING`/`ERROR`/`CRITICAL` will surface if — and only where — *your*
  application has configured logging. If your app has configured nothing at all,
  Python's built-in "last resort" prints `WARNING` and above to `stderr`. (This is
  standard-library behaviour, not something `ruf_common` does.)
- **You** decide entirely where logs go and how log files are managed. The library
  contributes log *records*; your handlers decide the destination, formatting,
  rotation, retention, etc.

## Turning logging on

Enabling is a one-liner: point a handler at the `ruf_common` logger and set the
level you want.

```python
import logging
import ruf_common

# Send ruf_common's logs to the console at DEBUG.
logging.basicConfig(level=logging.WARNING)               # your app's root config
logging.getLogger("ruf_common").setLevel(logging.DEBUG)  # this library, verbose
```

`basicConfig` installs a handler on the **root** logger; because `ruf_common`
loggers propagate, their records reach it. The per-library `setLevel` call is what
turns `INFO`/`DEBUG` on for this library specifically without making the rest of
your application verbose.

### Per-library and finer-grained control

The logger name gives you as much granularity as you want:

```python
import logging

logging.getLogger("ruf_common").setLevel(logging.INFO)          # whole library
logging.getLogger("ruf_common.network").setLevel(logging.DEBUG) # just one module
```

### Sending logs somewhere other than the console

Attach whatever handler you like directly to the library logger — a file, a
rotating file, syslog, etc. The library never does this for you:

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler("myapp.log", maxBytes=10_000_000, backupCount=3)
handler.setFormatter(logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s - %(message)s"
))

log = logging.getLogger("ruf_common")
log.setLevel(logging.DEBUG)
log.addHandler(handler)
```

### Turning it back off

```python
import logging
logging.getLogger("ruf_common").setLevel(logging.WARNING)  # silence INFO/DEBUG again
```

## Advanced: incorporating `ruf_common` logs into loguru

If your application uses [loguru](https://loguru.readthedocs.io/) instead of the
standard library, `ruf_common`'s records won't reach loguru automatically — the two
systems are separate. `ruf_common` emits standard-library records; loguru manages
its own sinks. You bridge them **once, in your application**, by adding a small
stdlib handler that forwards records into loguru (loguru's documented
`InterceptHandler` pattern). `ruf_common` needs no changes — it just keeps emitting
records.

```python
import logging
import sys
from loguru import logger

# --- your application's own loguru configuration (sinks, files, formats) ---
logger.remove()                                   # drop loguru's default handler
logger.add(sys.stderr, level="INFO")              # console
logger.add("app.log", level="DEBUG",              # rotating file, managed by YOU
           rotation="10 MB", retention="1 week", compression="zip")

# --- bridge: forward stdlib records (from ruf_common, etc.) into loguru ---
class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())

# Route just this library into loguru, and choose how verbose it should be:
lib = logging.getLogger("ruf_common")
lib.setLevel(logging.DEBUG)          # let DEBUG/INFO through for ruf_common
lib.addHandler(InterceptHandler())   # send its records to your loguru sinks
lib.propagate = False                # optional: don't also hit the stdlib root logger
```

From here on, everything `ruf_common` logs flows into whatever loguru sinks your
application configured (console, `app.log`, etc.), formatted and rotated entirely
by your application's rules.

> Incorporating `ruf_common` into **other** logging frameworks is typically the
> same shape: because `ruf_common` emits ordinary standard-library log records, any
> framework that can consume them works. For example, `structlog` reads stdlib
> records via its `ProcessorFormatter`; you attach that formatter's handler to the
> `ruf_common` logger exactly as shown above. Only the "install a handler that
> adapts stdlib records into framework X" step differs.
