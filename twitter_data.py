
# coding: utf-8

## Twitter Data

# To collect the tweets for the specified term. The connection to Twitter REST API is established and the tweets are gathered. The tweets are processed. The tweets are processed and the irrelevant tweets are removed. The url's in tweets are removed. 
# Further, multi-line tweet is converted to a single line. All the non releavant characters are removed. All re-tweets are ignored. 
# The tweets which are from same user is ignored. Moreover, if the tweet is a reply tweet is also not taken into consideration. The tweets which contain keyowrd trend\* is also ignored. As these are tweets which tell about trending topics.

# In[ ]:

from __future__ import division
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import math
import re
import sys


class TwitterData():

    def __init__(self, search, limit):
        self.search_term = search;
        self.search_limit = limit

        # Twitter Authentication
        self.consumer_key = '9jYyfXOK1Ppdr9tNHLY93Jnlf'
        self.consumer_secret = '9EXll74vpVIQy2WkeuuKB653P6ZylKZe2dDEBTkZZ1HUT7sdyw'
        self.oauth_token = '3178479342-BUBVOkOgx2lld4fJLLQYpMFdil5lm1PJePuytFV'
        self.oauth_token_secret = 'eq4QbbITTBJpNckhzOqL2GNgVJBai7xT1RCmaabYHs9xL'

        # File, to store twitter data
        self.data_file = "data/" + self.search_term + ".txt"


    def writeToFile(self, tweet_collection):

        documents = []
        out_file = open(self.data_file, 'w')
        for tweet in tweet_collection:
            out_file.write(tweet+ '\n')
            documents.append(tweet)

        out_file.close()

        return documents


    def getData(self):

        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.oauth_token, self.oauth_token_secret)

        api = API(auth)

        tweet_collection = []

        used_ids = {}

        for tweet in Cursor(api.search, q=str(self.search_term), lang='en').items(self.search_limit):
            text = tweet.text.encode('utf-8')
            reply_to_status = tweet.in_reply_to_status_id
            reply_to_user = tweet.in_reply_to_screen_name
            user_id = tweet.user.screen_name

            #Future features to incorporate - retweet, followers, favorite
            retweet_count = tweet.retweet_count

            #Text preprocessing - remove links from the text if any and remove special characters
            text = re.sub(r"(?:\@|https?\://)\S+", "", text)

            # remove new lines
            text = text.replace('\n','')

            #removes all other invalid characters
            text = re.sub(r'[^a-zA-Z0-9 "#:!-.,&\']','', text)

            #RT remmoved
            text = text.replace('RT ','')

            #ignore trend tweets
            if 'trend' in str.lower(text):
                continue

            #Filter Criteria - Remove tweets from same user, remove replies to tweets or users
            if reply_to_user is None and reply_to_status is None and user_id not in used_ids :
                used_ids[user_id] = True
                tweet_collection.append(text)

        return self.writeToFile(tweet_collection)

