from typing import cast

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from ultimate_fastapi_tutorial.db.base_class import Base


class Recipe(Base):
    id = cast(int, Column(Integer, primary_key=True, index=True))
    label = cast(str, Column(String(256), nullable=False))
    url = cast(str, Column(String(256), index=True, nullable=True))
    source = cast(str, Column(String(256), nullable=True))
    submitter_id = cast(
        int, Column(Integer, ForeignKey("user.id"), nullable=True)
    )
    submitter = relationship("User", back_populates="recipes")
