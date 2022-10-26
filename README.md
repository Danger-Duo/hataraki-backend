# Hataraki Backend

RESTful API service for Hataraki.

## Pre-requisite Installation

- Python >= 3.9
- GNU Make (for development)
- Docker (for production deployment)
- Docker Compose (for running tests)

## Recommended tools

- VSCode

## First time setup

1. Duplicate file `.env.example` and rename it to `.env`
2. Fill in the new file with appropriate values

> NB: The `.env` file is required for the application to run. Missing values in the file will cause the application to crash.

## Running the app

```bash
# run in development mode
make run

# run in production mode (ensure docker is running)
./bootstrap.sh
```

## Running tests

Docker Compose is required to run tests. A test database is created and destroyed during the test run.

```bash
# run tests
make test
```

## API Documentation

- [Swagger UI](https://hataraki-dev.hellodon.dev/docs)
