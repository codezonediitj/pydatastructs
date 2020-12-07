"""
Subset Sum Function which can be used in many problems 
like Subset Sum, Equal Sum Partition, Count of Subsets 
Sum with given sum, Minimum Subset Sum Difference, Count 
the number of Subset with given difference, Target Sum etc.

Parameters : 
==============
arr: list containing item array
sum1: Required sum
n: size of arr list
"""

def subsetsum(arr, sum1, n):
    t = [[0]*(sum1+1)]*(n+1)
    for i in range(0, n+1):
        t[i][0]=True
    for i in range(1, sum1+1):
        t[0][i]=False
    for i in range(1, n+1):
        for j in range(1,sum1+1):
            if arr[i-1]<=j:
                t[i][j] = t[i][j-arr[i-1]] or t[i-1][j]
            else:
                t[i][j] = t[i-1][j]
    return t[n][sum1]

"""
Subset Sum function is derived from 01 Knapsack and is based on concept 
of Dynamic Programming.
"""