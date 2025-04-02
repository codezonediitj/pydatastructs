from setuptools import setup, Extension
import sysconfig

bfs_dfs_module = Extension(
    '_bfs_dfs',  # Module name
    sources=['src/cpp/bfs_dfs.cpp'],
    include_dirs=[sysconfig.get_path('include')],
    extra_compile_args=['-std=c++11'],
)

setup(
    name='my_pydatastructs',
    version='0.1',
    package_dir={'': 'src/python'},
    py_modules=['graph_algorithms'],
    ext_modules=[bfs_dfs_module],
)