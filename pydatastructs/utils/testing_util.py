try:
    import pytest
except ImportError:
    raise Exception("pytest must be installed. Use `pip install pytest` "
                    "to install it.")

import os
import pathlib
import glob
import types

__all__ = ['test']


# Root pydatastructs directory
ROOT_DIR = pathlib.Path(os.path.abspath(__file__)).parents[1]


SKIP_FILES = ['testing_util.py']

def test(submodules=None, only_benchmarks=False,
         benchmarks_size=1000, **kwargs):
    """
    Runs the library tests using pytest

    Parameters
    ==========

    submodules: Optional, list[str]
        List of submodules test to run. By default runs
        all the tests
    """
    # set benchmarks size
    os.environ["PYDATASTRUCTS_BENCHMARK_SIZE"] = str(benchmarks_size)
    test_files = []
    if submodules:
        if not isinstance(submodules, (list, tuple)):
            submodules = [submodules]
        for path in glob.glob(f'{ROOT_DIR}/**/test_*.py', recursive=True):
            skip_test = False
            for skip in SKIP_FILES:
                if skip in path:
                    skip_test = True
                    break
            if skip_test:
                continue
            for sub_var in submodules:
                if isinstance(sub_var, types.ModuleType):
                    sub = sub_var.__name__.split('.')[-1]
                elif isinstance(sub_var, str):
                    sub = sub_var
                else:
                    raise Exception("Submodule should be of type: str or module")
                if sub in path:
                    if not only_benchmarks:
                        if not 'benchmarks' in path:
                            test_files.append(path)
                    else:
                        if 'benchmarks' in path:
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
            if not only_benchmarks:
                if not 'benchmarks' in path:
                    test_files.append(path)
            else:
                if 'benchmarks' in path:
                    test_files.append(path)

    extra_args = []
    if not kwargs.get("n", False) is False:
        extra_args.append("-n")
        extra_args.append(str(kwargs["n"]))

    pytest.main(extra_args + test_files)
