import nltk
import sys
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
sys.path.append( 'app/model/')
from models import Tweet, db
from peewee import SQL

class Utils:
    @staticmethod
    def frequent_words(count):
        go_stop = [u'https', u'go', u'gobus', u'station', u'hi', u'we', u'train', u'us']
        stop = stopwords.words('english') + go_stop
        s_stop = [str(w) for w in stop]
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
        
        return all_words.most_common(count)

    