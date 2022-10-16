from collections.abc import Iterator

from sqlalchemy.orm import Session

from ultimate_fastapi_tutorial.db.session import SessionLocal


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    db.current_user_id = None  # type: ignore
    try:
        yield db
    finally:
        db.close()
