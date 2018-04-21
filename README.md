# twitterAnalysis

Complete Notebook link : https://drive.google.com/file/d/1V8Sl8WW_X7GuOuM-lJZ7oSwy0zfDF1jP/view?usp=sharing


## Step 1: Get tweets.

To understand and estimate user sentiments over twitter to real news, we first need a lot of tweets. Our first task is to get as many as 10K tweets. 

Instead of going for 10K tweets, I first got 500 tweets for sample. These tweets were searched specifically for "#modi", "#commonwealth", "#facebook", "#music."

Using the library tweepy, I have acquired the specified number of tweet. These tweets were subsequently pushed to the mongoDB. 

These data sets are present in the folder "Datasets". 
