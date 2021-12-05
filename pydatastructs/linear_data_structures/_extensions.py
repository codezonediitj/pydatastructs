from setuptools import Extension

project = 'pydatastructs'

module = 'linear_data_structures'

backend = '_backend'

cpp = 'cpp'

arrays = '.'.join([project, module, backend, cpp, 'arrays'])
arrays_sources = ['/'.join([project, module, backend, cpp,
                            'arrays', 'arrays.cpp'])]
extension = Extension(arrays, sources=arrays_sources)
