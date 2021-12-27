from setuptools import Extension

project = 'pydatastructs'

module = 'linear_data_structures'

backend = '_backend'

cpp = 'cpp'

submodule = 'arrays'

dummy_submodule = '_arrays.py'

arrays = '.'.join([project, module, backend, cpp, '_arrays'])
arrays_sources = ['/'.join([project, module, backend, cpp,
                            submodule, 'arrays.cpp'])]

extensions = [
    Extension(arrays, sources=arrays_sources)
]
