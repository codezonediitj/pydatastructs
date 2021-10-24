import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydatastructs",
    version="0.0.1-dev",
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
        "Topic :: Education :: Data Structures",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries"
    ],
    python_requires='>=3.5',
)
