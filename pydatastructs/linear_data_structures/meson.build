python = import('python').find_installation(pure: false)

python.install_sources(
    [
        '__init__.py',
        'algorithms.py',
        'arrays.py',
        'linked_lists.py'
    ],
    subdir: 'pydatastructs/linear_data_structures'
)

python.install_sources(
    ['_backend/__init__.py', '_backend/cpp/__init__.py'],
    subdir: 'pydatastructs/linear_data_structures/_backend'
)

python.install_sources(
    ['_backend/cpp/algorithms/llvm_algorithms.py'],
    subdir: 'pydatastructs/linear_data_structures/_backend/cpp/algorithms'
)

python.extension_module(
    '_arrays',
    '_backend/cpp/arrays/arrays.cpp',
    install: true,
    subdir: 'pydatastructs/linear_data_structures/_backend/cpp'
)

python.extension_module(
    '_algorithms',
    '_backend/cpp/algorithms/algorithms.cpp',
    install: true,
    subdir: 'pydatastructs/linear_data_structures/_backend/cpp',
    cpp_args: ['-std=c++17'],
    override_options: ['cpp_std=c++17'],
)

subdir('tests')
