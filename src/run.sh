#!/bin/bash

[[ -z "$HOST" ]] && HOST="0.0.0.0"
[[ -z "$PORT" ]] && PORT=5000

gunicorn --bind ${HOST}:${PORT} wsgi:application
