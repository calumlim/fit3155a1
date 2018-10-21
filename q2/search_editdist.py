#NAME   : CALUM LIM SHENG EN
#ID     : 27372537
#TITLE  : Assignment #1 - Question 2

import sys

#A class object which contains the functions to find the pattern in the text with a edit distance<=1
class ZBox:

    #Initialisation of the variables within the ZBox class
    #dollarInd to keep track of the index of the dollar sign within the fulltxt
    def __init__(self, txt, pat):
        self.dollarInd = 0
        self.fulltxt = self.readFiles(txt, pat)
        self.n = len(self.fulltxt)
        self.z_arr = [0]*self.n
        self.z_arr[0] = self.n - self.dollarInd
        self.rev_fulltxt = self.reverse_string(self.fulltxt[0:self.dollarInd], self.fulltxt[self.dollarInd+1:])
        self.patternSearch(self.fulltxt, self.rev_fulltxt)

    #Function to generate the {pat + $ + txt} text
    def readFiles(self, txt, pat):
        fulltxt = ""
        fulltxt+=pat + "$"
        self.dollarInd = len(fulltxt)-1
        fulltxt+=txt
        return fulltxt

    #Function to reverse a string, returns the reversed string
    def reverse_string(self, pat, txt):
        fulltxt = ""
        for i in range(len(pat)-1,-1,-1):
            fulltxt+=pat[i]
        fulltxt+="$"
        for i in range(len(txt)-1,-1,-1):
            fulltxt+=txt[i]
        return fulltxt

    #Function to create a Z Array by using Z boxes. The function has a left_boundary
    #and a right_boundary to keep track of the indexes of the box. The function
    #iterates through the array starting from the dollar index until the end of
    #the text. It then calculates the Z Array index using the Z Box method.
    #Code Referenced From: (Ian) Wern Han Lim (Malaysian Tutor)
    def constructZArray(self, txt):
        arr = self.z_arr
        left_boundary = 0
        right_boundary = 0

        #Iteration through the text starting from the dollar sign index
        for i in range(self.dollarInd+1, self.n):
            #if i is larger than the boundary, set up a counter together
            #with a while loop. Replace the array index value with the
            #counter's value to update it.
            if i>right_boundary:
                counter = 0
                while i+counter < self.n and txt[counter] == txt[i+counter]:
                    counter+=1
                arr[i] = counter
                if counter>0:
                    left_boundary = i
                    right_boundary = i+counter-1
            #Else if i is smallerthan the boundary, set up a prefix index together
            #with a remainder variable.
            else:
                index = i-left_boundary
                remainder = right_boundary-i+1
                #If the array for the prefix index is smaller than the value of
                #remainder
                if arr[index] < remainder:
                    arr[i] = arr[index]
                #If the array for the prefix index is equals to the value of the
                #remainder
                elif arr[index] == remainder:
                    updated_right = right_boundary+1
                    while updated_right<self.n and txt[updated_right] == txt[updated_right-i]:
                        updated_right+=1
                    arr[i] = updated_right-i

                    left_boundary = i
                    right_boundary = updated_right-1
                #If the array for the prefix index is more than the value of the
                #remainder
                else:
                    arr[i] = remainder
        self.z_arr = arr
        return arr

    #A function that iterates through the Z Array and determines if there is a position
    #within the Z Array that has a edit distance of <=1, it does this by
    #computing two Z Arrays, one that is in order, and another which is reversed.
    #The function then determines if the position has a hamming distance of <=1
    #by adding the two corresponding values to get the total number of matches.
    #If the corresponding value of the reversed Z Array is 0, then k+1 and k-1 will
    #be checked for any insertion or deletion cases.
    def patternSearch(self, txt, rev_txt):
        #initiating the Z Arrays
        start_ind = self.dollarInd+1
        pat_len = start_ind-2
        z_arr=self.constructZArray(txt)[start_ind:]
        rev_z_arr=self.constructZArray(rev_txt)[start_ind:]
        editdist_arr = []
        #iterating through the array find for edit distance <= 1
        for i in range(len(z_arr)):
            neg_ind = -i-start_ind+1
            if i==len(z_arr)-pat_len:
                if z_arr[i]==pat_len or rev_z_arr[0]==pat_len:
                    editdist_arr.append([i+1, 1])
                    break
            if i+pat_len<len(z_arr):
                editdist = z_arr[i]+rev_z_arr[neg_ind]
                if rev_z_arr[neg_ind]!=0 or z_arr[i]==pat_len+1:
                    #substitution case
                    if editdist==pat_len:
                        editdist_arr.append([i+1, 1])
                    elif editdist>pat_len:
                        editdist_arr.append([i+1, 0])
                else:
                    #deletion or insertion
                    if -(neg_ind-1)<=len(z_arr):
                        left = z_arr[i]+rev_z_arr[neg_ind-1]
                        right = z_arr[i]+rev_z_arr[neg_ind+1]
                        #deletion
                        if left==pat_len+1 or left==pat_len+2:
                            editdist_arr.append([i+1, 1])
                        #insertion
                        elif right==pat_len:
                            editdist_arr.append([i+1, 1])
        return self.output_editdist(editdist_arr)

    #A function that iterates through the output array, then writes each line
    #into a file named output_hammingdist.txt
    def output_editdist(self, arr):
        f = open("output_editdist.txt", "w")
        n = len(arr)

        for i in range(n):
            if i!=n-1:
                line = str(arr[i][0])+" "+str(arr[i][1])+"\n"
            else:
                line = str(arr[i][0])+" "+str(arr[i][1])
            f.write(line)
        f.close()

if __name__ == "__main__":
    txtInp = open(sys.argv[1], "r")
    patInp = open(sys.argv[2], "r")
    txt = txtInp.read()
    pat = patInp.read()
    Z_Algo = ZBox(txt, pat)
