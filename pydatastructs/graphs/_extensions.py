from setuptools import Extension
import sysconfig

project = 'pydatastructs'

module = 'graphs'

backend = "_backend"

cpp = 'cpp'

bfs = '.'.join([project, module, backend, cpp, '_bfs'])
bfs_sources = ['/'.join([project, module, backend, cpp, 'algorithms.cpp'])]

extensions = [
    Extension(bfs, sources=bfs_sources)
]