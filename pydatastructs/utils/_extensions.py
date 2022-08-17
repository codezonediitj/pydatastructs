from setuptools import Extension

project = 'pydatastructs'

module = 'utils'

backend = '_backend'

cpp = 'cpp'

utils = '.'.join([project, module, backend, cpp, '_utils'])
utils_sources = ['/'.join([project, module, backend, cpp, 'utils.cpp'])]

extensions = [
    Extension(utils, sources=utils_sources),
]
