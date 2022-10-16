from logging import INFO
from logging import basicConfig
from logging import getLogger

from beartype import beartype

from ultimate_fastapi_tutorial.db.init_db import init_db
from ultimate_fastapi_tutorial.db.session import SessionLocal


basicConfig(level=INFO)
LOGGER = getLogger(__name__)


@beartype
def init() -> None:
    db = SessionLocal()
    init_db(db)


@beartype
def main() -> None:
    LOGGER.info("Creating initial data")
    init()
    LOGGER.info("Initial data created")


if __name__ == "__main__":
    main()
