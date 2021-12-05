import setuptools
from pydatastructs import linear_data_structures

with open("README.md", "r") as fh:
    long_description = fh.read()

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
    ext_modules=[
        linear_data_structures._extensions.extension
    ]
)
