#!/bin/bash

ruff check --fix --no-cache .

pytest -n auto
