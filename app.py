# Import Flash, PyMongo and BSON dependencies
import os
from flask import Flask, render_template
import pymongo
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Import environment variables if they exist
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# Configure Flask and MongoDB
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DBNAME = os.environ.get("MONGO_DBNAME")
MONGO_COLLECTION = "restaurants"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


@app.route("/")
def index():
    conn = mongo_connect(MONGO_URI)
    coll = conn[MONGO_DBNAME][MONGO_COLLECTION]
    documents = coll.find()
    # for doc in documents:
    #    print(doc)
    restaurants = list(mongo.db.restaurants.find())
    return render_template("index.html", documents=documents)


# set debug to false when operational
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"), debug=True)






