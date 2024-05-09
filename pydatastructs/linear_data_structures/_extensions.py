from setuptools import Extension

project = 'pydatastructs'

module = 'linear_data_structures'

backend = '_backend'

cpp = 'cpp'

arrays = '.'.join([project, module, backend, cpp, '_arrays'])
arrays_sources = ['/'.join([project, module, backend, cpp,
                            'arrays', 'arrays.cpp'])]

trees = '.'.join([project, 'trees', backend, cpp, 'BST'])
trees_sources = ['/'.join([project, 'trees', backend, cpp,
                            'BST_module.cpp'])]

algorithms = '.'.join([project, module, backend, cpp, '_algorithms'])
algorithms_sources = ['/'.join([project, module, backend, cpp,
                                'algorithms', 'algorithms.cpp'])]

extensions = [
    Extension(arrays, sources=arrays_sources),
    Extension(algorithms, sources=algorithms_sources),
    Extension(trees, sources=trees_sources)
]
