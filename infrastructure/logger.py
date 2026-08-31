import logging

logging.basicConfig(
    filename="auditoria.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    encoding="utf-8",
)

logger = logging.getLogger("auditoria")