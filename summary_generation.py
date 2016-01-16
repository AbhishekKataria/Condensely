
# coding: utf-8

## Summary Generation

# Given a group of text, finding a sentence that best represents the group of texts. 
# 
# A class summaryGen is created which takes input as a set of tweets. 
# 
# The generation() function is used which uses Information Retrieval technique. It computes the term frequency and inverse document frequency of each word. Each word is ranked by multiplying its term frequency and inverse document frequency. In a given sentence, the rank of all words is summed and normalized. The sentence with maximum rank is considered as summary.

# In[ ]:

from __future__ import division
import math

class summaryGen:

    def __init__(self, documents):
        self.documents = documents

        #ignoring stop words
        stop_word_file = "stop-word-list.txt"
        with open(stop_word_file) as f :
            self.stop_words = set(line.strip() for line in f)

        #total number of tweets
        self.numofSentences = self.count();
        
        #list of words in corpus
        self.listofallwords = self.findwords();
        
        #list of unique words present in corpus
        self.listofUniqueWords = self.listofallwords.keys()
        
        #To find toal number words
        self.totalcount = self.tofindtotalwords(self.listofallwords);
        
        self.wordweight_dict = dict()


    def isStopWord(self, w) :
        if w.lower() in self.stop_words:
            return True
        else:
            return False

    #total number of documents
    def count(self):
        count = 0
        count = len(self.documents)
        return count;

    
    #word frequency of each word
    def findwords(self):
        word_dict = dict()
        for line in self.documents:
            w = line.split()
            for words in w:
                if words not in word_dict:
                    word_dict[words] = 1
                else:
                    word_dict[words] = word_dict[words] + 1
        return word_dict

    def CountWordOccurences(self, word):
        return self.listofallwords[word]

    
    def tofindtotalwords(self, listwords):
        total = 0
        for words in listwords:
            total += listwords[words];
        return total

    #count number of sentenes in which the the word occurs
    def countSentenceOccurences(self, word):
        count = 1
        for line in self.documents:
            sen_words = line.split();
            if word in sen_words:
                count += 1;
        return count

    #assign weight to the word
    def assignWeighttoWord(self, word, wordWeight):
        self.wordweight_dict[word] = wordWeight 


    #average length of all sentences
    def average_len(self):
        total = 0;
        for sentence in self.documents:
            words = sentence.split();
            total += len(words)
        return total / len(self.documents)


    #to rank each sentence
    def generation(self):
        toptf = dict()
        #computing rank for each word
        for word in self.listofUniqueWords:
            termFrequency = self.CountWordOccurences(word) / self.totalcount;
            inverseDocFrequency = self.numofSentences / self.countSentenceOccurences(word);
            wordWeight = termFrequency *  math.log(inverseDocFrequency,2);
            toptf[word] = wordWeight
            self.assignWeighttoWord(word, wordWeight);

        sentenceweight = 0
        maxsentenceweight = -1
        threshold = self.average_len()
        summarysentence = ""

        for sentence in self.documents:
            sentenceweight = 0
            words = sentence.split();
            for word in words:
                if( self.isStopWord(word) != True):
                    sentenceweight += self.wordweight_dict.get(word, 0);
            #normalizing the sentence weight
            sentenceweight = sentenceweight / max( len(words), threshold );
    
            #summary sentence is the maximum ranked sentence
            if(sentenceweight > maxsentenceweight):
                maxsentenceweight = sentenceweight;
                summarysentence = sentence;

        #returns the summary sentence
        return summarysentence

