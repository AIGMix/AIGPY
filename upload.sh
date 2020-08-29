rm -rf dist
rm -rf build 
rm -rf aigpy.egg-info

python setup.py sdist bdist_wheel

pip uninstall -y aigpy

python setup.py install

twine upload dist/*
