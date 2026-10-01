#!/bin/sh
# VideoSpeed test runner. Core cases do not need ffmpeg or OpenCV.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m unittest discover -s tests -v
