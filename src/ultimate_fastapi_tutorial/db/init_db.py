from logging import getLogger
from typing import cast

from beartype import beartype
from pydantic import EmailStr
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from ultimate_fastapi_tutorial.crud.recipe import CRUDRecipe
from ultimate_fastapi_tutorial.crud.user import CRUDUser
from ultimate_fastapi_tutorial.db import base
from ultimate_fastapi_tutorial.db.base_class import Base
from ultimate_fastapi_tutorial.db.session import engine
from ultimate_fastapi_tutorial.recipe_data import RECIPES
from ultimate_fastapi_tutorial.schemas.recipe import RecipeCreate
from ultimate_fastapi_tutorial.schemas.user import UserCreate


LOGGER = getLogger(__name__)


FIRST_SUPERUSER = "admin@recipeapi.com"


_ = base  # ensure all models are imported


@beartype
def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line:

    # >>> Base.metadata.create_all(bind=engine)

    if FIRST_SUPERUSER:
        if (user := CRUDUser.read_by_email(db, FIRST_SUPERUSER)) is None:
            user_in = UserCreate(
                first_name="Initial",
                surname="Super User",
                email=cast(EmailStr, FIRST_SUPERUSER),
                is_superuser=True,
            )
            user = CRUDUser.create(db, user_in)
        else:
            LOGGER.warning(
                "Skipping creating superuser. User with email "
                + f"{FIRST_SUPERUSER} already exists. "
            )
        if not user.recipes:
            for recipe in RECIPES:
                recipe_in = RecipeCreate(
                    label=cast(str, recipe["label"]),
                    source=cast(str, recipe["source"]),
                    url=cast(HttpUrl, recipe["url"]),
                    submitter_id=user.id,
                )
                _ = CRUDRecipe.create(db, recipe_in)
    else:
        LOGGER.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            + "provided as an env variable. "
            + "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
