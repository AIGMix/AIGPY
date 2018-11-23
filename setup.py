from setuptools import setup, find_packages

setup(
    name = 'aigpy',
    version='1.0.0.12',
    license = "MIT Licence",
    description = "Python Common Tool",

    author = 'YaronH',
    author_email = "yaronhuang@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires=["requests", "configparser"],

    # entry_points={'console_scripts': [
    #     'tidal-dl = tidal_dl:main', ]}
)
