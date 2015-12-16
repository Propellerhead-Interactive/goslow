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
    
    def __init__(self, trip_id, departure_time, arrival_time, from_stop_id, to_stop_id):
        self.trip_id = trip_id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.from_stop_id = from_stop_id
        self.to_stop_id = to_stop_id

class Users(BaseModel):
    id = PrimaryKeyField()
    username = TextField()
    github_access_token = TextField()
    class Meta:
        db_table = 'users'
   
        
        
class Keys(BaseModel):
    id = PrimaryKeyField()
    api_key = TextField()   
    name = TextField()
    user =  ForeignKeyField(Users, related_name='keys')  
    class Meta:
        db_table = 'keys'



class Tweet(BaseModel):
    content = TextField()
    tweet_id = TextField()
    tweet_time = TextField()
    at_reply = BooleanField(default=True)
    author = TextField() 
    sentiment = IntegerField()
    sentiment_level = DecimalField()

db.create_tables([Users, Tweet], safe=True) 
db.create_tables([Keys], safe=True) 

   


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
        primary_key = peewee.CompositeKey('trip_id', 'stop_id', 'stop_sequence') 
    
class Status(BaseModel):
    route = TextField()
    fromStop = TextField()
    toStop = TextField()
    train_date = DateField(default=datetime.date)
    train_time = TextField()
    delay_time = TextField()
    message = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table = 'status'
        
    

db.create_tables([Status], safe=True) 

