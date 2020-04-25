PyDataStructs
=============

[![Build Status](https://travis-ci.org/codezonediitj/pydatastructs.png?branch=master)](https://travis-ci.org/codezonediitj/pydatastructs) [![Join the chat at https://gitter.im/codezonediitj/pydatastructs](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/codezoned2017/Lobby) [![Discuss at pydatastructs@googlegroups.com](https://img.shields.io/badge/discuss-pydatastructs%40googlegroups.com-blue.svg)](https://groups.google.com/forum/#!forum/pydatastructs) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/codezonediitj/pydatastructs/pulls) [![codecov](https://codecov.io/gh/codezonediitj/pydatastructs/branch/master/graph/badge.svg)](https://codecov.io/gh/codezonediitj/pydatastructs)

About
-----

Currently, the project aims to be a Python package for various data structures in computer science. Besides, we are also working on including parallel algorithms. To the best of our knowledge, a well-designed library/package which has covered most of the data structures and algorithms including their parallel implementation doesn't exist. 

In future, i.e, after a few releases of the package when the software design will become stable, we also aim to provide APIs for the code in C++ and Java as well.

Installation
------------

You can install the library by running the following command,

```python
python3 setup.py install
```

For development purposes, you can use the option `develop` as shown below,

```python
python3 setup.py develop
```

Make sure that your python version is above `3.5`.

Testing
-------

For testing your patch locally follow the steps given below,

1. Install [pytest-cov](https://pypi.org/project/pytest-cov/). Skip this step if you are already having the package.
2. Run, `python3 -m pytest --doctest-modules --cov=./ --cov-report=html`. Look for, `htmlcov/index.html` and open it in your browser, which will show the coverage report. Try to ensure that the coverage is not decreasing by more than 1% for your patch.

For a good visualisation of the different data structures and algorithms, refer the following websites:
- https://visualgo.net/
- https://www.cs.usfca.edu/~galles/visualization/

You can use the examples given in the following book as tests for your code:
- [https://opendatastructures.org/ods-python.pdf](https://opendatastructures.org/ods-python.pdf)

Why we use Python?
------------------

As we know Python is an interpreted language and hence is slow as compared to C++, the most
popular language for sports programming. We still decided to use Python because the software
development can happen at a much faster pace and it is much easier to test various software designs and APIs as coding them out takes no time. However, keeping the need of the users in mind, we will shift to C++ backend,  which will happen quickly as we would be required to just translate the tested code rather than writing it from scratch, after a few releases with APIs available for all the languages.

How to contribute?
------------------

Follow the steps given below,

1. Fork, https://github.com/codezonediitj/pydatastructs/
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

We recommend you to join our [gitter channel](https://gitter.im/codezoned2017/Lobby) for dicussing anything related to the project.

Please follow the rules and guidelines given below,

1. Follow the [numpydoc docstring guide](https://numpydoc.readthedocs.io/en/latest/format.html).
2. If you are planning to contribute a new data structure then first raise an issue for discussing the API, rather than directly making a PR.
3. For the first-time contributors we recommend not to take a complex data structure, rather start with `beginner` or `easy`.

The following parameters are to be followed to pass the code quality tests for your Pull Requests,

1. There should not be any trailing white spaces at any line of code.
2. Each `.py` file should end with exactly one new line.
3. Comparisons involving `True`, `False` and `None` should be done by
reference (using `is`, `is not`) and not by value(`==`, `!=`).

Keep contributing!!
