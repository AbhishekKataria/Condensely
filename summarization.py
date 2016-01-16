
# coding: utf-8

## Summarization

# This module takes in a term as a argument and number of topics as input. It gathers data for the specific term from twitter_data. It then performs topic modelling (using LDA) and groupts tweets into different groups. The summary is generated for each topic.  

# In[ ]:

import twitter_data as td
import summary_generation as sg
import lda_modelling as lda
import sys


class Summarization:
    def __init__(self, term, num):
        self.summarize_term = term
        self.num_topics = num

    def FindSummary(self):
        
        # gather data from twitter for the term and 2nd argument is number of tweets to be collected. The tweets are processed.
        obj = td.TwitterData(self.summarize_term, 500)

        documents = obj.getData()

        num_topics = int(self.num_topics)

        # perform LDA topic modelling on processed tweets
        lda_obj = lda.LdaModelling(num_topics, documents)

        # find the tweets which belongs to each group
        groups = lda_obj.getGroupedData()

        summaries = []
        
        # generate summary from each group
        for i in range(num_topics):
            generate = sg.summaryGen(groups[i])
            a = generate.generation()
            summaries.append(a)

        return summaries

