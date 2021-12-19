from setuptools import Extension
import os

project = 'pydatastructs'

module = 'linear_data_structures'

backend = '_backend'

cpp = 'cpp'

submodule = 'arrays'

arrays = '.'.join([project, module, backend, cpp, '_arrays'])
arrays_sources = ['/'.join([project, module, backend, cpp,
                            submodule, 'arrays.cpp'])]

extensions = [
    Extension(arrays, sources=arrays_sources)
]

dummy_submodules = ['_arrays.py']

def delete_dummy_submodules():
    for dummy_submodule in dummy_submodules:
        os.remove('/'.join([project, module, backend, cpp, dummy_submodule]))

def add_dummy_submodules():
    for dummy_submodule in dummy_submodules:
        dummy_file = open('/'.join([project, module, backend, cpp, dummy_submodule]), 'w+')
        dummy_file.close()