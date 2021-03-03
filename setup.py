from setuptools import setup, find_packages

setup(
    name = 'aigpy',
    version = '2021.3.1.0',
    license = "MIT Licence",
    description = "Python Common Tool",

    author = 'Yaronzz',
    author_email = "yaronhuang@foxmail.com",

    packages = find_packages(),
    platforms = "any",
    include_package_data = True,
    install_requires=["requests", "colorama", "mutagen"],
)
