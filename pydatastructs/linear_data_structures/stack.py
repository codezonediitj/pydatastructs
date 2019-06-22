
from __future__ import print_function, division
from copy import deepcopy as dc

__all__ = [
    'Stack'
]

_clean = lambda x: x\
    .replace("<class '", '', 1)\
    .replace("<type '", '', 1)\
    .replace("'>", '', 1)
_check_type = lambda a, t: isinstance(a, t)
NoneType = type(None)

class Stack(object):
    """Class defination for 'Stack' datatype
    
    Parameters
    ----------
    max_size : int, optional
        Maximum size of stack allowed
    type_restriction : list, optional
        List of types(as strings) for element which can be inserted into Stack, provide empty list for no restrictions.

    Raises
    ------
    TypeError
        max_size argument should of type 'int'.
    TypeError
        type_restriction argument takes 'list' type only.
    TypeError
        All types in type_restriction list should be provided in string format

    Example
    -------
    >>> from pydatastructs import Stack
    >>> my_stack = Stack()
    >>> my_stack.push(1)
    >>> my_stack.push(2)
    >>> my_stack.pop()
    2
    >>> print(my_stack)
    <Stack length:[1]>
    """

    def __init__(
        self, max_size=10 ** 15, type_restriction=list()
    ):  # TODO: Update magic number
        if not _check_type(max_size, int):
            raise TypeError(
                "max_size argument takes 'int' type not {}".format(type(max_size))
            )
        if not _check_type(type_restriction, list):
            raise TypeError(
                "type_restriction argument takes 'list' type not {}".format(
                    type(type_restriction)
                )
            )
        self.stack = list()
        self.max_size = max_size
        self.type_restriction = list()
        for types in type_restriction:
            if not _check_type(types, str):
                raise TypeError(
                    "All types in type_restriction list should be provided in string format"
                )
            self.type_restriction.append(_clean(types))

    def push(self, element):
        """Method to push new elements in stack
        
        Parameters
        ----------
        element :
            Element to push in stack
            
        Raises
        ------
        ValueError
            If stack is full.
        TypeError
            If 'element' type does match list of types in type restriction
        """
        if len(self.stack) >= self.max_size:
            raise ValueError("Stack overflow")
        if not len(self.type_restriction) == 0:
            if _clean(str(type(element))) not in self.type_restriction:
                raise TypeError(
                    "Provided element of type {} if not allowed in stack.".format(
                        type(element)
                    )
                )
        self.stack.append(element)

    def pop(self):
        """
        pop Method for Stack
        
        Returns
        -------
            Topmost element of Stack
        """
        if len(self.stack) == 0:
            raise ValueError("Stack Undeflow")
        element = dc(self.stack[-1])
        del self.stack[-1]
        return element

    def __len__(self):
        """
        Provides length of Stack
        """
        return len(self.stack)

    def __str__(self):
        """
        Used for printing
        """
        return "<Stack length:{}>".format(str(self.stack))
