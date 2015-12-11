import sys
sys.path.append( 'app/model/')
from models import Tweet, db
from peewee import SQL
import sentiment_mod as st

def compute_sentiment():

    tweets = Tweet.select()#.where("sentiment=")
    for tw in tweets:
        text = tw.content
        print text
        #sentiment_value, confidence
        print st.sentiment(text)
        #print sentiment_value, confidence, text
        
        
    
    
compute_sentiment()
