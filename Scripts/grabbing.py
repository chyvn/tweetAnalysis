import tweepy
import time
from tweepy import OAuthHandler

customer_key = "QneeoaNyVpnR0TTbPZbVZrQAD"
customer_secret = "QObDAXLP8uIhmhTvcb2lmQDj15RrS1JDcjZR65LX08oL0OEmdU"
access_token = "985031295666356224-Qkpu2qcApK1d9H5jj6sHe51zAj7h1wv"
access_secret = "48jrWQJvCICEesw8c93LqmUNCNtMoRliiBpJB5BCj1SHO"

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
