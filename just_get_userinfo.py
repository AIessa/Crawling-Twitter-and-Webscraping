#JUST GET SPECIFIED USER TIMELINES

#imports-----------------------------------------
import pickle
import tweepy
import csv


#list of profiles to crawl-----------------
path = 'file.pickle' #this was a pickle file, make sure to import different files correctly!
with open(path,'rb') as fin:
        userid_list = pickle.load(fin)


#authorize twitter, initialize tweepy------------
#fill in consumer key, secret and access token, secret. You can get these after creating a Twitter dev account & making an app on there. These tokens will then be generated. You should keep them secret, if you want to be the only one to have access to your account & app!
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True) #if you download large amounts of data, Twitter will limit this. It is good to set 'wait on rate limit' to True to avoid problems
print("oauth done, got api")


#crawl & save items-------------------------------

for userid in userid_list:
	print("user: "+str(userid))

	try: #Here I use 'try', because some profiles might not exist or be private/suspended/blocked, which will throw an error and terminate the function.
		print("finding user profile")
		user = api.get_user(userid)
		userinfo =[user.id,user.screen_name,user.location,user.url,user.description,user.followers_count,user.statuses_count,user.verified,user.lang,user.profile_image_url] #'user' is formatted like a json file, so if you only want specific information from the profiles, you need to specify!
		with open('userprofiles.csv', 'a') as f:
			writer = csv.writer(f)
			writer.writerow(userinfo)
	except tweepy.TweepError:
		print('error') #if you want to know the exact error, you can print it and look up what the error code means!

print(done)






