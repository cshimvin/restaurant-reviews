# Import Flash, PyMongo and BSON dependencies
import os
from flask import Flask, render_template, url_for, redirect, request
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
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    restaurants = list(mongo.db.restaurants.find({"$text": {"$search": query}}))
    return render_template("index.html", restaurants=restaurants)


@app.route("/get_restaurants")
def get_restaurants():
    restaurants = list(mongo.db.restaurants.find())
    return render_template("restaurants.html", restaurants=restaurants)


@app.route("/edit_restaurant/<restaurant_id>", methods=["GET", "POST"])
def edit_restaurant(restaurant_id):
    if request.method == "POST":
        submit = {
            "$set": {
                "name": request.form.get("name"),
                "url": request.form.get("url"),
                "type": request.form.get("type"),
                "address": request.form.get("address"),
                "town": request.form.get("town"),
                "county": request.form.get("county"),
                "postcode": request.form.get("postcode"),
                "description": request.form.get("description"),
                "image_url": request.form.get("image")
            }
        }
        restaurant = mongo.db.restaurants.find_one({"_id": ObjectId(restaurant_id)})
        mongo.db.restaurants.update_one({"_id": ObjectId(restaurant_id)}, submit)
        cuisines = list(mongo.db.restaurant_types.find().sort("type", 1))
        message = "Restaurant Successfully Updated"
        return render_template("edit_restaurant.html", restaurant=restaurant, message=message, cuisines=cuisines)
    restaurant = mongo.db.restaurants.find_one({"_id": ObjectId(restaurant_id)})
    # Get list of restaurant types to populate the cuisine select list
    cuisines = list(mongo.db.restaurant_types.find().sort("type", 1))
    return render_template("edit_restaurant.html", restaurant=restaurant, cuisines=cuisines)


@app.route("/add_restaurant", methods=["GET", "POST"])
def add_restaurant():
    if request.method == "POST":
        submit = {
                "name": request.form.get("name"),
                "url": request.form.get("url"),
                "type": request.form.get("type"),
                "address": request.form.get("address"),
                "town": request.form.get("town"),
                "county": request.form.get("county"),
                "postcode": request.form.get("postcode"),
                "description": request.form.get("description"),
                "image_url": request.form.get("image")
        }
        mongo.db.restaurants.insert_one(submit)
        message = "Restaurant Successfully Added"
        cuisines = list(mongo.db.restaurant_types.find().sort("type", 1))
        return render_template("add_restaurant.html", message=message, cuisines=cuisines)
    # Get list of restaurant types to populate the cuisine select list
    cuisines = list(mongo.db.restaurant_types.find().sort("type", 1))
    return render_template("add_restaurant.html", cuisines=cuisines)


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.restaurant_types.find().sort("type", 1))
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        submit = {
            "type": request.form.get("type")
        }
        mongo.db.restaurant_types.insert_one(submit)
        message = "Category Successfully Added"
        categories = list(mongo.db.restaurant_types.find().sort("type", 1))
        categories = list(mongo.db.restaurant_types.find().sort("type", 1))
        categories = list(mongo.db.restaurant_types.find().sort("type", 1))
        return render_template("categories.html", message=message, categories=categories)
    return render_template("add_category.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "$set": {
                "type": request.form.get("type")
            }
        }
        restaurant = mongo.db.restaurant_types.find_one({"_id": ObjectId(category_id)})
        mongo.db.restaurant_types.update_one({"_id": ObjectId(category_id)}, submit)
        categories = list(mongo.db.restaurant_types.find().sort("type", 1))
        message = "Category Successfully Updated"
        return render_template("categories.html", message=message, categories=categories)
    category = mongo.db.restaurant_types.find_one({"_id": ObjectId(category_id)})
    # Get list of restaurant types to populate the cuisine select list
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.restaurant_types.delete_one({"_id": ObjectId(category_id)})
    message = "Category Successfully Deleted"
    categories = list(mongo.db.restaurant_types.find().sort("type", 1))
    return render_template("categories.html", message=message, categories=categories)


@app.route("/users")
def get_users():
    return render_template("users.html")


# set debug to false when operational
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"), debug=True)
