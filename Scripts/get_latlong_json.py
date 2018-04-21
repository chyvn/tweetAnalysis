from pymongo import MongoClient
import pandas as pd

client = MongoClient()
db = client.twitterCleanDb
tweetCollection = db.tweetsClenaned

hashtags = []
retweets = []
followers = []
name = []
statusesCount = []
text = []
polarity = []
lat = []
longi = []
uid = []
createdat = []

hashTagCollection = tweetCollection.find({'entities.hashtags.text': {'$ne': None}})

for tweet in hashTagCollection:
    if len(tweet['entities']['hashtags']) > 0 and 'long' in tweet :
        hashtags.append(tweet['entities']['hashtags'][0]['text'])
        retweets.append(tweet['retweet_count'])
        followers.append(tweet['user']['followers_count'])
        lat.append(tweet['lat'])
        longi.append(tweet['long'])
        statusesCount.append(tweet['user']['statuses_count'])
        text.append(tweet['text'])
        polarity.append(tweet['polarity'])
        name.append(tweet['user']['name'])
        uid.append(tweet['id_str'])
        createdat.append(tweet['created_at'])

print (len(uid), len(name), len(polarity), len(text), len(statusesCount), len(followers), len(retweets), len(hashtags))

df = pd.DataFrame({'svgPath': 'targetSVG', 'zoomLevel': '5', 'scale': '0.5', 'title': name, 'latitude': lat, 'longitude': longi})
df.to_json('output.json', orient = 'records')


