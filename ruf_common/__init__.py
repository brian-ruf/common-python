import logging

# The library emits log records but installs no handler of its own, so it stays
# silent unless the calling application configures logging. Consumers enable it
# with e.g. ``logging.getLogger("ruf_common").setLevel(logging.INFO)`` plus a
# handler of their choosing. See docs/LOGGING.md.
logging.getLogger("ruf_common").addHandler(logging.NullHandler())

from . import country_code_converter
from . import data
from . import database
from . import helper
from . import html_to_markdown
from . import lfs
from . import network
from . import stats
from . import timezone_lookup
from . import xml_formatter

__all__ = [
    "data",
    "database",
    "lfs",
    "helper",
    "network",
    "stats",
    "country_code_converter",
    "html_to_markdown",
    "timezone_lookup",
    "xml_formatter"
]
