cd  %~dp0

REM remove old dir
rmdir /s/q dist
rmdir /s/q build
rmdir /s/q aigpy.egg-info

REM build
python setup.py sdist bdist_wheel

REM reinstall aigpy
pip uninstall -y aigpy

REM install 
python setup.py install


REM upload to pip
twine upload dist/*
