from dummy_submodules_data import (project, modules, backend,
    cpp, dummy_submodules)

def add_dummy_submodules():
    for module, dummy_submodule in zip(modules, dummy_submodules):
        open('/'.join([project, module, backend, cpp, dummy_submodule]), 'w+').close()

add_dummy_submodules()
