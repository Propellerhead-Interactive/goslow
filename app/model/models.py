import peewee
from peewee import *
import datetime

db = MySQLDatabase('goslow', user='root',passwd='')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class TrainRoute(BaseModel):
    route_name = TextField()
    route_id = IntegerField()
    route_time = TimeField()

class Status(BaseModel):
    route = ForeignKeyField(TrainRoute, related_name='train_routes')
    message = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

class Tweet(BaseModel):
    content = TextField()
    tweet_id = TextField()
    tweet_time = TextField()
    at_reply = BooleanField(default=True)
    author = TextField() 
    sentiment = IntegerField()
    sentiment_level = DecimalField()
