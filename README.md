PyDataStructs
=============

[![Build Status](https://github.com/codezonediitj/pydatastructs/actions/workflows/ci.yml/badge.svg)](https://github.com/codezonediitj/pydatastructs/actions) [![Discord](https://badgen.net/badge/icon/discord?icon=discord&label)](https://discord.gg/PwY7wQDG5G) [![Join the chat at https://gitter.im/codezonediitj/pydatastructs](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/codezoned2017/Lobby) [![Discuss at pydatastructs@googlegroups.com](https://img.shields.io/badge/discuss-pydatastructs%40googlegroups.com-blue.svg)](https://groups.google.com/forum/#!forum/pydatastructs) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/codezonediitj/pydatastructs/pulls) [![codecov](https://codecov.io/gh/codezonediitj/pydatastructs/branch/master/graph/badge.svg)](https://codecov.io/gh/codezonediitj/pydatastructs)

About
-----

- **PyDataStructs** project aims to be a Python package for various data structures and algorithms (including their parallel implementations).

- We are also working on providing C++ backend via Python C-API for high performance use cases.

Why PyDataStructs?
-------------------

- **Single package for all your data structures and algorithms**

- **Consistent and Clean Interface** - The APIs we have provided are consistent with each other, clean, and easy to use. We make sure of that before adding any new data structure or algorithm.

- **Well Tested** - We thoroughly test our code before making any new addition to PyDataStructs. 99 percent lines of our code have already been tested by us.

Installation
------------

If you are using Anaconda/Mamba, you can setup your development environment by executing the following commands,

```bash
conda env create --file environment.yml
conda activate pyds-env
```

You can install the library by running the following command,

```python
python scripts/build/install.py
```

For development purposes i.e., if you intend to be a contributor,

```python
python scripts/build/develop.py
```

Make sure you change your working directory to `pydatastructs` before executing any of the above commands. Also, your python version should be at least `3.8`.

Testing
-------

For testing your patch locally follow the steps given below,

1. Install [pytest-cov](https://pypi.org/project/pytest-cov/). Skip this step if you are already having the package.
2. Run, `python3 -m pytest --doctest-modules --cov=./ --cov-report=html`. Look for, `htmlcov/index.html` and open it in your browser, which will show the coverage report. Try to ensure that the coverage is not decreasing by more than 1% for your patch.

For a good visualisation of the different data structures and algorithms, refer the following websites:

- <https://visualgo.net/>
- <https://www.cs.usfca.edu/~galles/visualization/>

You can use the examples given in the following book as tests for your code:

- [https://opendatastructures.org/ods-python.pdf](https://opendatastructures.org/ods-python.pdf)

### Light weighted testing (without benchmarks)

Make sure you have activated the conda environment: `pyds-env` and your working directory is `../pydatastructs`.

In the terminal, run: `python -c "from pydatastructs.utils.testing_util import test; test()"`.

This will run all the test files, except benchmark tests. This should be used if benchmark tests are computationally too heavy to be run on your local machine.

Why do we use Python?
------------------

- As we know Python is an interpreted language and hence executing programs in it is slower as compared to C++.

- We still decided to use Python because the software development can happen at a much faster pace and it is much easier to test various software designs and APIs as coding them out takes no time in Python.

- However, keeping the need of the users in mind, we are also working on providing a C++ backend,  which will happen quickly as we would be required to just translate the tested code rather than writing it from scratch.

How to contribute?
------------------

Follow the steps given below,

1. Fork, <https://github.com/codezonediitj/pydatastructs/>
2. Execute, `git clone https://github.com/codezonediitj/pydatastructs/`
3. Change your working directory to `../pydatastructs`.
4. Execute, `git remote add origin_user https://github.com/<your-github-username>/pydatastructs/`
5. Execute, `git checkout -b <your-new-branch-for-working>`.
6. Make changes to the code.
7. Add your name and email to the AUTHORS, if you wish to.
8. Execute, `git add .`.
9. Execute, `git commit -m "your-commit-message"`.
10. Execute, `git push origin_user <your-current-branch>`.
11. Make PR.

That's it, 10 easy steps for your first contribution. For future contributions just follow steps 5 to 10. Make sure that before starting work, always checkout to master and pull the recent changes using the remote `origin` and then start following steps 5 to 10.

See you soon with your first PR.

It is recommended to go through the following links before you start working.

- [Issue Policy](https://github.com/codezonediitj/pydatastructs/wiki/Issue-Policy)
- [Pull Request Policy](https://github.com/codezonediitj/pydatastructs/wiki/Pull-Request-Policy)
- [Plan of Action for the Projects](https://github.com/codezonediitj/pydatastructs/wiki/Plan-of-Action-for-the-Projects)

Guidelines
----------

We recommend you to join our [discord channel](https://discord.gg/PwY7wQDG5G) for discussing anything related to the project.

Please follow the rules and guidelines given below,

1. Follow the [numpydoc docstring guide](https://numpydoc.readthedocs.io/en/latest/format.html).
2. If you are planning to contribute a new data structure then first raise an **issue** for discussing the API, rather than directly making a PR. Please go through [Plan of Action for Adding New Data Structures](https://github.com/codezonediitj/pydatastructs/wiki/Plan-of-Action-for-Adding-New-Data-Structures).
3. For the first-time contributors we recommend not to take a complex data structure, rather start with `beginner` or `easy`.
4. We don't assign issues to any individual. Instead, we follow First Come First Serve for taking over issues, i.e., if one contributor has already shown interest then no comment should be made after that as it won't be considered. Anyone willing to work on an issue can comment on the thread that he/she is working on and raise a PR for the same.
5. Any open PR must be provided with some updates after being reviewed. If it is stalled for more than 4 days, it will be labeled as `Please take over`, meaning that anyone willing to continue that PR can start working on it.
6. PRs that are not related to the project or don't follow any guidelines will be labeled as `Could Close`, meaning that the PR is not necessary at the moment.

The following parameters are to be followed to pass the code quality tests for your Pull Requests,

1. There should not be any trailing white spaces at any line of code.
2. Each `.py` file should end with exactly one new line.
3. Comparisons involving `True`, `False`, and `None` should be done by
reference (using `is`, `is not`) and not by value(`==`, `!=`).

Keep contributing!!

Thanks to these wonderful people ✨✨:

![https://github.com/codezonediitj/pydatastructs/graphs/contributors](https://contrib.rocks/image?repo=codezonediitj/pydatastructs)
