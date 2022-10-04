from typing import Any
from typing import cast

from beartype import beartype
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import status


RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/"
        + "cauliflower-and-tofu-curry-recipe.html",
    },
]


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")


api_router = APIRouter()


@api_router.get("/", status_code=status.HTTP_200_OK)
@beartype
def root() -> dict[str, Any]:
    """
    Root Get
    """

    return {"msg": "Hello, World!"}


@api_router.get("/recipe/{recipe_id}", status_code=status.HTTP_200_OK)
def fetch_recipe(*, recipe_id: int) -> dict[str, Any] | None:
    """
    Fetch a single recipe by ID
    """

    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]


@api_router.get("/search/", status_code=status.HTTP_200_OK)
def search_recipes(
    *, keyword: str | None = None, max_results: int | None = 10
) -> dict[str, Any]:
    """
    Search for recipes based on label keyword
    """

    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": RECIPES[:max_results]}

    results = [
        recipe
        for recipe in RECIPES
        if keyword.lower() in cast(str, recipe["label"]).lower()
    ]
    return {"results": results[:max_results]}


app.include_router(api_router)


if __name__ == "__main__":
    from uvicorn import run

    run(app, host="0.0.0.0", port=8001, log_level="debug")  # noqa: S104
