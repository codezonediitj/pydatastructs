import os
from dummy_submodules_data import (project, modules, backend,
    cpp, dummy_submodules_list)

def delete_dummy_submodules():
    for module, dummy_submodules in zip(modules, dummy_submodules_list):
        for dummy_submodule in dummy_submodules:
            os.remove('/'.join([project, module, backend, cpp, dummy_submodule]))

delete_dummy_submodules()
