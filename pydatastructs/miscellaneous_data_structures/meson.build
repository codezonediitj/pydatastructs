python = import('python').find_installation(pure: false)

python.install_sources(
    [
        '__init__.py',
        '_extensions.py',
        'algorithms.py',
        'multiset.py',
        'sparse_table.py',
        'disjoint_set.py',
        'queue.py',
        'binomial_trees.py',
        'segment_tree.py',
        'stack.py'
    ],
    subdir: 'pydatastructs/miscellaneous_data_structures'
)

python.install_sources(
    ['_backend/__init__.py', '_backend/cpp/__init__.py'],
    subdir: 'pydatastructs/miscellaneous_data_structures/_backend'
)

python.extension_module(
    '_stack',
    '_backend/cpp/stack/stack.cpp',
    install: true,
    subdir: 'pydatastructs/miscellaneous_data_structures/_backend/cpp'
)

subdir('tests')
