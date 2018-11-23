cd  %~dp0
rmdir /s/q dist
rmdir /s/q build
rmdir /s/q aigpy.egg-info
python setup.py sdist bdist_wheel
twine upload dist/*

pip install --upgrade aigpy