from pydantic import BaseModel
from pydantic import HttpUrl


class Recipe(BaseModel):
    id: int
    label: str
    source: str
    url: HttpUrl


class RecipeSearchResults(BaseModel):
    results: list[Recipe]


class RecipeCreate(BaseModel):
    label: str
    source: str
    url: HttpUrl
    submitter_id: int
