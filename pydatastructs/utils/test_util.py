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


SKIP_FILES = ['test_util.py']

def test(submodules=None, **kwargs):
    """
    Runs the library tests using pytest

    Parameters
    ==========

    submodules: Optional, list[str]
        List of submodules test to run. By default runs
        all the tests
    """
    test_files = []
    if submodules:
        if isinstance(submodules, str):
            submodules = [submodules]
        for path in glob.glob(f'{ROOT_DIR}/**/test_*.py', recursive=True):
            skip_test = False
            for skip in SKIP_FILES:
                if skip in path:
                    skip_test = True
                    break
            if skip_test:
                continue
            for sub in submodules:
                if sub in path:
                    test_files.append(path)
                    break
    else:
        for path in glob.glob(f'{ROOT_DIR}/**/test_*.py', recursive=True):
            skip_test = False
            for skip in SKIP_FILES:
                if skip in path:
                    skip_test = True
                    break
            if skip_test:
                continue
            test_files.append(path)

    extra_args = []
    if not kwargs.get("n", False) is False:
        extra_args.append("-n")
        extra_args.append(str(kwargs["n"]))

    pytest.main(extra_args + test_files)
