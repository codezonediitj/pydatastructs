

# initializing list 
test_list = [[1, 4, 3, 2], [5, 4, 1], [1, 4, 6, 7]] 

# printing the original list 
print ("The original list is : " + str(test_list)) 

# using sort() twice 
# sort list of lists by value and length 
test_list.sort() 
test_list.sort(key = len) 

# printing result 
print ("The list after sorting by value and length " + str(test_list)) 
