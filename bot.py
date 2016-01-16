
# coding: utf-8

## Bot

# This module gets the top 10 trending topics from Twitter of the specified loaction (United States). 
# Since we are restricted with requests from Twitter REST API, we gather only 500 tweets per 6 minutes for each trending topic. As the summaries for each topic is generated the bot writes the summary as tweet on http://twitter.com/condensely

# In[ ]:

from tweepy import OAuthHandler
from tweepy import API
import sched, time
import logging

import summarization as summary

logging.captureWarnings(True)


# authentication to Twitter REST API
def getAuth():
    consumer_key = '9jYyfXOK1Ppdr9tNHLY93Jnlf'
    consumer_secret = '9EXll74vpVIQy2WkeuuKB653P6ZylKZe2dDEBTkZZ1HUT7sdyw'
    oauth_token = '3178479342-BUBVOkOgx2lld4fJLLQYpMFdil5lm1PJePuytFV'
    oauth_token_secret = 'eq4QbbITTBJpNckhzOqL2GNgVJBai7xT1RCmaabYHs9xL'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(oauth_token, oauth_token_secret)

    return API(auth)

# India location=23424848
# US location=23424977

#return top trends
def getTrends(api, location=23424977):
    api = getAuth()
    result = api.trends_place(location)

    return result[0].get('trends')

def generateTweets(scheduler, api):
    trends = getTrends(api)
    info = api.me()
    count = info.statuses_count + 1
    
    for trend in trends:
        term =  trend.get('name')
        summary_num = 0

         #find summaries for each trend
        summarize_obj = summary.Summarization(term, 2)
        ret_summary = summarize_obj.FindSummary()

        #tweet the trend topic on twitter
        try:
            api.update_status('The summaries for the trend ' + str(count) + ' "' + term + '" as of ' + time.strftime("%Y-%m-%d %H:%M"))
        except:
            print "Error updating information for Trend: " + term

        for statement in ret_summary:
            if summary_num == 0:
                char = 'a'
            else:
                char = 'b'
                
            #tweet each summary on twitter
            try:
                api.update_status(str(count) + char + ": " + statement)
            except:
                print "Error in Tweet: " + statement

            summary_num += 1

        count += 1
        time.sleep(360) # delay in seconds for the next trend

    scheduler.enter(1, 1, generateTweets, (scheduler, api,))
    scheduler.run()
    
#to run every hour    
s = sched.scheduler(time.time, time.sleep)
api = getAuth()
generateTweets(s, api)

