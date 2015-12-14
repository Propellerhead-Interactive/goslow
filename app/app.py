import sys, json
from flask import Flask, jsonify
from flask import render_template
from playhouse.shortcuts import *
import sys
sys.path.append( 'app/model/')
sys.path.append( 'app/helper/')
from search import TrainSearch
from models import Tweet, db
from utils import Utils

sys.path.insert(0, 'app/model/')
from models import Routes, Status

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    use_reloader=True
)

@app.route("/")
def hello():
    words = {}
    words['delay'] = Tweet.select().where(Tweet.content.contains('delay')).count()
    words['sorry'] = Tweet.select().where(Tweet.content.contains('sorry')).count()
    words['signal'] = Tweet.select().where(Tweet.content.contains('signal')).count()
    words['switch'] = Tweet.select().where(Tweet.content.contains('switch')).count()
    words['problem'] = Tweet.select().where(Tweet.content.contains('problem')).count()
    words['issue'] = Tweet.select().where(Tweet.content.contains('issue')).count()
    words['cancel'] = Tweet.select().where(Tweet.content.contains('cancel')).count()
    words['oos'] = Tweet.select().where(Tweet.content.contains('out of service')).count()
    
    return render_template("index.html", words=words)

@app.route("/word_fun")
def wordfun():
    items = Utils.frequent_words(20)
    return render_template("delays.html", items=items)
    
#################API#######################

@app.route("/api")
def api():
    '''Doesnt do anything'''
    return jsonify({"message":"usage:TBD"})

#shows all the routes for the given system
@app.route("/api/<systemID>/routes",methods = ['GET'])
def all_routes(systemID):
    r = Routes.select().where(Routes.route_type==2)
    all_r = []
    for rr in r:
        all_r.append(model_to_dict(rr))
    return jsonify({"routes":(all_r) })

@app.route("/api/<systemID>/routes/<routeID>",methods = ['GET'])
def the_routes(systemID,routeID):
    '''shows a single route for the given system given *routeID*'''
    r = Routes.select().where(Routes.route_type==2).where(Routes.route_id==routeID)
    all_r = []
    for rr in r:
        all_r.append(model_to_dict(rr))
    return jsonify({"routes":all_r})

#shows all the times for the times route
@app.route("/api/<systemID>/routes/<routeID>/times",methods = ['GET'])
def the_route_times(systemID,routeID):
    return jsonify({"message":"usage:TBD"})
 
 
#shows cloest station to the person
@app.route("/api/<systemID>/close/<lat>/<lon>",methods = ['GET'])
def the_closest_stop(systemID, lat, lon):
    s = TrainSearch.find_closest(lat, lon)
    return jsonify({"stop":s})

   
#shows the given status for the routes
@app.route("/api/<systemID>/routes/<routeID>/status",methods = ['GET'])
def the_route_status(systemID,routeID):
    return jsonify({"message":"usage:TBD"})
    
#shows the given schedule for the routes for today
@app.route("/api/<systemID>/routes/<routeID>/schedule",methods = ['GET'])
def the_route_schedule(systemID,routeID):
    return jsonify({"message":"usage:TBD"})
    

#shows the given status for the routes - third arg is day of week
@app.route("/api/<systemID>/search_today/<from_station>/<to_station>",methods = ['GET'])
def the_route_search_today(systemID,from_station,to_station):
    s = TrainSearch.find_route(from_station, to_station, 0)
    #request.data
    return jsonify({"trips":s})
    
#shows the given status for the routes - third arg is day of week
@app.route("/api/<systemID>/search/<from_station>/<to_station>/<dow>",methods = ['GET'])
def the_route_search(systemID,from_station,to_station, dow):
    s = TrainSearch.find_route(from_station, to_station, dow)
    #request.data
    return jsonify({"trips":s})


#Lists all train stations
@app.route("/api/<systemID>/stops",methods = ['GET'])
def all_stops(systemID):
    s = TrainSearch.get_stops() #request.data
    all_r = []
    for rr in s:
        all_r.append(model_to_dict(rr))
    return jsonify({"routes":all_r })

#Lists all destination stations from origin station
@app.route("/api/<systemID>/stops/<from_station>",methods = ['GET'])
def all_stops_from_origin(systemID, from_station):
    s = TrainSearch.get_stops_from_origin(from_station) #request.data
    all_r = []
    for rr in s:
        if rr.stop_name.lower() != from_station.lower():
            all_r.append(model_to_dict(rr))
    return jsonify({"routes":all_r })

if __name__ == "__main__":
    app.run()

