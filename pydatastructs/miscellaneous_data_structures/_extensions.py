from setuptools import Extension

project = 'pydatastructs'

module = 'miscellaneous_data_structures'

backend = '_backend'

cpp = 'cpp'

stack = '.'.join([project, module, backend, cpp, '_stack'])
stack_sources = ['/'.join([project, module, backend, cpp, 'stack', 'stack.cpp'])]

extensions = [
    Extension(stack, sources=stack_sources),
]
