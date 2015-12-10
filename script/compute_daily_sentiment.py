import nltk
import sys
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
sys.path.append( 'app/model/')
from models import Tweet, db
from peewee import SQL
import sentiment_mod as st

def compute_sentiment():

    tweets = Tweet.select().where("sentiment=0")
    for tw in tweets:
        text = tw.content
        print text
        sentiment_value, confidence = s.sentiment(text)
        print sentiment_value, confidence, text
        
        
    
    
compute_sentiment()
