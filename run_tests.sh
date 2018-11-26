#!/usr/bin/env bash

cd "$(dirname "$0")"
PYTHONPATH="$(pwd):$PYTHONPATH" pytest -v
