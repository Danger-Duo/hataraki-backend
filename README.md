# Hataraki Backend

RESTful API service for Hataraki.

## Pre-requisite Installation

- Python >= 3.9
- GNU Make (for test)
- Docker (for production)
- Docker Compose (for dev + tests)

## Recommended tools

- VSCode

## First time setup

1. Duplicate file `.env.example` and rename it to `.env`
2. Fill in the new file with appropriate values

> NB: The `.env` file is required for the application to run. Missing values in the file may cause the application to crash.

## Running the app

```bash
### run in development mode
# with Docker
docker compose up
# without Docker
make run

### run in production mode (ensure docker is running)
./bootstrap.sh
```

## Running tests

Docker Compose is required to run tests. A test database is created and destroyed during the test run.

```bash
# run tests
make test-app
```

## API Documentation

- [Swagger UI](https://hataraki-dev.hellodon.dev/docs)
