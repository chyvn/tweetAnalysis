import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pymongo import MongoClient
from geopy.geocoders import Nominatim

locate = Nominatim()
client = MongoClient()
db = client.twitterCleanDb
tweetCollection = db.tweets

times = []
polarities = []
subjectivities = []
locations = []
locationPolarities = []
lats = []
longs = []
modiTweets = tweetCollection.find({'cleantest' :{'$regex': '.*a*.'}})
for tweet in modiTweets:
    times.append(tweet['created_at'])
    polarities.append(tweet['polarity'])
    subjectivities.append(tweet['subjectivity'])
    
    latlong = locate.geocode(tweet['user']['location'])
    if latlong is None:
        latlong = locate.geocode(tweet['user']['time_zone'])
        if latlong is None:
            print('appended')
        else:
            locations.append([latlong.latitude, latlong.longitude])
            print('appended 1', latlong, latlong.latitude, latlong.longitude)
            locationPolarities.append(tweet['polarity'])
    else:
        locations.append([latlong.latitude, latlong.longitude])
        print('appended 2', latlong, latlong.latitude, latlong.longitude)
        locationPolarities.append(tweet['polarity'])

import dateutil
df = pd.DataFrame({'time':times, 'polarity': polarities, 'subjectivity': subjectivities})
df = df.sort_values(by=['time'])
df['time'] = df['time'].apply(dateutil.parser.parse)
df.dtypes

plt.figure(figsize = (12, 5))

plt.title('Sentiment Comparision')
plt.plot(df['time'], df['polarity'])
plt.plot(df['time'], df['subjectivity'])

plt.xlabel('Time')
plt.ylabel('Sentiment Value')

lats = [lat[0] for lat in locations]
longi = [long[1] for long in locations]

print(lats, " +  ", longi)

lats = list(filter(lambda a: a != 'p', lats))

import mplleaflet

mapdf = pd.DataFrame({'lat': lats, 'longi': longi, 'polarity':polarities[:len(lats)]})
plt.figure(figsize=(8, 8))
plt.scatter(longi, lats, c = polarities[:len(lats)])
mplleaflet.display()
