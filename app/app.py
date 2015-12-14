import sys, json
from flask import Flask, jsonify, render_template, request
from flask.ext.autodoc import Autodoc
from playhouse.shortcuts import *
import sys
sys.path.append( 'app/model/')
sys.path.append( 'app/helper/')
from search import TrainSearch
from refund import Refund
from models import Tweet, db
from utils import Utils


sys.path.insert(0, 'app/model/')
from models import Routes, Status

from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader
import assets

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    use_reloader=True
)
auto = Autodoc(app)

assets_env = Environment(app)
assets_loader = PythonAssetsLoader(assets)
for name, bundle in assets_loader.load_bundles().iteritems():
        assets_env.register(name, bundle)

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

@app.route("/refund")
def refund():
    s = TrainSearch.get_stops()
    return render_template("refunds.html", stops=s)
    
#################API#######################

@app.route("/api")
def api():
    '''Doesnt do anything'''
    return render_template("api.html")

@app.route("/api/docs")
def api_docs():
    '''Doesnt do anything'''
    return auto.html(
        template='docs.html',
        title='My Documentation',
        author='John Doe'
    )

    
@app.route("/api/keys")
def api_key_index():
    '''Doesnt do anything'''
    return render_template("keys.html")
    
@app.route("/api/status")
def api_status_index():
    '''Doesnt do anything'''
    return render_template("status.html")
    
@app.route("/api/keys/create", methods=['POST'])
def api_key_create():
    '''Adds a new Key to the system'''
    #add key
    
    return render_template("keys.html")#, keys = keys)

#================= Actual API ==============================

@app.route("/api/<systemID>/routes",methods = ['GET'])
@auto.doc()
def all_routes(systemID):
    """shows all the routes for the given system."""
    r = Routes.select().where(Routes.route_type==2)
    all_r = []
    for rr in r:
        all_r.append(model_to_dict(rr))
    return jsonify({"routes":(all_r) })

@app.route("/api/<systemID>/routes/<routeID>",methods = ['GET'])
@auto.doc()
def the_routes(systemID,routeID):
    '''shows a single route for the given system given *routeID*'''
    r = Routes.select().where(Routes.route_type==2).where(Routes.route_id==routeID)
    all_r = []
    for rr in r:
        all_r.append(model_to_dict(rr))
    return jsonify({"routes":all_r})

#shows all the times for the times route
@app.route("/api/<systemID>/routes/<routeID>/times",methods = ['GET'])
@auto.doc()
def the_route_times(systemID,routeID):
    """shows all the times for the given route."""
    return jsonify({"message":"usage:TBD"})
 
#shows cloest station to the person
@app.route("/api/<systemID>/close/<lat>/<lon>",methods = ['GET'])
@auto.doc()
def the_closest_stop(systemID, lat, lon):
    """Given Latitude and Logitude coords, returns the closest station"""
    s = TrainSearch.find_closest(lat, lon)
    return jsonify({"stop":s})
   
#shows the given status for the routes
@app.route("/api/<systemID>/routes/<routeID>/status",methods = ['GET'])
@auto.doc()
def the_route_status(systemID,routeID):
    """returns the details about a given route, including current status if available."""
    return jsonify({"message":"usage:TBD"})

# @app.route("/api/<systemID>/routes/<routeID>/schedule",methods = ['GET'])
# @auto.doc()
# def the_route_schedule(systemID,routeID):
#     """Shows the given schedule for the routes for today"""
#     return jsonify({"message":"usage:TBD"})
#
@app.route("/api/<systemID>/search_today/<from_station_id>/<to_station_id>",methods = ['GET'])
@auto.doc()
def the_route_search_today(systemID,from_station_id,to_station_id):
    s = TrainSearch.find_route(from_station_id, to_station_id, 0)
    """shows the given status for the routes - third arg is day of week"""
    #request.data
    return jsonify({"trips":s})
    
#
@app.route("/api/<systemID>/search/<from_station_id>/<to_station_id>/<int:dow>",methods = ['GET'])
@auto.doc()
def the_route_search(systemID,from_station_id,to_station_id, dow):
    """shows the given status for the routes for a gien day of the week. (0 = Monday)"""
    s = TrainSearch.find_route(from_station_id, to_station_id, dow)
    #request.data
    return jsonify({"trips":s})


@app.route("/api/<systemID>/trips/<trip_id>/",methods = ['GET'])
@auto.doc()
def the_trip(systemID,trip_id):
    """Shows details about a particular trip"""
    s = TrainSearch.find_trip(trip_id)
    #request.data
    return jsonify({"stops":s})

#Lists all train stations
@app.route("/api/<systemID>/stops",methods = ['GET'])
@auto.doc()
def all_stops(systemID):
    """lists all the stops available in the network"""
    s = TrainSearch.get_stops() #request.data
    
    all_r = []
    for rr in s:
        all_r.append(model_to_dict(rr))
    return jsonify({"routes":all_r })

#Lists all destination stations from origin station
@app.route("/api/<systemID>/stops/<from_station>",methods = ['GET'])
@auto.doc()
def all_stops_from_origin(systemID, from_station):
    """Returns all the stops from any given station"""
    s = TrainSearch.get_stops_from_origin(from_station) #request.data
    all_r = []
    for rr in s:
        if rr.stop_name.lower() != from_station.lower():
            all_r.append(model_to_dict(rr))
    return jsonify({"routes":all_r })

#Lists all destination stations from origin station
@app.route("/api/<systemID>/refund",methods = ['POST'])
def do_refund(systemID):
    Refund.make_refund(request.form['pc_number'],
                       request.form['email'],
                       request.form['travel_date'],
                       request.form['from_station'],
                       request.form['to_station'],
                       request.form['travel_time'])

if __name__ == "__main__":
    app.run()
