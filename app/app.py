import sys
from flask import Flask
from flask import render_template

sys.path.insert(0, 'app/model/')
from models import TrainRoute, Status

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    use_reloader=True
)

@app.route("/")
def hello():
    
    return render_template("index.html")

@app.route("/schedule")
def delays():
    schedule = Status.get()
    return render_template("delays.html", items=schedule)

if __name__ == "__main__":
    app.run()

