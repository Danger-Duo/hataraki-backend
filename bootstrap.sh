#!/bin/bash

make install
venv/bin/uvicorn app.server:app --port 8001
