#Imports
import sys
sys.path.append( 'app/model/')
from models import Tweet, db
from peewee import SQL
import string
import twitter

# Twitter Logic
api = twitter.Api(consumer_key='zKWUxAituSEtELXZTUFZIpvN6',consumer_secret='DLtc8CJMCkGMHEChhwuEjuXM7OH0WzaJhZ1XyTSTPr7gxvnelz',access_token_key='11184792-wo0VQ63FhjVOsOgs28Mqk77CH73PB2KShCP8DwBKF',access_token_secret='PSAaONv8W7S8HJKWUMxappcr3khcAV2nlQfJPjzm5iZbN')

def storeStatuses(st):
  if st:
    print "Added " + str(len(st)) + " new records."
    with db.atomic():
        for s in st:
            u = s.user.screen_name
            if u!= "GOtransit" and "RT" not in s.text:
                atreply = True
                if s.text[0] != "@":
                    atreply = False
                    txt = clean(s.text)
                    Tweet.create(sentiment=0, sentiment_level=0, author=s.user.screen_name, content=txt, at_reply=atreply, tweet_time=s.created_at_in_seconds, tweet_id=s.id)
  else:
    print "No new tweets"

def clean(text):
    return filter(lambda x: x in string.printable, text)


def main():
    db.connect()
    db.create_tables([Tweet], safe=True) 

    if Tweet.select().where(SQL('author!="gotransit"')).count() > 0:
      last_tweet = int(Tweet.select().where(SQL('author!="gotransit"')).order_by(-Tweet.tweet_time).limit(1).get().tweet_id)
      statuses = api.GetUserTimeline(screen_name="gotransit",count=200, since_id=last_tweet)
    else:
      oldest_tweet = 0
      statuses = []
      count = 1
      while count < 17:
        print "Loading DB with 200 tweets..."
        more_statuses = api.GetSearch(term="gotransit",count=200*count, max_id=oldest_tweet)
        if count > 1:
          more_statuses.pop(0)
        oldest_tweet = more_statuses[-1].id
        statuses += more_statuses
        count += 1
        break

    storeStatuses(statuses)
    db.commit()
  
main()