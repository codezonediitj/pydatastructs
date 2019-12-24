PyDataStructs
=============

[![Build Status](https://travis-ci.org/codezonediitj/pydatastructs.png?branch=master)](https://travis-ci.org/codezonediitj/pydatastructs) [![Join the chat at https://gitter.im/codezonediitj/pydatastructs](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/codezoned2017/Lobby) [![Discuss at pydatastructs@googlegroups.com](https://img.shields.io/badge/discuss-pydatastructs%40googlegroups.com-blue.svg)](https://groups.google.com/forum/#!forum/pydatastructs) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/codezonediitj/pydatastructs/pulls) [![codecov](https://codecov.io/gh/codezonediitj/pydatastructs/branch/master/graph/badge.svg)](https://codecov.io/gh/codezonediitj/pydatastructs)

Who are we?
-----------

We are a group of people passionate about data structures and algorithms. We eye for implementing all the data structures given [here](https://en.wikipedia.org/wiki/List_of_data_structures).

How are we different?
---------------------

There are many pre-exisiting packages available in the open source world based on the above idea. However, they lack the implementation of complex data structures and this makes us different. If you have worked with C++ and Python then you know how hard it is to code bug free AVL trees :-).Well, after this project you will not have to worry about it. In fact, we will keep each data structure independent from each other for easy code reusability.

Why we use Python?
-----------------

As we know Python is an interepreted language and hence is slow as compared to C++, the most
popular language for sports programming. We still decided to use Python because the software
development can happen at a much faster pace and it is much easier to test various software designs and APIs as coding them out takes no time. However, keeping the need of the users in mind, we will shift to C++ backend,  which will happen quickly as we would be required to just translate the tested code rather than writing it from scratch, after a few releases with APIs available for all the languages.

How to contribute?
------------------

Follow the steps given below,

1. Fork, https://github.com/codezonediitj/pydatastructs/
2. Execute, `git clone https://github.com/<your-github-username>/pydatastructs/`
3. Change your working directory to `../pydatastructs`.
4. Execute, `git remote add origin_user https://github.com/<your-github-username>/pydatastructs/`
5. Execute, `git checkout -b <your-new-branch-for-working>`.
6. Make changes to the code.
7. Add your name and email to the AUTHORS, if you wish to.
8. Execute, `git add .`.
9. Execute, `git commit -m "your-commit-message"`.
10. Execute, `git push origin_user <your-current-branch>`.
11. Make a PR.

That's it, 10 easy steps for your first contribution. For future contributions just follow steps 5 to 10. Make sure that before starting work, always checkout to master and pull the recent changes using the remote `origin` and then start following steps 5 to 10.

See you soon with your first PR.

Guidelines
----------

We recommend you to introduce yourself on our [gitter channel](https://gitter.im/codezoned2017/Lobby). You can include the courses you have taken relevant to data strucutres and algorithms, some projects, prior experience, in your introduction. This will help us to allocate you issues of suitable difficulty.

Please follow the rules and guidelines given below,

1. Follow the [numpydoc docstring guide](https://numpydoc.readthedocs.io/en/latest/format.html).
2. If you are planning to contribute a new data structure then first raise an issue for discussing the API, rather than directly making a PR.
3. For the first-time contributors we recommend not to take a complex data strucutre, rather start with `linear data structures` or `abstract data types`. You can also pick issues labelled as `good_first_issues`.

Keep contributing!!
