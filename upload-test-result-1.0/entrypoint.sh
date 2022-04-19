#!/bin/sh

set -eu

pip install -r /source/requirements.txt
python /source/app/script.py

