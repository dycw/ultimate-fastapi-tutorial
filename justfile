local:
  uvicorn --host=0.0.0.0 --port=8001 --reload --app-dir=src \
    ultimate_fastapi_tutorial.main:app

deploy:
  sudo nginx -s reload
  sudo systemctl restart nginx.service
  gunicorn --bind=unix:///tmp/uvicorn.sock --workers=2 \
    --worker-class=uvicorn.workers.UvicornWorker --chdir=src \
    --forwarded-allow-ips='*' ultimate_fastapi_tutorial.main:app
