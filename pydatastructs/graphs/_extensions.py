from setuptools import Extension
import os

project = 'pydatastructs'

module = 'graphs'

backend = '_backend'

cpp = 'cpp'

graph = '.'.join([project, module, backend, cpp, '_graph'])
graph_sources = ['/'.join([project, module, backend, cpp,
                            'graph.cpp']),"pydatastructs/utils/_backend/cpp/graph_utils.cpp"]
algorithms = '.'.join([project, module, backend, cpp, '_algorithms'])
algorithms_sources = ['/'.join([project, module, backend, cpp,
                            'algorithms.cpp']),"pydatastructs/utils/_backend/cpp/graph_utils.cpp"]

include_dir = os.path.abspath(os.path.join(project, 'utils', '_backend', 'cpp'))

extensions = [Extension(graph, sources=graph_sources,include_dirs=[include_dir], language="c++", extra_compile_args=["-std=c++17"]),
              Extension(algorithms, sources=algorithms_sources,include_dirs=[include_dir], language="c++", extra_compile_args=["-std=c++17"]),
              ]
