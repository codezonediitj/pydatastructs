from setuptools import Extension

project = 'pydatastructs'

module = 'linear_data_structures'

backend = '_backend'

cpp = 'cpp'

arrays = '.'.join([project, module, backend, cpp, '_arrays'])
arrays_sources = ['/'.join([project, module, backend, cpp,
                            'arrays', 'arrays.cpp'])]

algorithms = '.'.join([project, module, backend, cpp, '_algorithms'])
algorithms_sources = ['/'.join([project, module, backend, cpp,
                                'algorithms', 'algorithms.cpp'])]

extensions = [
    Extension(arrays, sources=arrays_sources, language="c++", extra_compile_args=["-std=c++17"]),
    Extension(algorithms, sources=algorithms_sources, language="c++", extra_compile_args=["-std=c++17"])
]
