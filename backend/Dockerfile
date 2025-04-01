FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1


WORKDIR /app

RUN apt-get update && apt-get install

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

WORKDIR /app/e_commerce

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]