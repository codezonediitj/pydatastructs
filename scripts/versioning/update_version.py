import sys

from pydatastructs.utils.tests.test_code_quality import _list_files

# Files to be updated with the new version number
# The first element of the tuple is the directory path
# and the second element is a lambda function that
# returns True if the file should be updated.
FILES_TO_BE_SCANNED = {
    'pydatastructs': ('./pydatastructs', lambda _file: _file.endswith('.py')),
    'docs': ('./docs/source', lambda _file: _file.endswith('.rst') or _file.endswith('.py'))
}


def update_version_in_files(file_paths, origin_version, new_version):
    """
    Updates the version number in the specified files.

    Parameters
    ==========

    file_paths: list
        List of file paths to be updated.
    origin_version: str
        The original version number to be replaced.
    new_version: str
        The new version number to replace the original.

    Returns
    =======

    None
    """
    was_updated = False
    for path in file_paths:
        with open(path, 'r') as file:
            data = file.read()
        if origin_version in data:
            was_updated = True
            data = data.replace(origin_version, new_version)
            with open(path, 'w') as file:
                file.write(data)

    return was_updated


def main():
    if len(sys.argv) != 3:
        print('Usage: python update_version.py <origin_version> <new_version>')
        return

    origin_version, new_version = sys.argv[1], sys.argv[2]
    print(f'Updating version number from {origin_version} to {new_version}...')

    file_paths = ['README.md', 'setup.py']

    for _, (dir_path, checker) in FILES_TO_BE_SCANNED.items():
        file_paths.extend(_list_files(checker, dir_path))

    was_updated = update_version_in_files(
        file_paths, origin_version, new_version)

    if was_updated:
        print('Version number updated successfully!')
    else:
        print('WARNING: Version number not found in the specified files.')


if __name__ == "__main__":
    main()
