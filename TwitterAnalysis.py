
# # Twitter Sentiment Analysis

#LIBRARIES

from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
nltk.download('vader_lexicon')
import pycountry
import re
import string
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer


#AUTHENTICATION


consumerKey = ""
consumerSecret = ""
accessToken = ""
accessTokenSecret = ""
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


#ANALYSIS


def percentage(part,whole):
    return 100* float(part)/float(whole)

keyword=input("Please enter keyword to search")
noOfTweet=int(input("Please enter number of tweets to analyze"))

tweets=tweepy.Cursor(api.search_tweets,q=keyword).items(noOfTweet)

positive=0
negative=0
netural=0
polarity=0
tweet_list=[]
neutral_list=[]
negative_list=[]
positive_list=[]

for tweet in tweets:
    tweet_list.append(tweet.text)
    analysis=TextBlob(tweet.text)
    score=SentimentIntensityAnalyzer().polarity_scores(tweet.text)
    neg=score['neg']
    neu=score['neu']
    pos=score['pos']
    comp=score['compound']
    polarity+=analysis.sentiment.polarity
    if neg>pos:
        negative_list.append(tweet.text)
        negative+=1
    elif pos>neg:
        positive_list.append(tweet.text)
        positive+=1
    elif pos==neg:
        neutral_list.append(tweet.text)
        neutral+=str(1)

positive=percentage(positive,noOfTweet)
negative=percentage(negative,noOfTweet)
neutral=percentage(neutral,noOfTweet)
polarity=percentage(polarity,noOfTweet)
positive=format(positive,'.1f')
negative=format(negative,'.1f')
neutral=format(neutral,'.1f')


#TOTAL TWEETS


tweet_list=pd.DataFrame(tweet_list)
neutral_list=pd.DataFrame(neutral_list)
negative_list=pd.DataFrame(negative_list)
positive_list=pd.DataFrame(positive_list)
print("Total number of tweets: ",len(tweet_list))
print("Total number of positive tweets: ",len(positive_list))
print("Total number of negative tweets: ",len(negative_list))
print("Total number of neutral tweets: ",len(neutral_list))


#PIE CHART


labels = ['Positive ['+str(positive)+'%]' , 'Neutral ['+str(neutral)+'%]','Negative ['+str(negative)+'%]']
sizes = [positive, neutral, negative]
colors = ['yellowgreen', 'blue','red']
patches, texts = plt.pie(sizes,colors=colors, startangle=90)
plt.style.use('default')
plt.legend(labels)
plt.title("Sentiment Analysis Result for keyword: "+keyword)
plt.axis('equal')
plt.show()
