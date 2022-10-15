# Hataraki Backend

RESTful API service for Hataraki in Java Spring 5.

## Pre-requisite Installation

- Python >= 3.9
- GNU Make

## Recommended tools

- VSCode

## First time setup

1. Duplicate file `.env.example` and rename it to `.env`
2. Fill in the new file with appropriate values

## Running the app

```bash
# run in development mode
make run

# run in production mode
make install
source venv/bin/activate
uvicorn app:app --port 8001
```

## API Documentation

- [Swagger UI](http://localhost:8001/docs)
