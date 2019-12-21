import pytest

def raises(exception, code):
    """
    Utility for testing exceptions.

    Parameters
    ==========

    exception
        A valid python exception
    code: lambda
        Code that causes exception
    """
    with pytest.raises(exception):
        code()
    return True
