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

python.extension_module(
    'pydatastructs.trees._backend.cpp._trees',
    '_backend/cpp/trees.cpp',
    install: true,
    subdir: 'pydatastructs/trees'
)

subdir('tests')
