# base img
FROM python:3.9-slim AS base

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8001"]

# test img
FROM base AS test

WORKDIR /code

COPY tests/requirements.txt /code/tests/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/tests/requirements.txt

COPY ./tests /code/tests
