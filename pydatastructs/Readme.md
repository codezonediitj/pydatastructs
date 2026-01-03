# PyDataStructs

PyDataStructs is a Python library providing implementation of various data structures and algorithms, including optional C++ backend support for performance-critical components.

## Project Status

The project contains both Python implementations as well as components tha rely on compiled C++ extensions.

### Windows Support

On Windows systems, tests that depend on C++ backend may fail due to missing compiled extensions . This behavior has been seen and observed across Python 3.11.9 and Python 3.13.2 .

Pure-Python data structures (such as linear data structures,trees,and strings) function as expected on Windows.

Users working on Windows are recommended to:
- Focus on pure-python components
- Skip C++ backend-dependent tests
- Use Linux environments if full backend testing is required

## Development Notes
- Python virtual environment are stongly recommended
- Some test failures on Windows are expected and documented
- Contributions improving cross-platform support are welcome