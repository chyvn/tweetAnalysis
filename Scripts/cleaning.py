from pymongo import MongoClient
from bson.json_util import dumps
client = MongoClient()
db = client.twitterDb
modiPosts = db.tenKtweets
texts = []
postsJson = []
for post in modiPosts.find():
    texts.append(post['text'])
    print (post['text'])
print(len(texts))
import re

texts = [text.lower() for text in texts]
texts = [re.sub('\W+', ' ', text) for text in texts]

texts = [re.sub('[^a-z0-9\s]', '', text) for text in texts]

print(texts, len(texts))


englishWords = open('eng_words.txt', 'rt').read()
englishWords.replace('rt', '')

cleanTexts = []
for text in texts:
    words = re.split(r'\W+', text)
    words = [word for word in words if word in englishWords]
    words = [word for word in words if word not in ['rt', 'co', 't', 'c']]
    text = ' '.join(words)
    print(len(text))
    cleanTexts.append(text)

from textblob import TextBlob
for text in cleanTexts:
    sentiment = TextBlob(text).sentiment
    print (len(text), text, sentiment)
len(cleanTexts)
from pymongo import MongoClient
from bson.json_util import dumps
import json
client = MongoClient()
db = client.twitterCleanDb
collection = db.tenKtweetsCleaned

for post in postsJson:
    print('this' + post)

from bson.json_util import loads
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
            print(jsonObj, '\n\n', cleanTexts[i], '\n\n\n')
            collection.insert_one(jsonObj)

    
