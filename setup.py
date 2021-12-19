import setuptools
from pydatastructs.linear_data_structures import _extensions as linear_data_structures__extensions

with open("README.md", "r") as fh:
    long_description = fh.read()

extensions = []

extensions.extend(linear_data_structures__extensions.extensions)

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
