alembic upgrade 'name' апгрейд до миграции
alembic revision --autogenerate -m "DataBase creation" - создание миграции
uvicorn main:app --reload запуск сайта