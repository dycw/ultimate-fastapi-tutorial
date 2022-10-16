from beartype import beartype
from sqlalchemy.orm import Session

from ultimate_fastapi_tutorial.crud.base import CRUDBase
from ultimate_fastapi_tutorial.models.user import User
from ultimate_fastapi_tutorial.schemas.user import UserCreate
from ultimate_fastapi_tutorial.schemas.user import UserUpdate


class _CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    @beartype
    def read_by_email(self, db: Session, email: str, /) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @beartype
    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


CRUDUser = _CRUDUser(User)
