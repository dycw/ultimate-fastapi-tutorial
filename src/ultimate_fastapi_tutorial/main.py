from typing import Any

from beartype import beartype
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import status


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")


api_router = APIRouter()


@api_router.get("/", status_code=status.HTTP_200_OK)
@beartype
def root() -> dict[str, Any]:
    """
    Root Get
    """

    return {"msg": "Hello, World!"}


app.include_router(api_router)


if __name__ == "__main__":
    from uvicorn import run

    run(app, host="0.0.0.0", port=8001, log_level="debug")  # noqa: S104
