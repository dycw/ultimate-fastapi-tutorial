local:
  uvicorn --host=0.0.0.0 --port=8001 --reload --app-dir=src \
    ultimate_fastapi_tutorial.main:app
