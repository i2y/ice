"""Import a Python object made by compiling a Ice file.
"""

import os

from ice.core import init, pyc_compile


def get_function(name, file_path):
    """Python function from Ice.

    Compiles a Ice file to Python bytecode and returns the
    imported function.
    """
    return getattr(get_module(name, file_path), name)


def get_module(full_name, file_path):
    """Python function from Ice.

    Compiles a Ice file to Python bytecode and returns the
    Python module.
    """
    print(full_name)
    name = full_name.split('.')[-1]
    base_path = os.path.dirname(file_path)
    ice_name = os.path.join(base_path, name + '.ice')
    py_name = os.path.join(base_path, name + '.pyc')
    pyc_compile(ice_name, py_name)
    return __import__(full_name)

init()
