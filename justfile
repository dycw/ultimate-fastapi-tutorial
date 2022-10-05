local:
  uvicorn --host=0.0.0.0 --port=8001 --reload --app-dir=src \
    ultimate_fastapi_tutorial.main:app

deploy:
	sudo nginx -s reload
	sudo systemctl restart nginx.service
	poetry run gunicorn --bind=unix:///tmp/uvicorn.sock -w 2 --forwarded-allow-ips='*' -k uvicorn.workers.UvicornWorker app.main:app
