import tweepy
import time
from tweepy import OAuthHandler

customer_key = "***"
customer_secret = "***"
access_token = "***"
access_secret = "***"

auth = OAuthHandler(customer_key, customer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
from pymongo import MongoClient
client = MongoClient()
db = client.twitterDb
posts = db.tenKtweets
for i in range(0, 2000):
    time.sleep(5)
    tweets = api.search(q = "a", count = 5)
    j = 0
    for tweet in tweets:
        posts.insert_one(tweet._json)
        print('inserted:', i, j)
        j += 1
