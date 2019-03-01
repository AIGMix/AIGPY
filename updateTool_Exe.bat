cd  %~dp0

REM remove old dir
rmdir /s/q dist
rmdir /s/q build
rmdir /s/q aigpy.egg-info
REM rmdir /s/q exe
rm exe/aigpy.exe
mkdir exe

REM build
python setup_Exe.py sdist bdist_wheel

REM reinstall aigpy
pip uninstall -y aigpy

REM creat exe file
pyinstaller -F aigpy/__main__.py

REM rename exe name
cd dist
ren __main__.exe aigpy.exe
move aigpy.exe ../exe/
cd ..

