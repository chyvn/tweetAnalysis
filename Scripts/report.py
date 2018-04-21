Cleaning the data:

Once we are done with collecting the tweets, we ne+ed to clean the data. As the tweets contain all kinds of languages, expressions and slangs but the NLP library we are using to analyse the sentiments of the users is limited in capabilities, this is a necessary step.

Let us retrieve the data from raw collection of 10 K tweets. 

from pymongo import MongoClient
from bson.json_util import dumps
client = MongoClient()
db = client.twitterDb
modiPosts = db.zurkerbergposts
texts = []
postsJson = []
for post in modiPosts.find():
    texts.append(post['text'])
    print (post['text'])


Let us convert the text to lower case, as most of the libraries and collections of words that we will be using are in lower case. It will be an efficient decision for further comparisions. 

texts = [text.lower() for text in texts]


Considering the types of special characters and how they mean nothing to the target libraries we can remove these too. We also make sure only characters that are understandable are present.

texts = [re.sub('\W+', ' ', text) for text in texts]
texts = [re.sub('[^a-z0-9\s]', '', text) for text in texts]

To remove any words that don't make sense we use a collection of all English words and remove the letters not occuring in this collection. 

englishWords = open('eng_words.txt', 'rt').read()
englishWords.replace('rt', '')

cleanTexts = []
for text in texts:
    words = re.split(r'\W+', text)
    words = [word for word in words if word in englishWords]
    words = [word for word in words if word not in ['rt', 'co', 't', 'c']]
    text = ' '.join(words)
    #print(len(text))
    cleanTexts.append(text)


Once the same is done, the data is clean and it can be analyzed for sentiment. This is done by importing sentiment from TextBlob. 

from textblob import TextBlob
for text in cleanTexts:
    sentiment = TextBlob(text).sentiment
    #print (len(text), text, sentiment)
len(cleanTexts)

This data is then appended to the corresponding clean tweets. We will create a new database with clean values. from bson.json_util import loads
from bson.json_util import dumps

results = modiPosts.find()
results = list(results)
i = 0;

for i in range(0, len(cleanTexts)):
    if len(cleanTexts[i]) > 0 :
        sentiment = TextBlob(cleanTexts[i]).sentiment
        if sentiment.subjectivity > 0.2:
            result = results[i]
            jsonObj = loads(dumps(result))
            jsonObj['polarity'] = sentiment.polarity
            jsonObj['subjectivity'] = sentiment.subjectivity
            jsonObj['cleantest'] = cleanTexts[i]
            #print(jsonObj, '\n\n', cleanTexts[i], '\n\n\n')
            collection.insert_one(jsonObj)

    
Analysis and representation of results:


As we have already calculated sentiments of each of the tweets, we can now head to representing the analysis and visualizing the results.

Tweet Cloud:

To represent the tweet despersion globally over a map, we will be using the library mplleaflet. The library takes inputs in the form of coordinates over the map, renders the map from google maps. The points are then plotted as matplotlib figures. 

Inordre to achieve this we can get coordinates, but sadly not every tweet comes with coordinates. However, a few users supply their location information along with tweets. This information can be used to plot tweets. Finding such tweets, making sense of the coordinates we can use geopy. 

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pymongo import MongoClient
from geopy.geocoders import Nominatim

locate = Nominatim()
client = MongoClient()
db = client.twitterCleanDb
tweetCollection = db.tenKtweetsCleaned

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
    
    latlong = locate.geocode(tweet['user']['location'], timeout = 10)
    if latlong is None:
        latlong = locate.geocode(tweet['user']['time_zone'], timeout = 10)
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
    

In the code above, we also append the sentiment values to each of the queried tweets. This makes a pretty good dataframes to analyse further. 

Now let us examine the sentiment value variations with respect to time. 
import dateutil
df = pd.DataFrame({'time':times, 'polarity': polarities, 'subjectivity': subjectivities})
df = df.sort_values(by=['time'])
df['time'] = df['time'].apply(dateutil.parser.parse)
df.dtypes

By sorting the values by time, parsing and indexing the column date as a date object the data frame can be plotted. 

plt.figure(figsize = (12, 5))

plt.title('Sentiment Comparision')
plt.plot(df['time'], df['polarity'])
plt.plot(df['time'], df['subjectivity'])

plt.xlabel('Time')
plt.ylabel('Sentiment Value')

Analysis:
We can see from the graph that there are multiple gaps in the data, this might be due to the trend in tweets and no one actually tweeting in the stipulated time. 

Aggregating the latitude and longitude values, and plotting them using mplleaflet we can see the temporal distribution of tweets. 

lats = [lat[0] for lat in locations]
longi = [long[1] for long in locations]

print(lats, " +  ", longi)
lats = list(filter(lambda a: a != 'p', lats))

import mplleaflet

mapdf = pd.DataFrame({'lat': lats, 'longi': longi, 'polarity':polarities[:len(lats)]})
plt.figure(figsize=(8, 8))
plt.scatter(longi, lats, c = polarities[:len(lats)])
mplleaflet.display()



In the final representation of Heroku, much emphasis was given to user experience and more varied pots are made. 

Link: 
