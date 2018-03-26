import nltk
from nltk.collocations import *
 	

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = BigramCollocationFinder.from_words(
nltk.corpus.genesis.words('/home/rupesh20/ProjectFinal/IITB/NEw.txt'))
print finder.score_ngrams()