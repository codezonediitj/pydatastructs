from setuptools import Extension

project = 'pydatastructs'

module = 'trees'

backend = '_backend'

cpp = 'cpp'

trees = '.'.join([project, module, backend, cpp, '_trees'])
trees_sources = ['/'.join([project, module, backend, cpp,
                            'trees', 'trees.cpp'])]

# Add tree algorithms later

# algorithms = '.'.join([project, module, backend, cpp, '_algorithms'])
# algorithms_sources = ['/'.join([project, module, backend, cpp,
#                                 'algorithms', 'algorithms.cpp'])]

extensions = [
    Extension(trees, sources=trees_sources),
    # Extension(algorithms, sources=algorithms_sources)
]
