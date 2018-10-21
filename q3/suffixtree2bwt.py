#NAME   : CALUM LIM SHENG EN
#ID     : 27372537
#TITLE  : Assignment #1 - Question 3

import sys

#A class object which contains the variables and functions for a Node object.
class Node:

    def __init__(self):
        self.edge_arr = [0]*27
        self.linkNode = None
        self.nodePos = 0

    #A function to add an edge to the edge array, according to its first character
    def addEdge(self, char, edge):
        if char!="$":
            ind = ord(char)-96
            self.edge_arr[ind] = edge
        else:
            self.edge_arr[0] = edge

    #A function which returns the edge corresponding to the character input
    def searchEdge(self, char):
        if char!="$":
            return self.edge_arr[ord(char)-96]
        else:
            return self.edge_arr[0]

#A class object which contains the variables of an Edge object
class Edge:

    #Initialisation of the Edge class variables, label to store the string
    #for the edge, prevNode to store the previous Node object of the Edge,
    #and lastNode to store the ending Node object of the Edge
    def __init__(self, label):
        self.label = label
        self.prevNode = None
        self.lastNode = None

#A class object which represents the global end value for the Ukkonen's suffix
#tree
class GlobalEnd:

    def __init__(self):
        self.globalend = 0

    #A function to increment the global end value by 1
    def add(self):
        self.globalend+=1

#A class object which contains the variables and functions to construct a suffix
#tree using Ukkonen's Linear Time Complexity suffix tree construction algorithm.
class SuffixTree:

    #Initialisation of the variables
    def __init__(self, txt):
        self.txt = txt
        self.r = Node()
        self.globalend = GlobalEnd()
        self.constructTree(self.txt)
        BWT_txt = self.constructBWT(self.txt, self.r, [])
        self.outputFile(BWT_txt)

    #A function to fascilitate the creation of a new edge within the tree
    def createEdge(self, found_edge, ind, globalend, previousNode, txt):
        newEdge = Edge([ind, globalend])
        newEdge.prevNode = previousNode
        previousNode.addEdge(txt[ind], newEdge)
        return newEdge

    #A function to fascilitate the creation of a new edge together with the
    #creation of an intermediate node that connects the splitted label.
    def createExtensionEdge(self, found_edge, i, ind, boundary):
        f_label = [found_edge.label[0], found_edge.label[0]+i-ind]
        l_label = [found_edge.label[0]+i-ind+1, found_edge.label[1]]
        found_edge.label = f_label
        extensionNode = Node()
        l_edge = Edge(l_label)
        l_edge.prevNode = extensionNode
        l_edge.lastNode = found_edge.lastNode
        found_edge.lastNode = extensionNode
        extensionNode.addEdge(txt[l_label[0]], l_edge)
        extensionNode.nodePos = boundary
        return extensionNode

    #A function that fascilitates the process of creating a suffix link for
    #the suffix tree
    def suffixLink(self, linkingNode, found_edge, traverse_len):
        if linkingNode!=None:
            linkingNode.linkNode = found_edge.prevNode
            linkingNode.linkNode.nodePos = traverse_len
            return None
        else:
            return linkingNode

    #A function that checks if rule 3 applies in the current traversal, if yes,
    #the function returns i+1 so that no further action can be done
    def checkCriterion(self, found_edge, globalend, ind, i):
        if found_edge.label[1]==self.globalend:
            if ind>found_edge.label[0] and ind<found_edge.label[1].globalend:
                ind=i+1
        else:
            if ind>found_edge.label[0] and ind<found_edge.label[1]:
                ind=i+1
        return ind

    #A function that writes the Burrows-Wheeler Transform to a text file.
    def outputFile(self, txt):
        f = open("output_bwt.txt", "w")
        f.write(txt.rstrip())
        f.close()

    #A function that constructs the Burrows-Wheeler Transform based on the
    #constructed suffix tree, it traverses through the tree lexicographically
    #and when a leaf edge is found, a mathematical formula is used in order to
    #obtain the index of the last character of the rotational suffix. It is then
    #appended into an array which is then iterated through to obtain the last characters
    #of the rotaional suffixes. The final BWT text is then returned.
    def constructBWT(self, txt, root, arr):
        edge_arr = root.edge_arr
        n = len(root.edge_arr)

        for i in range(n):
            if edge_arr[i]!=0:
                if edge_arr[i].lastNode!=None:
                    self.constructBWT(txt, edge_arr[i].lastNode, arr)
                else:
                    len_label = edge_arr[i].label[1].globalend-edge_arr[i].label[0]
                    endPos = root.nodePos+len_label
                    arr.append(len(txt)-endPos-2)

        if len(arr)==len(txt):
            BWT = ""
            for i in range(len(arr)):
                BWT+=txt[arr[i]]
            return BWT

    #The main function which constructs the Suffix Tree based on Ukkonen's algorithm
    #This algorithm uses the three rules of ukkonen's construction of suffix trees,
    #suffix links, general extension procedure, space saving efficiency method,
    #skip/count trick, premature extension stopping criterion, and fast leaf extension
    #trick. Alltogether the algorithm runs in O(N) time for a string[1...n]
    def constructTree(self, txt):
        root = self.r
        n = len(txt)
        linkingNode = None

        #inserting the first suffix
        firstChar = Edge([0,self.globalend])
        firstChar.prevNode = root
        root.addEdge(txt[0], firstChar)
        last = 0

        #constructing the tree
        for i in range(1,n):
            j=last
            self.globalend.add()

            #initiating a while loop based on the "last"ij value,
            #this will allow the algorithm to skip many unwated comparisons
            while j<i+1:
                ind = j
                traverse_len = 0

                #traversing the tree using the skip/count method
                #if an edge can be found from the root:
                if root.searchEdge(txt[ind])!=0:
                    found_edge = root.searchEdge(txt[ind])
                    boundary = i-ind+1

                    #initiate a while loop based on if ind is lesser than i
                    while ind<i:
                        ind+=1
                        if found_edge.label[1]==self.globalend:
                            len_label = found_edge.label[1].globalend-found_edge.label[0]+1
                        else:
                            len_label = found_edge.label[1]-found_edge.label[0]+1
                        traverse_len+=len_label

                        #if the traversing has reached its limit
                        if traverse_len==boundary and ind<=i:
                            #check for criterion/premature stopping
                            ind = self.checkCriterion(found_edge, self.globalend, ind, i)
                            #if the edge is a leaf: does not have children
                            if found_edge.lastNode==None:
                                ind = i+1
                                last+=1
                                #suffix link to another node if a link exists
                                if found_edge.prevNode.linkNode!=None and found_edge.prevNode.linkNode!=self.r:
                                    ind = found_edge.label[0]
                                    traverse_len = found_edge.prevNode.linkNode.nodePos+1
                                    if found_edge.prevNode.linkNode.searchEdge(txt[ind])!=0:
                                        found_edge = found_edge.prevNode.linkNode.searchEdge(txt[ind])
                                    else:
                                        found_edge = self.createEdge(found_edge, ind, self.globalend,found_edge.prevNode.linkNode,txt)
                                        last+=1
                                    ind+=1
                            #if the edge is not a leaf, traverse to the next edge and apply any suffix links
                            else:
                                if found_edge.lastNode.searchEdge(txt[ind])!=0:
                                    found_edge = found_edge.lastNode.searchEdge(txt[ind])
                                    linkingNode = self.suffixLink(linkingNode, found_edge, traverse_len)
                                    ind = i+1

                        #traversing the edges using the skip/count method
                        elif traverse_len<boundary and ind<=i and found_edge.lastNode!=None:
                            ind+=len_label-1
                            if found_edge.lastNode.searchEdge(txt[ind])!=0:
                                found_edge = found_edge.lastNode.searchEdge(txt[ind])
                            #if an edge cannot be found, create a new one
                            else:
                                found_edge = self.createEdge(found_edge, ind, self.globalend, found_edge.lastNode, txt)
                                last+=1

                        #extension with an intermediary node if there is a mismatch between i and the label
                        elif traverse_len>=boundary and ind<=i and traverse_len<=n and txt[found_edge.label[0]+i-ind+1] != txt[i]:
                            #splitting the label and creating the extension Node
                            extensionNode = self.createExtensionEdge(found_edge, i, ind, boundary-1)
                            ind = i
                            #creating the extension edge
                            found_edge = self.createEdge(found_edge, ind, self.globalend, extensionNode, txt)
                            linkingNode = extensionNode
                            #checking for any queued up suffix links
                            if j+2==i+1 and root.searchEdge(txt[ind])!=0:
                                linkingNode.linkNode = root.searchEdge(txt[ind]).prevNode
                                linkingNode = None
                            last+=1
                #else if an edge cannot be found from the root, make a new edge, applying rule 2
                else:
                    found_edge = self.createEdge(found_edge, ind, self.globalend, root, txt)
                    last+=1
                    #checking for any queued up suffix links
                    linkingNode = self.suffixLink(linkingNode, found_edge, traverse_len)
                j+=1


if __name__ == "__main__":

    txtInp = open(sys.argv[1], "r")
    txt = txtInp.read()+"$"
    Tree = SuffixTree(txt)
