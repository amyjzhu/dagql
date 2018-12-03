#!/usr/bin/env bash

cd "$(dirname "$0")"
PYTHONPATH="$(pwd):$PYTHONPATH" pylint dagql test
