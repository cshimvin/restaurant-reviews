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
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_restaurants")
def index():
    restaurants = mongo.db.restaurants.find()
    return render_template("index.html", restaurants=restaurants)


@app.route("/categories")
def get_categories():
    return render_template("categories.html")


@app.route("/users")
def get_users():
    return render_template("users.html")


# set debug to false when operational
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"), debug=True)
