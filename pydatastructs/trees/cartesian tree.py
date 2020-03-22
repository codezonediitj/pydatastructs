class node:
    def __init__(self,data):
        self.data=data
        self.left=None
        self.right=None 


class CartesianTree:
    def __init__(self,arr):
        self.arr=arr

    def printInorder(self,root):

        if root==None:
            return
        self.printInorder(root.left)
        print(root.data,end=' ')
        self.printInorder(root.right)

    def buildhelper(self,root,arr,parent,leftchild,rightchild):
        if root==-1:
            return None

        temp=node(arr[root])

        temp.left=self.buildhelper(leftchild[root],arr,parent,leftchild,rightchild)
        temp.right=self.buildhelper(rightchild[root],arr,parent,leftchild,rightchild)

        return temp

    def buildCartesiantree(self,arr):
        parent= [-1]*len(arr)
        leftchild=[-1]*len(arr)
        rightchild=[-1]*len(arr)
        
        root=0
        for i in range(1,n):
            last=i-1
            rightchild[i]=-1

            while(arr[last]<=arr[i] and last!=root):
                last=parent[last]

            if arr[last]<=arr[i]:

                parent[root]=i
                leftchild[i]=root
                root=i

            elif rightchild[last]==-1:

                rightchild[last]=i
                parent[i]=last
                leftchild[i]=-1

            else:

                parent[rightchild[last]]=i
                leftchild[i]=rightchild[last]
                rightchild[last]=i
                parent[i]=last

        parent[root]=-1

        return self.buildhelper(root,arr,parent,leftchild,rightchild)

    

    def cartesiansort(self,root):
        myPq = PriorityQueue()
        myPq.insert(root)
        sorted_ar=[]
        temp=root
        print("Array in sorted decreasing order is")
        while(myPq.isEmpty() is False):
            temp=myPq.delete()
            print(temp.data,end=' ')
            sorted_ar.append(temp.data)
            if(temp.left):
                myPq.insert(temp.left)
            if(temp.right):
                myPq.insert(temp.right)

        return sorted_ar

class PriorityQueue(): 
        def __init__(self): 
            self.queue = [] 

        def isEmpty(self): 
            return len(self.queue) == [] 
      
        def insert(self, data): 
            self.queue.append(data) 
      
        def delete(self): 
            try: 
                max = 0
                for i in range(len(self.queue)): 
                    if self.queue[i].data > self.queue[max].data: 
                        max = i 
                item = self.queue[max] 
                del self.queue[max] 
                return item 
            except IndexError: 
                print() 
                exit()