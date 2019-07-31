from setuptools import setup, find_packages
import sys

if sys.version_info >= (3, 0):
    install_requires = ["requests", "configparser", "colorama",
                        "reportlab", "Pillow", "mutagen"]
else:
    install_requires = ["requests", "configparser", "colorama",
                        "futures", "reportlab", "Pillow", "mutagen"]

setup(
    name = 'aigpy',
    version='2019.7.31.0',
    license = "MIT Licence",
    description = "Python Common Tool",

    author = 'YaronH',
    author_email = "yaronhuang@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires=install_requires,
    # entry_points={'console_scripts': [
    #     'tidal-dl = tidal_dl:main', ]}
)
