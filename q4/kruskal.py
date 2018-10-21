#NAME   : CALUM LIM SHENG EN
#ID     : 27372537
#TITLE  : Assignment #1 - Question 4

import sys

#A class object which contains the variables and functions to create a union_by_height
#disjoint data structure to obtain the minimum spanning tree.
class UBH:

    #Initialisation of the variables used to construct the minimum spanning tree.
    def __init__(self, input_file):
        self.arr_ubh = []
        self.arr_MST = []
        self.arr_graph = self.readFile(input_file)
        self.heapSort(self.arr_graph)
        self.kruskalMST()

    #A function that swaps the positions of two indexes give both indexes
    def swap(self, arr, i, j):
        arr[i],arr[j] = arr[j], arr[i]
        return arr

    #A function which inputs the given input file into an array for computation
    def readFile(self, readF):
        arr_graph = []
        max_vertex = 0
        for line in readF:
            line = line.strip('\n')
            line = line.split(' ')
            for i in range(len(line)):
                line[i] = int(line[i])
                if i==0 and line[i]>max_vertex:
                    max_vertex = line[i]
                if i==1 and line[i]>max_vertex:
                    max_vertex = line[i]
            arr_graph.append(line)
        self.arr_ubh = [-1]*max_vertex
        return arr_graph

    #A function that balances the heap.
    def heapify(self, array, n, x):
        root = x
        right = 2*x+2
        left = 2*x+1
        #checking the left child
        if left<n:
            arr_left = array[left][2]
            arr_k = array[x][2]
            if arr_left>arr_k:
                root = left
        #checking the right child
        if right<n:
            arr_right = array[right][2]
            arr_root = array[root][2]
            if arr_right>arr_root:
                root = right
        #if the root is not the same anymore
        if root!=x:
            array = self.swap(array, x, root)
            self.heapify(array, n, root)

    #A function which implements the heapsort algorithm, it sorts the given
    #values in O(NlogN) time complexity
    def heapSort(self, array):
        k = len(array)
        
        #building a max heap
        for j in range(k, -1, -1):
            self.heapify(array, k, j)
            
        #extracting the elements
        for j in range(k-1, 0, -1):
            array = self.swap(array, 0, j)
            self.heapify(array, j, 0)

    #A function that searches the array and returns the index only when
    #the index is lesser than 0
    def search(self, k):
        arr = self.arr_ubh
        if arr[k]<0:
            return k
        else:
            arr[k] = self.search(arr[k])
            return arr[k]

    #A function that performs a union based on the height/rank of the position
    #of the array, based of that, the minimum spanning tree can be found by simply
    #appending the values when root of x is not in the same set of root y.
    #Code referenced from: FIT3155 Lecture Slides Week 4
    def union_by_height(self, w, x, y):
        arr = self.arr_ubh
        root_x = self.search(x)
        root_y = self.search(y)

        #if the root for both vertices are already in the same set, return prematurely
        if root_x == root_y:
            return
        #found vertices for the minimum spanning tree, append it into the array
        self.arr_MST.append([x+1,y+1, w])

        #updating the height/rank values
        height_x = -arr[root_x]
        height_y = -arr[root_y]
        if height_x > height_y:
            arr[root_y] = root_x
        elif height_y > height_x:
            arr[root_x] = root_y
        else:
            arr[root_x] = root_y
            arr[root_y] = -(height_y+1)

    #A function which iterates through all of the vertices given in the input
    #file which is then inserted into the disjoint data set by using the union_by_height
    #function. From there, the minimum spanning tree will be constructed.
    def kruskalMST(self):
        graph = self.arr_graph
        for i in range(len(graph)):
            u = graph[i][0]-1
            v = graph[i][1]-1
            w = graph[i][2]
            self.union_by_height(w, u, v)
        return self.outputFile(self.arr_MST)

    #A function that iterates through the output array, then writes each line
    #into a file named output_kruskal.txt
    def outputFile(self, array):
        n = len(array)
        f = open("output_kruskal.txt", 'w')
        for i in range(n):
            if i!=n-1:
                line = str(array[i][0])+" "+str(array[i][1])+" "+str(array[i][2])+"\n"
            else:
                line = str(array[i][0])+" "+str(array[i][1])+" "+str(array[i][2])
            f.write(line)
        f.close()


if __name__=="__main__":
    verticesInput = open(sys.argv[1], "r")
    MST = UBH(verticesInput)
