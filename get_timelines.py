"""
adapted from @author: Abeer

Some resources:
count status for user_ time line limited to 200 to extend it check the below url :
https://stackoverflow.com/questions/46734636/tweepy-api-user-timeline-count-limited-to-200

to get the full url 
https://stackoverflow.com/questions/17910493/complete-urls-in-tweepy-when-expanded-url-is-not-enough-integration-with-urllib

working with url : https://stackoverflow.com/questions/17910493/complete-urls-in-tweepy-when-expanded-url-is-not-enough-integration-with-urllib

status full discription : https://developer.twitter.com/en/docs/basics/twitter-ids.html

"""

#imports
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.api import API
import tweepy #https://github.com/tweepy/tweepy

import csv
import pickle
import pandas as pd

import math
import re
import sys
from time import sleep
from os import path
import logging



#import download_tweets as tweetd
__docformat__ = 'restructedtext en'
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


#authorize twitter, initialize tweepy
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
print("oauth done, got api")



def record_ID_as_done(id_tw):
    content=open('testing_done_ids_top5000.txt','a')
    content.write(str(id_tw)+'\n')
    
def get_all_tweets(userid):
    
    print("user: "+str(userid))

	#initialize a list to hold all the Tweets
    alltweets = []

    #Twitter only allows access to a users most recent 3240 tweets with this method
	#make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        new_tweets = api.user_timeline(user_id = userid,count=200, tweet_mode="extended", url= 'expanded_url')
	
    	#save most recent tweets
        alltweets.extend(new_tweets)
        print("After initial request, got "+str(len(new_tweets))+" recent tweets from timeline.")

    	#save the id of the oldest tweet less one
        if len(alltweets)==0:
            oldest = 0
            print("Collected no tweets from profile") #This means while loop will be interrupted right away
        else:
            oldest = alltweets[-1].id - 1

    	#keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            try:
                print ("getting tweets before %s" % (oldest))
        		
        		#all subsiquent requests use the max_id param to prevent duplicate
                new_tweets = api.user_timeline(user_id = userid,count=200,max_id=oldest, tweet_mode="extended")
        		
        		#save most recent tweets
                alltweets.extend(new_tweets)
        		
        		#update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1
                print ("...%s tweets downloaded so far" % (len(alltweets)))
        	
        	#transform the tweepy tweets into a 3D array that will populate the csv	
                outtweets = [[tweet.id_str, tweet.created_at, tweet.full_text.encode("utf-8"), tweet.entities['urls']] for tweet in alltweets]

        	#write the csv	
            #each user gets a separate file in a 'timelines' directory, each containing the tweets from the user's timeline
                with open('timelines/%s_tweets.csv' % str(userid), 'w') as f:
                    writer = csv.writer(f)
                    writer.writerow(["userid","tweet_id","created_at","text","URLs"]) #title row
                    writer.writerows(outtweets)
            
            except tweepy.TweepError:
                print("tweepy error, sleeping for 3")
                sleep(3)
                continue
            except StopIteration:
                print("stopping iteration")
                break
            
    except tweepy.TweepError:
        print("tweepy error, sleeping for 3")
        sleep(3)

	
pass   


def pass_screen_name():
    print('passing screen_name')
    
    path_userids = 'twitter_user_ids.pickle' #put the path to the file with the user-ids from which you want to collect the timelines
    with open(path_userids,'rb') as fin:
        tweet_IDs = pickle.load(fin)
    tweet_IDs = pd.DataFrame(tweet_IDs)

    #run batches based on the instance of app that you are running (you can separate the run on to multible instances):    
    #get starting location:
    path_done_log = 'done_log.txt'
    with open(path_done_log,'r')as fin:
        lines = fin.readlines()
        fin.close()
    startid_index = len(lines) #basically index of last done id + 1
    print("Starting with user ID at index: "+str(startid_index))
    
    #tweet_IDs=tweet_IDs.iloc[startid_index:startid_index+5000] #we want to go through next 5000 before interrupting
    tweet_IDs = tweet_IDs.iloc[startid_index:]

    IDs=[x[0] for x in tweet_IDs.values.tolist()]
    
    #you should have the api from authorizing at the beginning. 
    """
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''   
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    """
    
    #start looping
    limit = len(IDs)
    
    i = math.ceil(limit/100)
    start = 0
    end = 100
        
    for go in range(i):
        print('currently getting {} - {}'.format(start, end))
        sleep(7)  # needed to prevent hitting API rate limit
        id_batch = IDs[start:end]
        start += 100
        end += 100
        #status = api.statuses_lookup(id_batch)
        #tweet_txt = []
        for i in id_batch:
            print("AT USER: "+str(i))
            get_all_tweets(i)
            record_ID_as_done(i)
            print("recorded %s as done" % i)
            


if __name__ == '__main__':
    print('inmain')
    pass_screen_name()
    
    
