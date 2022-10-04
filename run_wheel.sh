#!/bin/sh
rm -rf .pytest_cache/
rm -rf dist/
rm -rf build/
python setup.py bdist_wheel
