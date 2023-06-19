from setuptools import Extension

project = 'pydatastructs'

module = 'graphs'

backend = '_backend'

cpp = 'cpp'

graph = '.'.join([project, module, backend, cpp, '_graph'])
graph_sources = ['/'.join([project, module, backend, cpp, 'graph', 'graph.cpp'])]

extensions = [
    Extension(graph, sources=graph_sources),
]
