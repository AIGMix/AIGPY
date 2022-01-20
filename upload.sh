rm -rf dist
rm -rf build 
rm -rf aigpy.egg-info

python setup.py sdist bdist_wheel

pip uninstall -y aigpy

# python setup.py install


twine upload dist/*





cmd
rd /s /q build
rd /s /q dist
rd /s /q aigpy.egg-info

python setup.py sdist bdist_wheel
twine upload dist/*