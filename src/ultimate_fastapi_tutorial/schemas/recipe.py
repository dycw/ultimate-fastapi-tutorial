from collections.abc import Sequence

from pydantic import BaseModel
from pydantic import HttpUrl


class RecipeBase(BaseModel):
    label: str
    source: str
    url: HttpUrl


class RecipeCreate(RecipeBase):
    submitter_id: int


class RecipeUpdate(RecipeBase):
    ...


# Properties shared by models stored in DB
class RecipeInDBBase(RecipeBase):
    id: int
    submitter_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Recipe(RecipeInDBBase):
    pass


# Properties properties stored in DB
class RecipeInDB(RecipeInDBBase):
    pass


class RecipeSearchResults(BaseModel):
    results: Sequence[Recipe]
