#Finding trigrams for entire corpus with NLTK
#kathiasi 1.3.2022
import os
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import nltk
import re
from nltk.corpus.reader import PlaintextCorpusReader
from nltk.probability import FreqDist

corpus_root = "/home/hiovain/Desktop/code_test/to_voices"
texts = PlaintextCorpusReader(corpus_root, '.*\.txt')

# make a tokenized corpus?

fdist = nltk.FreqDist()
tokens = texts.words() 

for token in tokens:

    pattern = re.compile("^[a-zA-Z]+$")
    pattern.match(token)
    # for value in dict.items(): ??? 
    fdist.update(nltk.trigrams(token))
    

for trigram in fdist:
    print(f"{trigram}\t{fdist[trigram]}") 
    # one line only
    if True:
        input()
    continue
    