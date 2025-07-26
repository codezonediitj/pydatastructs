python = import('python').find_installation(pure: false)

# Install pure python sources
install_subdir(
    '.',
    install_dir: python.get_install_dir(subdir: 'pydatastructs'),
)

# utils extension modules
python.extension_module(
    'pydatastructs.utils._backend.cpp._nodes',
    'utils/_backend/cpp/nodes.cpp',
    install: true,
    subdir: 'pydatastructs/utils'
)
python.extension_module(
    'pydatastructs.utils._backend.cpp._graph_utils',
    'utils/_backend/cpp/graph_utils.cpp',
    install: true,
    subdir: 'pydatastructs/utils'
)

# linear_data_structures extension modules
python.extension_module(
    'pydatastructs.linear_data_structures._backend.cpp._arrays',
    'linear_data_structures/_backend/cpp/arrays/arrays.cpp',
    install: true,
    subdir: 'pydatastructs/linear_data_structures'
)
python.extension_module(
    'pydatastructs.linear_data_structures._backend.cpp._algorithms',
    'linear_data_structures/_backend/cpp/algorithms/algorithms.cpp',
    install: true,
    subdir: 'pydatastructs/linear_data_structures'
)

# miscellaneous_data_structures extension module
python.extension_module(
    'pydatastructs.miscellaneous_data_structures._backend.cpp._stack',
    'miscellaneous_data_structures/_backend/cpp/stack/stack.cpp',
    install: true,
    subdir: 'pydatastructs/miscellaneous_data_structures'
)

# trees extension module
python.extension_module(
    'pydatastructs.trees._backend.cpp._trees',
    'trees/_backend/cpp/trees.cpp',
    install: true,
    subdir: 'pydatastructs/trees'
)

# graphs extension modules
py_include = include_directories('utils/_backend/cpp')
python.extension_module(
    'pydatastructs.graphs._backend.cpp._graph',
    'graphs/_backend/cpp/graph.cpp',
    include_directories: py_include,
    install: true,
    subdir: 'pydatastructs/graphs'
)
python.extension_module(
    'pydatastructs.graphs._backend.cpp._algorithms',
    'graphs/_backend/cpp/algorithms.cpp',
    include_directories: py_include,
    install: true,
    subdir: 'pydatastructs/graphs'
)
