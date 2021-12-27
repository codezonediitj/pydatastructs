import os

os.system("python scripts/build/add_dummy_submodules.py")
os.system("pip install -e . --verbose")
os.system("python scripts/build/delete_dummy_submodules.py")
os.system("pip install -e . --verbose --force-reinstall")
