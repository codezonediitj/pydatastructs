import os

os.system("python scripts/build/add_dummy_submodules.py")
os.system("python setup.py build_ext --inplace")
os.system("pip install .")
os.system("python scripts/build/delete_dummy_submodules.py")
os.system("pip install . --force-reinstall")
