from setuptools import Extension

project = 'pydatastructs'

module = 'trees'

backend = '_backend'

cpp = 'cpp'

trees = '.'.join([project, module, backend, cpp, '_trees'])
trees_sources = ['/'.join([project, module, backend, cpp,
                            'trees.cpp'])]

extensions = [
    Extension(trees, sources=trees_sources)
]
