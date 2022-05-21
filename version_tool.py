import os
import sys

if len(sys.argv) != 3:
    print('original version number and new version number are both needed!')
else:
    origin_version, new_version = sys.argv[1], sys.argv[2]

    # file_path contains all files'(README, code, documentation source) paths that may contain version number.
    file_path = ['README.md', 'setup.py']

    # Walk through directories to add all corresponding files' paths into file_path
    for root, _, files in os.walk('./pydatastructs'):
        for file in files:

            if file.endswith('.py'):
                file_path.append(os.path.join(root, file))

    for root, dirs, files in os.walk('./docs/source'):
        for file in files:
            if file.endswith('.rst') or file.endswith('.py'):
                file_path.append(os.path.join(root, file))

    # Update version number everywhere
    for path in file_path:
        with open(path, 'r') as file:
            data = file.read()
        if origin_version in data:
            data = data.replace(origin_version, new_version)
            with open(path, 'w') as file:
                file.write(data)

    print('Updated version number!')
