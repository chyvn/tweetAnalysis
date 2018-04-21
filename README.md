# twitterAnalysis

Complete Notebook link : https://drive.google.com/file/d/1V8Sl8WW_X7GuOuM-lJZ7oSwy0zfDF1jP/view?usp=sharing


## Step 1: Get tweets.

To understand and estimate user sentiments over twitter to real news, we first need a lot of tweets. Our first task is to get as many as 10K tweets. 

Instead of going for 10K tweets, I first got 500 tweets for sample. These tweets were searched specifically for "#modi", "#commonwealth", "#facebook", "#music."

Using the library tweepy, I have acquired the specified number of tweet. These tweets were subsequently pushed to the mongoDB. 

These data sets are present in the folder [Datasets](https://github.com/chyvn/tweetAnalysis/tree/master/DataSets).


##Step 2: Clean the data.
Once the data sets are cleaned using [script](https://github.com/chyvn/tweetAnalysis/blob/master/Scripts/cleaning_new.py) the [cleaned data sets](https://github.com/chyvn/tweetAnalysis/tree/master/DataSets) are generated.


##Step 3: Analyze the data.
The data sets are then used to analyze [sentiments](https://github.com/chyvn/tweetAnalysis/blob/master/Scripts/results.py). 

##Step 4: Presenting the analysis
These sentiment values are plotted in python using libraries [matplotlib](https://matplotlib.org/), [mplleaflet](https://github.com/jwass/mplleaflet). And the resulting graphs can be seen in [html notebook results](https://github.com/chyvn/tweetAnalysis/tree/master/Outputs/NotebooksHtml).

##Step 5: Hosting the results
To present the work in web format, I have generated [json files](https://github.com/chyvn/tweetAnalysis/blob/master/Outputs/output.json). The [website]() is hosted [at]().
