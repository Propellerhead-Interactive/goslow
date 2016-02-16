import sys, json, uuid
sys.path.append( './app/model/')
sys.path.append( './app/helper/')
sys.path.append( './app/lib/')

import time
from datetime import date

from flask import Flask, jsonify,request, g, session, redirect, url_for, flash, render_template
from playhouse.shortcuts import *
from flask_github import GitHub
from flask.ext.autodoc import Autodoc

from search import TrainSearch
from models import *
from refund import Refund
from utils import Utils



from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader
import assets

app = Flask(__name__)

app.config['GITHUB_CLIENT_ID'] = 'd0155a375a97ba22c38c'
app.config['GITHUB_CLIENT_SECRET'] = 'e64a177e17970823444c9b1a124c4380d8f4bfd5'
app.config['GITHUB_BASE_URL'] = 'https://api.github.com/'
#app.config['GITHUB_AUTH_URL'] = 'https://localhost:5000/login/oauth/'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config.update(
    DEBUG=True,
    use_reloader=True
)

github = GitHub(app)
auto = Autodoc(app)


assets_env = Environment(app)
assets_loader = PythonAssetsLoader(assets)
for name, bundle in assets_loader.load_bundles().iteritems():
        assets_env.register(name, bundle)




############### GITHUB OAUTH ###################

@app.before_request
def before_request():
    g.user = None
    if 'token' in session:
        u = Users.select().where(Users.github_access_token==session['token']).get()
        g.user = u
        session["user_id"]=g.user.id
       
        
        
@app.context_processor
def inject_user():
    t = token_getter()
    if not t == "":
        data = github.get("user")
        return dict(user_data=data)
    else:
        return dict(user_data=dict())

@app.after_request
def after_request(response):
    #session['user'] = None
    return response

@app.route('/login')
def login():
    return github.authorize()

# @app.route('/me')
# def me():
#     me = github.get('user')
#     x = me["login"]
#     return jsonify({"me":me})
       
    
@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('api_key_index')
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)
        
    session['token'] = oauth_token
    try:
        user = Users.select().where(Users.github_access_token==oauth_token).get()
    except Users.DoesNotExist:
        #print str(github.get('/user' ))
        user = Users.create(github_access_token = oauth_token, username="temp")
        
        
    user.github_access_token = oauth_token
    s = github.get('user')
    x = s["login"]
    user.username=x
    user.save()
    session['user'] = user
    
    return redirect(next_url)
    
@github.access_token_getter
def token_getter():
    user = g.user
    a = ""
    if user is not None:
        a= user.github_access_token
    elif  session.has_key('token'):
        a= session['token']
        
    else:
        a=""
        
    return a
#================= APP ========================

@app.route("/")
def hello():
    #since = date.fromtimestamp(float(Tweet.get(Tweet.id == 1).tweet_time)).strftime('%B %d, %Y')
    words = {}
    words['delay'] = Tweet.select().where(Tweet.content.contains('delay')).count()
    words['late'] = Tweet.select().where(Tweet.content.contains('late')).count()
    words['sorry'] = Tweet.select().where(Tweet.content.contains('sorry')).count()
    words['signal'] = Tweet.select().where(Tweet.content.contains('signal')).count()
    words['switch'] = Tweet.select().where(Tweet.content.contains('switch')).count()
    words['problem'] = Tweet.select().where(Tweet.content.contains('problem')).count()
    words['issue'] = Tweet.select().where(Tweet.content.contains('issue')).count()
    words['cancel'] = Tweet.select().where(Tweet.content.contains('cancel')).count()
    words['oos'] = Tweet.select().where(Tweet.content.contains('out of service')).count()
    words['ontime'] = Tweet.select().where(Tweet.content.contains('on time')).count()
    
    return render_template("index.html", words=words, stops=refund(True))

@app.route("/lateness")
def lateness():
    items = Status.select()
     return render_template("delays.html", items=items)


@app.route("/word_fun")
def wordfun():
    items = Utils.frequent_words(20)
    return render_template("delays.html", items=items)

@app.route("/refund")
def refund(t=False):
    s = TrainSearch.get_stops()
    if t:
        return s
    else:
        return render_template("refunds.html", stops=s)

@app.route("/history",methods = ['GET'])
def history():
    statii = Status.select()
    return render_template("history.html", issues=statii)
    

@app.route("/history/search",methods = ['POST'])
def search_history():
    
    statii = Status.select().where(Status.route.contains(request.form["q"]))
    return render_template("history.html", issues=statii)
    
@app.route("/schedule/<route_id>",methods = ['GET'])
def today_schedule(route_id):
    route = Routes.select().where(Routes.route_short_name==route_id).get()
    
    stops = StopTimes.raw("Select * from stop_times inner join stops inner join trips where trips.route_id==%s", (route_id))
    
    #join(Stops).join("Trips").where(Trips.route_id==route.route_id)
    
    return render_template("schedule.html", route=route)


################# API HTML PAGES #######################

@app.route("/api")
def api():
    '''Doesnt do anything'''
    return render_template("api.html")

@app.route("/api/docs")
def api_docs():
    '''Shows the documentation'''
    return auto.html(
        template='docs.html',
        title='My Documentation',
        author='John Doe'
    )

    
@app.route("/api/keys")
def api_key_index():
    if g.user:
        
        keys_raw = Keys.select().where(Keys.user==g.user)
        keys = [k for k in keys_raw]
    else:
        keys = []
    return render_template("keys.html", keys = keys)
    
@app.route("/api/status")
def api_status_index():
    '''Doesnt do anything'''
    return render_template("status.html")
    
@app.route("/api/keys/create", methods=['POST'])
def api_key_create():
    '''Adds a new Key to the system'''
    key = Keys.create(api_key=uuid.uuid1(), name=request.form['name'], user=g.user)
    
    return  redirect("/api/keys")
    
@app.route("/api/keys/del", methods=['POST'])
def api_key_delete():
    '''REmove a  Key to the system'''
    
    key = Keys.delete().where(Keys.api_key==request.form["api_key"])
    key.execute()
    
    return  redirect("/api/keys")


#================= Actual API ==============================

@app.route("/api/<systemID>/routes",methods = ['GET'])
@auto.doc()
def all_routes(systemID):
    """Returns all the routes for the given system."""
    r = Routes.select().where(Routes.route_type==2)
    all_r = []
    for rr in r:
        all_r.append(model_to_dict(rr))
    return jsonify({"routes":(all_r) })

@app.route("/api/<systemID>/routes/<routeID>",methods = ['GET'])
@auto.doc()
def the_routes(systemID,routeID):
    '''Returns a single route for the given system given *routeID*'''
    r = Routes.select().where(Routes.route_type==2).where(Routes.route_id==routeID)
    all_r = []
    for rr in r:
        all_r.append(model_to_dict(rr))
    return jsonify({"routes":all_r})

#shows all the times for the times route
@app.route("/api/<systemID>/routes/<routeID>/times",methods = ['GET'])
@auto.doc()
def the_route_times(systemID,routeID):
    """Returns all the times for the given route."""
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
    """Returns the details about a given route, including current status if available."""
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
    """Returns the given status for the routes - third arg is day of week"""
    #request.data
    return jsonify({"trips":s})
    
#
@app.route("/api/<systemID>/search/<from_station_id>/<to_station_id>/<int:departure_date>",methods = ['GET'])
@auto.doc()
def the_route_search(systemID,from_station_id,to_station_id, departure_date):
    """Returns the given status for the routes for a gien day of the week. (0 = Monday)"""
    s = TrainSearch.find_route(from_station_id, to_station_id, departure_date)
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
    """Returns a list of the stops available in the network"""
    s = TrainSearch.get_stops() #request.data
    
    all_r = []
    for rr in s:
        all_r.append(model_to_dict(rr))
    return jsonify({"routes":all_r })

#Lists all destination stations on the same line from origin station
@app.route("/api/<systemID>/stops/<from_station>",methods = ['GET'])
@auto.doc()
def all_stops_on_line(systemID, from_station):
    """Returns all the stops on the same line as from_station """
    s = TrainSearch.get_stops_from_line(from_station) #request.data
    all_r = []
    for rr in s:
        if rr.stop_name.lower() != from_station.lower():
            all_r.append(model_to_dict(rr))
    return jsonify({"routes":all_r })   

#Lists all destination stations on the same line from origin station
@app.route("/api/<systemID>/stops",methods = ['POST'])
@auto.doc()
def all_stops_from_origin(systemID):
    """Returns all the stops from origin station """
    s = TrainSearch.get_stops_from_origin(request.form['from_station'],
                                          request.form['travel_date'],
                                          request.form['travel_time'])
    return jsonify({"stops":s })   

@app.route("/api/<systemID>/stoptimes/<from_station_id>/<int:dep_date>",methods = ['GET'])
@auto.doc()
def the_stoptimes(systemID,from_station_id, dep_date):
    """Returns the given status for the routes for a gien day of the week. (0 = Monday)"""
    s = TrainSearch.find_route(from_station_id, False, dep_date)
    #request.data
    return jsonify({"times":s})



#-------------------SPECIFIC ACTIONS FOR GO--------------
@app.route("/api/<systemID>/refund",methods = ['POST'])
def do_refund(systemID):
    r = Refund.make_refund(request.form['pc_number'],
                       request.form['email'],
                       request.form['travel_date'],
                       request.form['from_station'],
                       request.form['to_station'],
                       request.form['travel_time'])

    return jsonify({"status": r})

if __name__ == "__main__":
    app.run()
