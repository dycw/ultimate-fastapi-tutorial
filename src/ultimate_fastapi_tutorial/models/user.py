from typing import cast

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from ultimate_fastapi_tutorial.db.base_class import Base


class User(Base):
    id = cast(int, Column(Integer, primary_key=True, index=True))
    first_name = cast(str, Column(String(256), nullable=True))
    surname = cast(str, Column(String(256), nullable=True))
    email = cast(str, Column(String, index=True, nullable=False))
    is_superuser = cast(bool, Column(Boolean, default=False))
    recipes = relationship(
        "Recipe",
        cascade="all,delete-orphan",
        back_populates="submitter",
        uselist=True,
    )
