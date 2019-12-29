import os, re, sys

def _list_files():
    root_path = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.pardir, os.pardir))
    py_files = []
    for (dirpath, _, filenames) in os.walk(root_path):
        for _file in filenames:
            if re.match(r".*\.py$", _file):
                py_files.append(os.path.join(dirpath, _file))
    return py_files

def test_trailing_white_spaces():
    py_files = _list_files()
    for file_path in py_files:
        file = open(file_path, "r")
        line = file.readline()
        while line != "":
            if line.endswith(" \n") or line.endswith("\t\n"):
                assert False, "%s contains trailing whitespace at %s"%(file_path, line)
            line = file.readline()
