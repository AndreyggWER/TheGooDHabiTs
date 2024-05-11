alembic upgrade 'name' апгрейд до миграции
alembic revision --autogenerate -m "name" - создание миграции
uvicorn main:app --reload запуск сайта