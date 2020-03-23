def cocktailSort(a):
   n = len(a)
   flag = True
   start = 0
   end = n-1
   while (flag==True):
      # to ignore the result of the previous iteration
      flag = False
      # left to right traversal
      for i in range (start, end):
         if (a[i] > a[i+1]) :
            a[i], a[i+1]= a[i+1], a[i]
            flag=True
      # if no swap takes place array remains sorted
      if (flag==False):
         break
      # otherwise, reset the flag
      flag = False
      # last item is aldready sorted
      end = end-1
      # iteration from right to left
      for i in range(end-1, start-1,-1):
         if (a[i] > a[i+1]):
            a[i], a[i+1] = a[i+1], a[i]
            flag = True
      # first element is already sorted
      start = start+1
