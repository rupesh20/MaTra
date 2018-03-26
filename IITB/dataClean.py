import sys
import os
import nltk 
def DictLook(New):
    NewList 
    jobj=json.load(open('words_dictionary.json'))
    for w in New:
        if jobj[w] is 1 or :

class textClean(object):
    """docstring for Cleaning"""

    def __init__(self, arg):
        super(Cleaning, self).__init__()
        self.arg = arg
        
    def substr(l, m,i,j):
        while i <len(m):
            if m[i] == l[j]:
                if i >= len(m):
                    break
                if j>= len(l):
                    break
                i+=1
                j+=1
                if j == len(l)-1:
                    return True
            else: 
                i+=1
                j=0
        return False 

    def url(w,index):
        for i in words:
            s ='http'
            if substr(s,i,0,0) is True:
                    words[index] = ' '
            index+=1 
        
    def lowercase(lt,j,lt1):
        for var in lt:
            j=0
            s = ''
            temp=0
            while j < len(var):
                temp = ord(var[j])
                if temp >=65 and temp <=90:
                    temp += 32
                    s += str(unichr(temp))
                else:
                    s += str(unichr(temp))    
                #print var[j]
                j+=1
            lt1.append(s)        
            

    def substr_new(l,m,i,j,arr):
        count =0
        print l
        while i <len(m):
            if m[i] == l[j]:
                count+=1
                if count is 2:    
                    arr.append(i-1)
                    j=0
                    count=0
                i+=1        
            else: 
                i+=1
                j=0

        return m


    def unwanted(words):    
        for var in words:
            j=0
            while j < len(var):
                temp = ord(var[j])
                if (var>=32 and var<=64)  or (var>=91 and var <=96) or (var>=123 and var<=127):
                    var[j] = '$'
                j+=1 
    
    def splitWords(text):
        words = []
        for line in text:
            j=0
            s=''
            while j<len(line):
                if line[j] is not ' ':
                    s+=line[j]
                else:  
                    words.append(s)
                    s=''
                j+=1
            print(words)                        

class StupidBackoff(object):
               
               def __init__(self, arg):
                   super(StupidBackoff, self).__init__()
                   self.arg = arg
                              
