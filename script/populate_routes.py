import urllib2, sys, json
import json
sys.path.insert(0, 'app/model/')
from  models import TrainRoute, db, Status
from BeautifulSoup import BeautifulSoup


def setupTables():
    db.connect()
    db.create_tables([TrainRoute], safe=True)
    db.create_tables([Status], safe=True)
    db.commit()
    
def get_routes():
    setupTables()
    routes = range(150,950)
    src='http://gmcprod.metrolinx.com/pins/details/'
    for x in routes:
        newsrc=src + str(x)
        page = urllib2.urlopen(newsrc)
        #if len(page)>100:
        a = (str(BeautifulSoup(page)))
        
        if len(a) > 50:
            route = json.loads(a)
            route_id = route["trip"]["id"]
            route_name = route["trip"]["name"]
            route_time = route["trip"]["time"]
            
            print route_id, route_name, route_time
            route = TrainRoute.get_or_create(route_name=route_name, route_id = route_id, route_time = route_time)
           
get_routes()
        
    
    