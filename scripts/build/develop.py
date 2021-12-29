import os, argparse

parser = argparse.ArgumentParser(description='Process build options.')
parser.add_argument('--clean', type=bool, default=False,
                    help='Execute `git clean -fdx` (default 0)')

build_options = parser.parse_args()

if build_options.clean:
    response = input("Warning: Executing `git clean -fdx` [Y/N]: ")
    if response.lower() in ("y", "yes"):
        os.system("git clean -fdx")

os.system("python scripts/build/add_dummy_submodules.py")
os.system("pip install -e . --verbose")
os.system("python scripts/build/delete_dummy_submodules.py")
os.system("pip install -e . --verbose --force-reinstall")
