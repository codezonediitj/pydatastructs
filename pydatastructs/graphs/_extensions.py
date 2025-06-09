from setuptools import Extension
import os

project = 'pydatastructs'

module = 'graphs'

backend = '_backend'

cpp = 'cpp'

graph = '.'.join([project, module, backend, cpp, '_graph'])
graph_sources = ['/'.join([project, module, backend, cpp,
                            'graph.cpp']),"pydatastructs/utils/_backend/cpp/graph_utils.cpp"]

include_dir = os.path.abspath(os.path.join(project, 'utils', '_backend', 'cpp'))

extensions = [Extension(graph, sources=graph_sources,include_dirs=[include_dir])]
