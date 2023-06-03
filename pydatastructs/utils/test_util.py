try:
    import pytest
except ImportError:
    raise Exception("pytest must be installed. Use `pip install pytest` "
                    "to install it.")

import os
import pathlib
import glob

__all__ = ['test']


# Root pydatastructs directory
ROOT_DIR = pathlib.Path(os.path.abspath(__file__)).parents[2]


def test(**kwargs):
    test_files = []
    for path in glob.glob(f'{ROOT_DIR}/**/test_*.py', recursive=True):
        test_files.append(path)
    extra_args = []
    if not kwargs.get("n", False) is False:
        extra_args.append("-n")
        extra_args.append(str(kwargs["n"]))

    pytest.main(extra_args + test_files)
