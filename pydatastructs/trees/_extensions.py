from setuptools import Extension

project = 'pydatastructs'

module = 'trees'

backend = '_backend'

cpp = 'cpp'

trees = '.'.join([project, module, backend, cpp, 'BST'])
trees_sources = ['/'.join([project, module, backend, cpp,
                            'BST_module.cpp'])]

extensions = [
    Extension(trees, sources=trees_sources)
]
