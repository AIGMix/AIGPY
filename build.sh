rm -rf dist
rm -rf build 
rm -rf *.egg-info
rm -rf __pycache__

python setup.py sdist bdist_wheel

pip uninstall -y aigpy

# python setup.py install


twine upload dist/*


