from setuptools import Extension

project = 'pydatastructs'

module = 'strings'

backend = '_backend'

cpp = 'cpp'

# Define the extension for string algorithms
algorithms = '.'.join([project, module, backend, cpp, '_algorithms'])
algorithms_sources = [
    '/'.join([project, module, backend, cpp, 'algorithms', 'algorithms.cpp']),
    '/'.join([project, "utils", "_backend", "cpp", "string.cpp"])
]

# Define the extension for the Trie data structure
trie = '.'.join([project, module, backend, cpp, '_trie'])
trie_sources = [
    '/'.join([project, module, backend, cpp, 'trie', 'trie.cpp']),
    '/'.join([project, "utils", "_backend", "cpp", "string.cpp"])
]

# Define the extension for the main strings module
strings = '.'.join([project, module, backend, cpp, '_strings'])
strings_sources = [
    '/'.join([project, module, backend, cpp, 'strings.cpp'])
]

extensions = [
    Extension(algorithms, sources=algorithms_sources),
    Extension(trie, sources=trie_sources),
    Extension(strings, sources=strings_sources)
]