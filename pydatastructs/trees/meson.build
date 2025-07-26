python = import('python').find_installation(pure: false)

python.install_sources(
    [
        '__init__.py',
        '_extensions.py',
        'binary_trees.py',
        'heaps.py',
        'm_ary_trees.py',
        'space_partitioning_trees.py'
    ],
    subdir: 'pydatastructs/trees'
)

python.install_sources(
    ['_backend/__init__.py', '_backend/cpp/__init__.py'],
    subdir: 'pydatastructs/trees/_backend'
)

python.extension_module(
    '_trees',
    '_backend/cpp/trees.cpp',
    install: true,
    subdir: 'pydatastructs/trees/_backend/cpp'
)

subdir('tests')
