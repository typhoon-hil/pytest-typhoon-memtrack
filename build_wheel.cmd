pushd %~dp0
python setup.py build_ext bdist_wheel clean --all
popd