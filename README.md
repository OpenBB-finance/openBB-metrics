# OpenBB Open Source Metrics

To run using Docker (recommended):

`docker build .`

`docker image ls`

`docker run -p 8000:8000 {IMAGE ID}`

To run using Docker-compose: 

`docker-compose build`

`docker-compose run web alembic revision --autogenerate`

`docker-compose run web alembic upgrade head`

`docker-compose up`

To run without Docker: 

`pip install poetry`

`poetry install`

`uvicorn main:app --reload`

For reference:

- https://ahmed-nafies.medium.com/fastapi-with-sqlalchemy-postgresql-and-alembic-and-of-course-docker-f2b7411ee396