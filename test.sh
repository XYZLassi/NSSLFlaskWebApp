#!/usr/bin/env bash

PYTHONPATH=".:src/"
export PYTHONPATH
pytest --cov-report html --cov-report term --cov=src
