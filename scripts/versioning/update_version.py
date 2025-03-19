import sys

from pydatastructs.utils.tests.test_code_quality import _list_files


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

    pydatastructs_files = _list_files(lambda _file: _file.endswith('.py'),
                                      './pydatastructs')
    docs_files = _list_files(lambda _file: _file.endswith('.rst') or _file.endswith('.py'),
                             './docs/source')
    file_paths = ['README.md', 'setup.py'] + pydatastructs_files + docs_files

    was_updated = update_version_in_files(
        file_paths, origin_version, new_version)

    if was_updated:
        print('Version number updated successfully!')
    else:
        print('WARNING: Version number not found in the specified files.')


if __name__ == "__main__":
    main()
