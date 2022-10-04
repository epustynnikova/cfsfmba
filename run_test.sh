#!/bin/sh
rm -rf .pytest_cache/
rm -rf dist/
rm -rf build/
BASEDIR=$(dirname "$0")
echo "$BASEDIR"
pip install -r "$BASEDIR/requirements.txt"
python -m pytest -v "$BASEDIR/test"
