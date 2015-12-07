from flask import Flask

app = Flask(__name__, template_folder="views")

@app.route("/")
def hello():
    return "Hello World!"
 
@app.route("/test")   
def test():
    return render_template("views/test.html")

if __name__ == "__main__":
    app.run()

