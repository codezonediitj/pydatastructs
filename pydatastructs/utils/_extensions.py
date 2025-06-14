from setuptools import Extension

project = 'pydatastructs'

module = 'utils'

backend = '_backend'

cpp = 'cpp'

nodes = '.'.join([project, module, backend, cpp, '_nodes'])
nodes_sources = ['/'.join([project, module, backend, cpp,
                            'nodes.cpp'])]
graph_utils = '.'.join([project, module, backend, cpp, '_graph_utils'])
graph_utils_sources = ['/'.join([project, module, backend, cpp,
                            'graph_utils.cpp'])]

extensions = [
    Extension(nodes, sources=nodes_sources, language="c++", extra_compile_args=["-std=c++17", "-stdlib=libc++"]),
    Extension(graph_utils, sources = graph_utils_sources, language="c++", extra_compile_args=["-std=c++17", "-stdlib=libc++"])
]
