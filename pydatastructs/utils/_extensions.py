from setuptools import Extension
import os
import sys
import os
import sys

project = 'pydatastructs'
module = 'utils'
backend = '_backend'
cpp = 'cpp'

nodes = '.'.join([project, module, backend, cpp, '_nodes'])
nodes_sources = [os.path.join(project, module, backend, cpp, 'nodes.cpp')]

nodes_sources = [os.path.join(project, module, backend, cpp, 'nodes.cpp')]

graph_utils = '.'.join([project, module, backend, cpp, '_graph_utils'])
graph_utils_sources = [os.path.join(project, module, backend, cpp, 'graph_utils.cpp')]

extra_compile_args = ["-std=c++17"]

if sys.platform == "darwin":
    extra_compile_args.append("-mmacosx-version-min=10.13")
elif sys.platform == "win32":
    extra_compile_args = ["/std:c++17"]
graph_utils_sources = [os.path.join(project, module, backend, cpp, 'graph_utils.cpp')]

extra_compile_args = ["-std=c++17"]

if sys.platform == "darwin":
    extra_compile_args.append("-mmacosx-version-min=10.13")
elif sys.platform == "win32":
    extra_compile_args = ["/std:c++17"]

extensions = [
    Extension(
        nodes,
        sources=nodes_sources,
        extra_compile_args=extra_compile_args,
    ),
    Extension(
        graph_utils,
        sources=graph_utils_sources,
        extra_compile_args=extra_compile_args,
    ),
]
