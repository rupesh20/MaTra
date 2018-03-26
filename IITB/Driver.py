#import dataClean
import	spacy 
import json
import nltk
import re 
import urllib2
from nltk.text import Text
from nltk import sent_tokenize
from nltk import ngrams
from pprint import pprint

#CorpusSize  = 0 
TransHindi = []
Subj =[]
verb = []
obj = []
sentences =[]
Gram = []
Gram5 = []

CountGram1 = {}
CountGram2 = {}
CountGram3 = {}
CountGram4 = {}
CountGram5 = {}

s1 = "{}"
s2 = "{} {}"
s3 = "{} {} {}"
s4 = "{} {} {} {}"
s5 = "{} {} {} {} {}"

def unwanted(words):
    index=0
    for var in words:
        j=0
        s = '' 
        while j < len(var):
            temp = ord(var[j])
            if (temp is  46)  or (temp>=65 and temp <=90) or (temp>=97 and temp<=122):
                s += str(unichr(temp))
            j+=1

        if s is not '':    
        	words[index]=s
        else:
        	words[index]=''	
        index+=1
    return words    
        
def lowercase(lt,j,lt1):
    for var in lt:
        j=0
        counter=0
        s = ''
        temp=0
        while j < len(var):
            temp = ord(var[j])
            if temp>127:
                counter=1
                break
            elif temp >=65 and temp <=90:
                temp += 32
                s += str(unichr(temp))
            else:
                s += str(unichr(temp))    
            #print var[j]
            j+=1
        if counter is 1 :
            a=unicode(var,errors='ignore')
            a=a.encode('ascii','ignore')
            lt1.append(a)
        else:    
            lt1.append(s)        
    return lt1  

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
    for i in w:
        s ='http'
        if substr(s,i,0,0) is True:
            w[index] = ' '
        index+=1 
    return w         

def Writer(NewList,obj):
	for w in NewList:
		obj.write(w)
		obj.write(" ")

def Ngram(sentences,n,Csize):
    CorpusSize  = 0 
    sixgrams = ngrams(sentences.split(),n)
    for grams in sixgrams:
        if n is 1:
            CorpusSize +=1    
        Gram.append(grams)
    Csize+=CorpusSize 
    return Csize    

def DictLook(New):
	NewList = [ ]
	jobj=json.load(open('words_dictionary.json'))
	for w in New:
		if len(w) > 0:
			try:	
				if w[len(w)-1] is '.':
					if jobj[w[:len(w)-2]] is 1:
						NewList.append(w)
				elif jobj[w] is 1: 
					   NewList.append(w)	
			except Exception as e:
				continue		
	return NewList

def unpack(tup,len):
    s = ''
    if len is 1:
        s=s1.format(*tup)
    elif len is 2:
        s=s2.format(*tup)
    elif len is 3:
        s=s3.format(*tup)
    elif len is 4:
        s=s4.format(*tup)
    else:
        s=s5.format(*tup)   
    return s 
       
def FreqCount(words):
    text = Text(words)
    freq = nltk.FreqDist(text)
    Score = list(nltk.FreqDist.keys(freq)) 
    for i in Score:
        if len(i) is 1:
            CountGram1[unpack(i,len(i))] = freq[i]
        elif len(i) is 2:        
            CountGram2[unpack(i,len(i))] = freq[i]
        elif len(i) is 3:
            CountGram3[unpack(i,len(i))] = freq[i]
        elif len(i) is 4:
            CountGram4[unpack(i,len(i))] = freq[i] 
        else:
            CountGram5[unpack(i,len(i))] = freq[i]      
        #print unpack(i,len(i))

def Sliced(Str):
    l=len(Str) - 1
    while Str[l] is not ' ':
        l-=1
        if l < 0:
            return -1
    return Str[:l]     

def StupidBackoff(MainStr,SliceStr,x):
    words = MainStr.split()
    if len(words) is 5:
        try:
            if CountGram5[MainStr] > 0:
                return float(CountGram5[MainStr])/CountGram4[SliceStr]
        except Exception as e:
                #print Sliced(SliceStr)
                score = (0.4)*StupidBackoff(SliceStr,Sliced(SliceStr),x)
                #print score
                return score    
    elif len(words) is 4:
        try:
            if CountGram4[MainStr] > 0:
                return float(CountGram4[MainStr])/CountGram3[SliceStr]
        except Exception as e:
                #print Sliced(SliceStr)
                score = (0.4)*StupidBackoff(SliceStr,Sliced(SliceStr),x)
                #print score       
                return score    
    elif len(words) is 3:
        try:
            if CountGram3[MainStr] > 0:
                return float(CountGram3[MainStr])/CountGram2[SliceStr]             
        except Exception as e:
                #print Sliced(SliceStr)
                score = (0.4)*StupidBackoff(SliceStr,Sliced(SliceStr),x)
                #print score     
                return score    
    elif len(words) is 2:
        try:
            if CountGram2[MainStr] > 0:
                return float(CountGram2[MainStr])/CountGram1[SliceStr]
        except Exception as e:        
                score =  (0.4)*StupidBackoff(SliceStr,Sliced(SliceStr),x)
                #print score
                return score    
    elif len(words) is 1: 
        try:
            if CountGram1[MainStr] > 0:
                return float(CountGram1[MainStr])/x
        except Exception as e:
               return 0   

def TestNgram(sentences,n):
    sixgrams = ngrams(sentences.split(),n)
    for grams in sixgrams:    
        Gram5.append(grams)

def CalcScore(y,z):
    for i in Gram5:
        s=unpack(i,len(i))
        z.write(s)
        z.write("     :   ")
	Score = StupidBackoff(s,Sliced(s),y)
        z.write(str(Score))
        z.write('\n')

def processContent(strArray):
    try:
	#index=0
	#count=0
        for item in strArray:		
            tokenized = nltk.word_tokenize(item)	
            tagged = nltk.pos_tag(tokenized)
	    count  =0
	    index =0	
	    for tag in tagged:	
            	if 'VB' in tagged[index][1][:2] : 
			verb.append(tagged[index][0])
			count = 1
            	elif count is 0:
			Subj.append(tagged[index][0])
		elif count is 1:
			obj.append(tagged[index][0])
	    	index+=1				
    except Exception as e:
        print(str(e))

def BilingDict(txt,ID):
	try:
		url = 'https://glosbe.com/gapi/translate?from=eng&dest=hin&format=json&phrase={}&pretty=true'.format(ID)
		response = urllib2.urlopen(url)
		data = json.loads(response.read())
		x=data['tuc'][0]['phrase']['text']
		x=x.encode("utf-8")
		#x_translate = json.dumps(x,ensure_ascii=False)
		txt.write(x)
		txt.write(" ")
		#TransHindi.append(x_translate)
	except Exception as e:
		print(str(e))
def main():
	""" 
		These files used for testing and conversion
	"""
	fl = '/home/rupesh20/ProjectFinal/IITB/conv.txt'
	Pconv = '/home/rupesh20/ProjectFinal/IITB/prevconv.txt'
        filename = '/home/rupesh20/ProjectFinal/IITB/NEw.txt'
        outfile = '/home/rupesh20/ProjectFinal/IITB/Demo.txt'
        outputfile ='/home/rupesh20/ProjectFinal/IITB/Test.txt'

	""" 
		Other comments are for debugging.
	"""
        #filename = '/home/rupesh20/ProjectFinal/final/en_US/en_US.blogs.txt'
        #newfilename = '/home/rupesh20/ProjectFinal/IITB/NEw.txt'
        #file = open(filename,'r')
        #newfile = open(newfilename,'w')

        #text = file.read()
        #file.close()
        #words = text.split()
	
        #new = []
        #new=lowercase(words,0,new)
        #new=url(new,0)
        #new=unwanted(new)
        #new=DictLook(new)
		
	with open(Pconv) as f:
    		lines = f.readlines()
	""" 
		lines : contains list of strings in english for conversion 
	"""
        #Writer(new,newfile)
        #newfile.close()

	""" 
		Objects for files are opened
	"""
	txt = open(fl,'w')
        Tobj1=open(outputfile,'w')
        #Ttext1=Tobj1.read()
        #Tobj1.close()1
        Nobj=open(filename,'r')
        Ntext=Nobj.read()
        Nobj.close()
        Nobj1=open(outfile,'r')
        Ntext1=Nobj1.read()
        Nobj1.close()
	""" 
		Sentences are Tokenized 
	"""
        sentences=sent_tokenize(Ntext)
        testSentences=sent_tokenize(Ntext1)
         
        Csize=0
	""" 
		After Tokenize the text in sentences 
		We have calculated the Ngram 
		1,2 3,4,5 grams
		Gram1 list contains uni-gram
		||ly Gram2,3,4,5 contains further grams
		
	"""
        for sent in sentences:
            for j in xrange(1,6):
                Csize= Ngram(sent,j,Csize)
        print Csize        
        FreqCount(Gram)
        for sent in testSentences:
            TestNgram(sent,5)
        #print Gram5
        #print Sliced(x)
        
	"""" 
		CalcScore : function to ecaluate the score using the 
			    stupid backoff algo
		output file :  generated after the calcscore module , sent : Score
			
	"""
	CalcScore(Csize,Tobj1)

	""" 
		Processcontent : module is for Alignment, S-O-V 
				determization.
	
	"""

	""" 
		below code translate, del list[:]( delete whole list )
	
	"""
	for line in lines:
		temp = []
		temp.append(line)	
		processContent(temp)
		for i in Subj:
			BilingDict(txt,i)
		for i in obj:
			BilingDict(txt,i)
		for i in verb:
			BilingDict(txt,i)	
		del Subj[:]
		del verb[:]
		del obj[:]
		
		txt.write('\n')

	#print Subj[0] 
	#print verb
	#print obj
	""" 
		Bilingdict : module contain JSON lookup table.
				genrates a file with HINDI text.

	"""
			    
	#print StupidBackoff(x,Sliced(x),Csize)
        #print CountGram1
        #print CountGram2
        #print CountGram3
        #print CountGram4
        #freq.plot(50)

if __name__ == '__main__':
	main()
