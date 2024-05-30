FROM python:3.11

WORKDIR /code

COPY ./poetry.lock /code/poetry.lock
COPY ./pyproject.toml /code/pyproject.toml

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY ./src /code/src

EXPOSE 8080

CMD ["python", "./src/main.py"]
#CMD ["fastapi", "run", "./src/main.py", "--port", "8080"]
