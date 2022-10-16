from logging import INFO
from logging import WARN
from logging import basicConfig
from logging import getLogger

from beartype import beartype
from tenacity import after_log
from tenacity import before_log
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed

from ultimate_fastapi_tutorial.db.session import SessionLocal


basicConfig(level=INFO)
LOGGER = getLogger(__name__)


max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(LOGGER, INFO),
    after=after_log(LOGGER, WARN),
)
@beartype
def init() -> None:
    try:
        db = SessionLocal()
        _ = db.execute("SELECT 1")
    except Exception as error:
        LOGGER.error(error)
        raise error


@beartype
def main() -> None:
    LOGGER.info("Initializing service")
    init()
    LOGGER.info("Service finished initializing")


if __name__ == "__main__":
    main()
