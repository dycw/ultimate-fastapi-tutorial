from typing import Any
from typing import cast

from beartype import beartype
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status

from ultimate_fastapi_tutorial.recipe_data import RECIPES
from ultimate_fastapi_tutorial.schemas import Recipe
from ultimate_fastapi_tutorial.schemas import RecipeCreate
from ultimate_fastapi_tutorial.schemas import RecipeSearchResults


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")


api_router = APIRouter()


@api_router.get("/", status_code=status.HTTP_200_OK)
@beartype
def root() -> dict[str, Any]:
    """
    Root Get
    """

    return {"msg": "Hello, World!"}


@api_router.get(
    "/recipe/{recipe_id}", status_code=status.HTTP_200_OK, response_model=Recipe
)
def fetch_recipe(*, recipe_id: int) -> dict[str, Any]:
    """
    Fetch a single recipe by ID
    """

    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@api_router.get(
    "/search/",
    status_code=status.HTTP_200_OK,
    response_model=RecipeSearchResults,
)
def search_recipes(
    *, keyword: str | None = None, max_results: int | None = 10
) -> dict[str, Any]:
    """
    Search for recipes based on label keyword
    """

    if keyword:
        results = [
            recipe
            for recipe in RECIPES
            if keyword.lower() in cast(str, recipe["label"]).lower()
        ]
    else:
        results = RECIPES
    return {"results": results[:max_results]}


@api_router.post(
    "/recipe/", status_code=status.HTTP_201_CREATED, response_model=Recipe
)
def create_recipe(*, recipe_in: RecipeCreate) -> Recipe:
    """
    Create a new recipe (in memory only)
    """

    new_entry_id = len(RECIPES) + 1
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url,
    )
    RECIPES.append(recipe_entry.dict())
    return recipe_entry


app.include_router(api_router)


if __name__ == "__main__":
    from uvicorn import run

    run(app, host="0.0.0.0", port=8001, log_level="debug")  # noqa: S104
