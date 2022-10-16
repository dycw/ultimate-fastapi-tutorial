from typing import Any
from typing import cast

from sqlalchemy.orm import as_declarative
from sqlalchemy.orm import declared_attr
from utilities.class_name import get_class_name
from utilities.inflection import snake_case


class_registry = {}


@as_declarative(class_registry=class_registry)
class _Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return snake_case(get_class_name(cls))


Base = cast(Any, _Base)
