import os, re, sys

def _list_files():
    root_path = os.path.abspath(
                os.path.join(
                os.path.split(__file__)[0],
                os.pardir, os.pardir))
    py_files = []
    for (dirpath, _, filenames) in os.walk(root_path):
        for _file in filenames:
            if re.match(r".*\.py$", _file):
                py_files.append(os.path.join(dirpath, _file))
    return py_files

py_files = _list_files()

def test_trailing_white_spaces():
    for file_path in py_files:
        file = open(file_path, "r")
        line = file.readline()
        while line != "":
            if line.endswith(" \n") or line.endswith("\t\n") \
                or line.endswith(" ") or line.endswith("\t"):
                assert False, "%s contains trailing whitespace at %s"\
                               %(file_path, line)
            line = file.readline()
        file.close()

def test_final_new_lines():
    for file_path in py_files:
        file = open(file_path, "r")
        lines = []
        line = file.readline()
        while line != "":
            lines.append(line)
            line = file.readline()
        if lines:
            if lines[-1][-1] != "\n":
                assert False, "%s doesn't contain new line at the end."%(file_path)
            if lines[-1] == "\n" and lines[-2][-1] == "\n":
                assert False, "%s contains multiple new lines at the end."%(file_path)
        file.close()

def test_comparison_True_False_None():
    for file_path in py_files:
        if file_path.find("test_code_quality.py") == -1:
            file = open(file_path, "r")
            line = file.readline()
            while line != "":
                if ((line.find("== True") != -1) or
                    (line.find("== False") != -1) or
                    (line.find("== None") != -1) or
                    (line.find("!= True") != -1) or
                    (line.find("!= False") != -1) or
                    (line.find("!= None") != -1)):
                    assert False, "%s compares True/False/None using by "\
                                "value, should be done by reference at %s"\
                                %(file_path, line)
                line = file.readline()
            file.close()

def test_presence_of_tabs():
    for file_path in py_files:
        file = open(file_path, "r")
        line = file.readline()
        while line != "":
            line = file.readline()
            if (line.find('\t') != -1):
                assert False, "Tab present at %s in %s. " \
                            "Configure your editor to use " \
                            "white spaces."%(line, file_path)
        file.close()
