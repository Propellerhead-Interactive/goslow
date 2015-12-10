import peewee
from peewee import *
import datetime

db = MySQLDatabase('goslow', user='goslow',passwd='goslow1!23', host='192.168.0.147')
db_gtfs = MySQLDatabase('gtfs', user='root',passwd='')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class GTFSModel(peewee.Model):
    class Meta:
        database = db_gtfs

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

class CalendarDates(GTFSModel):
    service_id = TextField()
    date = TextField()

    class Meta:
        db_table = 'calendar_dates'

class Routes(GTFSModel):
    route_id = TextField(primary_key=True)
    route_short_name = TextField()
    route_long_name = TextField()
    route_type = IntegerField()

class Stops(GTFSModel):
    stop_id = TextField(primary_key=True)
    stop_name = TextField()

class StopTimes(GTFSModel):
    trip_id = TextField()
    arrival_time = TextField()
    departure_time = TextField()
    stop_id = TextField()
    stop_sequence = IntegerField()

    class Meta:
        db_table = 'stop_times'

class Trips(GTFSModel):
    route_id = TextField()
    service_id = TextField()
    trip_id = TextField(primary_key=True)
    direction_id = IntegerField()
