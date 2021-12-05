from setuptools import Extension, setup

arrays_extension = Extension('pydatastructs.linear_data_structures.backend.cpp.arrays.arrays', sources=['pydatastructs/linear_data_structures/backend/cpp/arrays/arrays.cpp'])

setup(name='arrays', ext_modules=[arrays_extension], py_modules=["arrays"])
