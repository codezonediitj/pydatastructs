import os
import argparse
import subprocess
import sys

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}", file=sys.stderr)
        sys.exit(result.returncode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build and install pydatastructs.")
    parser.add_argument("--clean", action="store_true", help="Execute `git clean -fdx`")
    args = parser.parse_args()

    if args.clean:
        response = input("Warning: Executing `git clean -fdx` [Y/N]: ")
        if response.lower() in ("y", "yes"):
            run_cmd("git clean -fdx")
        else:
            print("Skipping clean step.")

    run_cmd("python scripts/build/add_dummy_submodules.py")
    run_cmd("python setup.py build_ext --inplace")
    run_cmd("python -m pip install .")
    run_cmd("python scripts/build/delete_dummy_submodules.py")
    run_cmd("python -m pip install . --force-reinstall")
