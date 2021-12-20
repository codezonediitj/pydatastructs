import os
from dummy_submodules_data import (project, modules, backend,
    cpp, dummy_submodules)

def delete_dummy_submodules():
    for module, dummy_submodule in zip(modules, dummy_submodules):
        os.remove('/'.join([project, module, backend, cpp, dummy_submodule]))

delete_dummy_submodules()