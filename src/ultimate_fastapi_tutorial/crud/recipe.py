from ultimate_fastapi_tutorial.crud.base import CRUDBase
from ultimate_fastapi_tutorial.models.recipe import Recipe
from ultimate_fastapi_tutorial.schemas.recipe import RecipeCreate
from ultimate_fastapi_tutorial.schemas.recipe import RecipeUpdate


class _CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    ...


CRUDRecipe = _CRUDRecipe(Recipe)
