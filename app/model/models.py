import peewee
from peewee import *
import datetime

db = MySQLDatabase('goslow', user='root',passwd='')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class TrainRoute(BaseModel):
    name = TextField()
    route_id = IntegerField()
    
class Status(BaseModel):
    route = ForeignKeyField(TrainRoute, related_name='train_routes')
    title = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    
def main():
    db.connect()
    db.create_tables([TrainRoute])
    db.create_tables([Status])
    db.commit()
  
main()
            