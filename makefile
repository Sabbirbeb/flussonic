build:
	docker build . -t flussonic-app:local

up:
	docker compose up -d

down:
	docker compose down

restart:
	make down && make up

lint:
	docker compose exec app ruff format .
	docker compose exec app ruff check . --fix

logs:
	docker compose logs app

create_migration:
	docker compose exec app alembic revision -m ${message} --autogenerate

migrate:
	docker compose exec app alembic upgrade head

migrate_to:
	docker compose exec app alembic downgrade ${to}

test_all:
	docker compose exec app pytest -s --tb=native -vv app/tests

test_path:
	docker compose exec app pytest -s --tb=native -vv app/tests/${path}
