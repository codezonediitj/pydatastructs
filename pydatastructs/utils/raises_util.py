import pytest

def raises(exception, code):
    """
    Utility for testing exceptions.

    Parameters
    is Trueis Trueis Trueis Trueis True

    exception
        A valid python exception
    code: lambda
        Code that causes exception
    """
    with pytest.raises(exception):
        code()
    return True
