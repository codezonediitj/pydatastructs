python = import('python').find_installation(pure: false)

python.install_sources(
    [
        '__init__.py',
        'adjacency_list.py',
        'adjacency_matrix.py',
        'algorithms.py',
        'graph.py'
    ],
    subdir: 'pydatastructs/graphs'
)

python.install_sources(
    ['_backend/__init__.py', '_backend/cpp/__init__.py'],
    subdir: 'pydatastructs/graphs/_backend'
)

py_include = include_directories('../utils/_backend/cpp')

python.extension_module(
    '_nodes',
    '_backend/cpp/nodes.cpp',
    install: true,
    subdir: 'pydatastructs/utils/_backend/cpp'
)

python.extension_module(
    '_graph_utils',
    '_backend/cpp/graph_utils.cpp',
    install: true,
    subdir: 'pydatastructs/utils/_backend/cpp'
)

subdir('tests')
