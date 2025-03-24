db:
	docker run --name hw06 -p 5432:5432 -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -d postgres
migration:
	alembic revision --autogenerate -m 'Init'
migrate:
	alembic upgrade head

sl:
	python my_select.py
f:
	black . --exclude=venv