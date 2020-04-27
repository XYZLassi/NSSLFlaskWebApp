#!/usr/bin/env bash


export PYTHONPATH=".:src/"
pytest --cov-report html --cov-report term --cov=src
