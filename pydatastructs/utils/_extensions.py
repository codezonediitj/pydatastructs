from setuptools import Extension

project = 'pydatastructs'

module = 'utils'

backend = '_backend'

cpp = 'cpp'

nodes = '.'.join([project, module, backend, cpp, '_nodes'])
nodes_sources = ['/'.join([project, module, backend, cpp,
                            'nodes.cpp'])]

extensions = [
    Extension(nodes, sources=nodes_sources)
]
