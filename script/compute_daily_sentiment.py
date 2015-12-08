import nltk
import sys
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
sys.path.append( 'app/model/')
from models import Tweet, db
from peewee import SQL


def commonalities():
    stop = stopwords.words('english')
    punct = ['!',':','@', '']
    tknzr = RegexpTokenizer(r'\w+')
    all_words = []
    tweets = Tweet.select()
    all_tweet_text = [tw.content for  tw in tweets]
    tweet_text = (''.join(all_tweet_text))
    print tweet_text
    for w in tknzr.tokenize(str(tweet_text)):
        if "@" not in w and w not in stop :
            all_words.append(w.lower()) 
    all_words = nltk.FreqDist(all_words)
    print all_words
    print(all_words.most_common(15))

commonalities()