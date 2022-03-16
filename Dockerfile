FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

ENTRYPOINT poetry run python -m pytest tests/ -m "not slow" --junit-xml=/out/report.xml

COPY . /app/
