from typing import Any

from beartype import beartype
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from utilities.git import get_repo_root

from ultimate_fastapi_tutorial.crud.recipe import CRUDRecipe
from ultimate_fastapi_tutorial.deps import get_db
from ultimate_fastapi_tutorial.schemas.recipe import Recipe
from ultimate_fastapi_tutorial.schemas.recipe import RecipeCreate
from ultimate_fastapi_tutorial.schemas.recipe import RecipeSearchResults


ROOT = get_repo_root()
TEMPLATES = Jinja2Templates(directory=ROOT.joinpath("src", "templates"))


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")


api_router = APIRouter()


@api_router.get("/", status_code=status.HTTP_200_OK)
@beartype
def root(*, request: Request, db: Session = Depends(get_db)) -> Response:
    """
    Root Get
    """

    recipes = CRUDRecipe.read_multi(db)
    return TEMPLATES.TemplateResponse(
        "index.html", {"request": request, "recipes": recipes}
    )


@api_router.get(
    "/recipe/{recipe_id}", status_code=status.HTTP_200_OK, response_model=Recipe
)
@beartype
def fetch_recipe(
    *, db: Session = Depends(get_db), recipe_id: int
) -> dict[str, Any]:
    """
    Fetch a single recipe by ID
    """

    if (result := CRUDRecipe.read(db, recipe_id)) is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with ID {recipe_id} not found",
        )
    else:
        return result


@api_router.get(
    "/search/",
    status_code=status.HTTP_200_OK,
    response_model=RecipeSearchResults,
)
@beartype
def search_recipes(
    *,
    db: Session = Depends(get_db),
    max_results: int | None = 10,
    keyword: str | None = None,
) -> dict[str, Any]:
    """
    Search for recipes based on label keyword
    """

    recipes = CRUDRecipe.read_multi(db, limit=max_results)
    if keyword is not None:
        recipes = [
            recipe
            for recipe in recipes
            if keyword.lower() in recipe.label.lower()
        ]
    return {"results": recipes}


@api_router.post(
    "/recipe/", status_code=status.HTTP_201_CREATED, response_model=Recipe
)
@beartype
def create_recipe(
    *, db: Session = Depends(get_db), recipe: RecipeCreate
) -> Recipe:
    """
    Create a new recipe (in memory only)
    """

    return CRUDRecipe.create(db, recipe)


app.include_router(api_router)


if __name__ == "__main__":
    from uvicorn import run

    run(app, host="0.0.0.0", port=8001, log_level="debug")  # noqa: S104
