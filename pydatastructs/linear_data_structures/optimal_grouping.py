from types import *
from typing import List


def get_value(matrix, lookup_index: List[int]):
    """
    gets a value
    """
    return matrix[lookup_index[0]][lookup_index[1]]


def set_value(matrix, lookup_index: List[int], value):
    """
    sets a value
    """
    matrix[lookup_index[0]][lookup_index[1]] = value


def compare(maximize: bool, value, compareWith=None):
    """
    compares a value with another. if compareWith is None then value is compared with Infinity or -Infinity
    parameters
        [maximize] if True then the function returns true if value is greater than compareWith and vice versa
    """
    if compareWith == None:
        if maximize:
            compareWith = float('-inf')
        else:
            compareWith = float('inf')
    if maximize:
        return value > compareWith
    return value < compareWith


def initialize_arrays(maximize: bool, rows: int, columns: int):
    """
    returns a 2-d array of rows*columns size filled with either Infinity or -Infinity
    parameters:
        [maximize]
            if 'True' fills with -Infinity and vice versa
        [rows]
            expects a number 
        [columns]
            expects a number
    """
    value = float('inf')
    if maximize:
        value = float('-inf')
    return [[value for a in range(0, columns+1)] for a in range(0, rows+1)]


def optimal_grouping_rec(object_arr, cost_storage: List[List[int]], solution_matrix: List[List[int]], maximize_prob: bool, min_compare_len: int, lookup_index: List[int], get_lookup_fn, cost_fn):
    """
    Helper function for optimal_grouping function
    """

    # gets the present value at the present index
    present_value = get_value(cost_storage, lookup_index)
    # return the present value if it is not infinity
    if compare(maximize_prob, present_value):
        return present_value

    # get the start and end indices where end index depends on the min_compare_len
    start_index = lookup_index[0]
    end_index = lookup_index[1]+1-(min_compare_len-1)

    if start_index == end_index or start_index > end_index:
        cost = cost_fn(object_arr, lookup_index, start_index)
        if compare(maximize_prob, cost, present_value):
            set_value(cost_storage, lookup_index, cost)
            set_value(solution_matrix, lookup_index, start_index)
            present_value = cost

    for i in range(start_index, end_index):

        # get indices for left recursion tree
        left_rec_indices = get_lookup_fn('before', lookup_index, i)
        test_lookup_function(left_rec_indices, lookup_index)

        cost = optimal_grouping_rec(object_arr, cost_storage, solution_matrix, maximize_prob,
                                    min_compare_len, left_rec_indices, get_lookup_fn, cost_fn)

        # get indices for right recursion tree
        right_rec_indices = get_lookup_fn('after', lookup_index, i)
        test_lookup_function(right_rec_indices, lookup_index)

        cost = cost+optimal_grouping_rec(object_arr, cost_storage, solution_matrix, maximize_prob,
                                         min_compare_len, right_rec_indices, get_lookup_fn, cost_fn)

        # get cost for present partition
        cost = cost+cost_fn(object_arr, lookup_index, i)

        # update the values if this is the best solution until now
        if compare(maximize_prob, cost, present_value):
            set_value(cost_storage, lookup_index, cost)
            set_value(solution_matrix, lookup_index, i)
            present_value = cost

    return present_value


def test_lookup_function(lookup_index: List[int], input_index: List[int]):
    if lookup_index is None:
        raise TypeError(
            'Check lookup_function: returning wrong type should return an array of start and end index')

    if lookup_index.__len__() < 2:
        raise ValueError(
            'Check lookup_function:lookup index should at least have 2 integer items, first specifying the start and second specifying the last indices')

    if input_index == lookup_index:
        raise RuntimeError(
            'Check lookup_function:verify get_lookup_fn giving same output as input which will lead to infinite loop')


def optimal_grouping(process_objects, maximize_prob: bool, min_compare_len: int, lookup_index: List[int], get_lookup_fn, cost_fn):
    """
    Description: Optimal Grouping groups given set of objects using the given cost function 

    Parameters:
     object_arr
        accepts array of objects on which the algorithm is supposed to run
     maximize_prob 
        pass True if the algorithm should find maximum value of the cost function otherwise pass False
     min_compare_len 
        a positive number decides to which level of gap the algorithm can maintain while iterating from start to end,
        for example-> if minimun length is 2 then it can only iterate if endIndex=startIndex+2
     lookup_index 
        format-->[start_index,endIndex] algorithm runs from start to end
     get_lookup_fn
      should return next range of indices
      sample -> get_lookup_fn(position, rangeIndices, currentIndex)
       position is either 'before' or 'after' 
       rangeIndices is the present range of index like [start_index,endIndex]
     cost_fn
      should return the cost 
      sample -> cost_fn(object_arr,rangeIndices,currentIndex)


      **Usage examples : 

      1.OPTIMAL BINARY SEARCH TREE

        from binarytree import Node
        n = 5
        p = [None, Node(0.15), Node(0.10), Node(0.05), Node(0.10), Node(0.20)]
        q = [Node(0.05), Node(0.10), Node(0.05), Node(0.05), Node(0.05), Node(0.10)]


        def lookup(position, endIndex, middle):
            if position is 'before':
             return [endIndex[0], middle-1]
            else:
             return [middle+1, endIndex[1]]


        def cost(obj, endIndex, middle):

            if(endIndex[1]<endIndex[0]):
                return obj['q'][endIndex[1]].value

            sum = 0
            for i in range(endIndex[0], endIndex[1]+1):
                sum += obj['p'][i].value
            for i in range(endIndex[0]-1, endIndex[1]+1):
                sum += obj['q'][i].value
            return sum


        print(optimal_grouping({'p': p, 'q': q},  False, 1, [1, n], lookup, cost))



      2.MATRIX CHAIN MULTIPLICATION

        def cost(matrix, endIndex, middle):

            if endIndex[0] == endIndex[1]:
            return 0
        return matrix[endIndex[0]-1]*matrix[middle]*matrix[endIndex[1]]


        def lookup(position, endIndex, middle):
        if position is 'before':
            return [endIndex[0], middle]
        else:
            return [middle+1, endIndex[1]]


        print(optimal_grouping([30, 35, 15, 5, 10, 20, 25], False, 2, [1, 6], lookup, cost))

    """

    if process_objects is None:
        raise TypeError('process_objects cannot be none')

    if maximize_prob is None:
        raise TypeError(
            'maximize_prob cannot be none')

    if min_compare_len is None:
        raise TypeError(
            'min_compare_len cannot be none')
    if min_compare_len < 1:
        raise ValueError(
            'min_compare_len should be a positive integer')

    if lookup_index is None:
        raise TypeError(
            'lookup_index cannot be none')
    if lookup_index.__len__() < 2 or lookup_index[0] > lookup_index[1]:
        raise ValueError(
            'lookup index should at least have 2 integer items, first specifying the start and second specifying the last indices')

    if get_lookup_fn is None or type(get_lookup_fn) is not FunctionType:
        raise TypeError(
            'get_lookup_fn cannot be none and should be a function with 3 arguments')

    test_result = get_lookup_fn('before', lookup_index, lookup_index[0])
    if test_result == lookup_index:
        raise RuntimeError(
            'verify get_lookup_fn giving same output as input which may lead to infinite loop')
    test_result = get_lookup_fn('after', lookup_index, lookup_index[0])
    if test_result == lookup_index:
        raise RuntimeError(
            'verify get_lookup_fn giving same output as input which may lead to infinite loop')

    if cost_fn is None or type(cost_fn) is not FunctionType:
        raise TypeError(
            'cost_fn cannot be none and should be a function with 3 arguments')

    test_result = cost_fn(process_objects, lookup_index, lookup_index[0])
    try:
        int(test_result)
    except Exception:
        raise TypeError(
            'output for cost function should be any type of number')
    if test_result is None:
        raise RuntimeError(
            'output for cost function should be any type of number and cannot be None')

    #  end of edge cases

    length = lookup_index[1]-lookup_index[0]+1

    # for storing the computed values (helper array)
    cost_storage = initialize_arrays(maximize_prob, length+1, length+1)
    #  for storing the solutions
    solution_matrix = initialize_arrays(maximize_prob, length+1, length+1)

    optimal_grouping_rec(process_objects, cost_storage, solution_matrix, maximize_prob,
                         min_compare_len, lookup_index, get_lookup_fn, cost_fn)
    return solution_matrix