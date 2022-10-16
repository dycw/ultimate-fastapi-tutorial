from collections.abc import Mapping
from typing import Any
from typing import Generic
from typing import TypeVar

from beartype import beartype
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ultimate_fastapi_tutorial.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    @beartype
    def __init__(self, model: type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """

        super().__init__()
        self.model = model

    @beartype
    def create(self, db: Session, schema: CreateSchemaType, /) -> ModelType:
        as_dict = jsonable_encoder(schema)
        as_model = self.model(**as_dict)
        db.add(as_model)
        db.commit()
        db.refresh(as_model)
        return as_model

    @beartype
    def read(self, db: Session, id: Any, /) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == id).one_or_none()

    @beartype
    def read_multi(
        self, db: Session, /, *, skip: int = 0, limit: int | None = 100
    ) -> list[ModelType]:
        query = db.query(self.model).offset(skip)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    @beartype
    def update(
        self,
        db: Session,
        model: ModelType,
        update: UpdateSchemaType | Mapping[str, Any],
        /,
    ) -> ModelType:
        as_dict = jsonable_encoder(model)
        if isinstance(update, Mapping):
            update_as_dict = update
        else:
            update_as_dict = update.dict(exclude_unset=True)
        for field in set(as_dict) & set(update_as_dict):
            setattr(model, field, update_as_dict[field])
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

    @beartype
    def delete(self, db: Session, id: int, /) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
