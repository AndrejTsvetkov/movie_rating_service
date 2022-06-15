FROM python:3.9


RUN mkdir /code
WORKDIR /code

# requirements (poetry)
COPY ./poetry.lock ./poetry.toml ./pyproject.toml  /code/

RUN pip install poetry
RUN POETRY_VIRTUALENVS_CREATE=false poetry install
#RUN poetry shell
#RUN poetry install --no-dev


COPY ./app /code/app
COPY ./init_db.py /code
RUN python init_db.py

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
