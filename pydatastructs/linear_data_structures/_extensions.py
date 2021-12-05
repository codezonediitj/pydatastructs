from setuptools import Extension

project = 'pydatastructs'

module = 'linear_data_structures'

backend = '_backend'

cpp = 'cpp'

submodule = 'arrays'

arrays = '.'.join([project, module, backend, cpp, submodule, 'arrays'])
arrays_sources = ['/'.join([project, module, backend, cpp,
                            submodule, 'arrays.cpp'])]
extension = Extension(arrays, sources=arrays_sources)
