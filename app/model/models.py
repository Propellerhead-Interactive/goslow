import peewee
from peewee import *
import datetime

#db = MySQLDatabase('goslow', user='goslow',passwd='goslow1!23', host='192.168.0.147')
db = MySQLDatabase('goslow', user='root',passwd='')

class BaseModel(peewee.Model):
    class Meta:
        database = db
        

class ComposedSchedule():
    trip_id = None
    departure_time = None
    arrival_time = None
    from_stop_id = None
    to_stop_id = None
    direction = None
    
    def __init__(self, trip_id, departure_time, arrival_time, from_stop_id, to_stop_id, direction):
        self.trip_id = trip_id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.from_stop_id = from_stop_id
        self.to_stop_id = to_stop_id
        self.direction = direction
        
    

class Tweet(BaseModel):
    content = TextField()
    tweet_id = TextField()
    tweet_time = TextField()
    at_reply = BooleanField(default=True)
    author = TextField() 
    sentiment = IntegerField()
    sentiment_level = DecimalField()

class CalendarDates(BaseModel):
    service_id = TextField()
    date = TextField()

    class Meta:
        db_table = 'calendar_dates'

#this is a line - top level for a number of stations
class Routes(BaseModel):
    route_id = TextField(primary_key=True)
    route_short_name = TextField()
    route_long_name = TextField()
    route_type = IntegerField()

class Trips(BaseModel):
    route = ForeignKeyField(Routes, related_name='routeid')
    service_id = TextField()
    trip_id = TextField(primary_key=True)
    direction_id = IntegerField()

#This is a location - contains info on the location
class Stops(BaseModel):
    stop_id = TextField(primary_key=True)
    stop_name = TextField()
    stop_lat = FloatField()
    stop_lon = FloatField()
    

class StopTimes(BaseModel):
    trip = ForeignKeyField(Trips, related_name='tripid')
    arrival_time = TextField()
    departure_time = TextField()
    stop = ForeignKeyField(Stops, related_name='stops')
    stop_sequence = IntegerField()

    class Meta:
        db_table = 'stop_times'
    
class Status(BaseModel):
    route = ForeignKeyField(Routes, related_name='routes')
    message = TextField()
    trip = ForeignKeyField(Trips, related_name='trips')
    created_at = DateTimeField(default=datetime.datetime.now)
