
# coding: utf-8

## Topic Modelling using LDA

# Given a text corpus, LDA (Latent Dirichlet Allocation) modelling divides the texts into groups of different topics based on number of topics specified. It is unsupervised algorithm. It is based on a bag of words model.

### Gensim

# Gensim (https://radimrehurek.com/gensim/) is a Python library which is used for topic modelling. It supports various algorithms for topic modelling. It is available under GNU license. It is easy to install and use.

# In[ ]:

from gensim import corpora, models, similarities


# Created a class LdaModelling for Topic modelling. It takes 2 input parameters num and text. 'num' represents number of topics to group 'text' fom corpus. 
# 
# 
# The function getGroupedData finds the group for the associated tweets. It finds which tweet belongs to which group. It returns the associated list of bags. 
# 
# All the stop words are ignored while modeling the topic. The text is converted to lower case. A dictionary is created which specifies the frequency of the occurence of the word in corpus. The words occuring once are ignored. 
# A bag of words corpus is created from the text. A lda model is created from text corpus, dictionary and number of topics.  
# A list named "groups" appends the corresponding tweet to the group to which it belongs to and is returned. 

# In[ ]:

from collections import defaultdict
import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class LdaModelling:


    def __init__(self, num, text):
        self.num_topics = num
        self.documents = text


    def getGroupedData(self):
        #ignore stop-words
        stoplist = set(line.strip() for line in open('stop-word-list.txt'))

        #lowercase
        texts = [[word for word in document.lower().split() if word not in stoplist]
                for document in self.documents]

        # count frequency
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        #use only words that appear more than once
        texts = [[token for token in text if frequency[token] > 1]
               for text in texts]

        #creating bag of wrods model
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]

        #creating a lda model
        lda_model = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=self.num_topics)
        corpus_lda = lda_model[corpus]


        groups = []
        for i in range(self.num_topics):
            groups.append([])


        #finding the associated gropu for each tweet in text and appending to corresponding group
        i=0
        for doc in corpus_lda: 
            a = list(sorted(doc, key=lambda x: x[1]))
            #print self.documents[i] , (a[-1][0])
            groups[a[-1][0]].append(self.documents[i])
            i = i + 1

        return groups

