from setuptools import setup, find_packages
setup(
    name = 'aigpy',
    version='2019.5.9.2',
    license = "MIT Licence",
    description = "Python Common Tool",

    author = 'YaronH',
    author_email = "yaronhuang@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires=["requests", "configparser", "futures", "reportlab", "Pillow"],
    # entry_points={'console_scripts': [
    #     'tidal-dl = tidal_dl:main', ]}
)
