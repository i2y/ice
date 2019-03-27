#!/usr/bin/env python
from setuptools import setup, find_packages
# from pip.download import PipSession
# from pip.req import parse_requirements


from ice import __author__, __version__, __license__, GE_PYTHON_34


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_requires = parse_requirements('requirements.txt')
# install_requires = [str(ir.req) for ir in install_reqs]

if not GE_PYTHON_34:
    install_requires.append('pathlib>=1.0.1')


def is_windows():
    from sys import platform
    return platform.startswith('win') or platform.startswith('cygwin')

if is_windows():
    readme = ''
else:
    with open('README.md', 'r') as f:
        readme = f.read()

setup(
    name='ice-lang',
    version=__version__,
    description='Dynamically typed functional programming language',
    long_description=readme,
    license=__license__,
    author=__author__,
    url='https://github.com/i2y/ice',
    platforms=['any'],
    entry_points={
        'console_scripts': [
            'ice = ice.core:main'
        ]
    },
    packages=find_packages(),
    package_data = {
        'ice': ['sexpressions/*',
                'core/import_global_env.ice'],
    },
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers"
    ]
)
