import setuptools
from pydatastructs import utils
from pydatastructs import linear_data_structures
from pydatastructs import miscellaneous_data_structures
from pydatastructs import trees

with open("README.md", "r") as fh:
    long_description = fh.read()

extensions = []

extensions.extend(utils._extensions.extensions)
extensions.extend(linear_data_structures._extensions.extensions)
extensions.extend(miscellaneous_data_structures._extensions.extensions)
extensions.extend(trees._extensions.extensions)

setuptools.setup(
    name="cz-pydatastructs",
    version="1.0.1-dev",
    author="PyDataStructs Development Team",
    author_email="pydatastructs@googlegroups.com",
    description="A python package for data structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codezonediitj/pydatastructs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries"
    ],
    python_requires='>=3.5',
    ext_modules=extensions
)
