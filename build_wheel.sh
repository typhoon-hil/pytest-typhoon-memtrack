#! /bin/bash

pushd "$(dirname "$0")"
python setup.py build_ext bdist_wheel clean --all
popd