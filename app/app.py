import sys
from flask import Flask, jsonify
from flask import render_template
import sys
sys.path.append( 'app/model/')
sys.path.append( 'app/helper/')

from models import Tweet, db
from utils import Utils

sys.path.insert(0, 'app/model/')
from models import TrainRoute, Status

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
    
@app.route("/api")
def api():
    return jsonify({"message":"usage:TBD"})

if __name__ == "__main__":
    app.run()

