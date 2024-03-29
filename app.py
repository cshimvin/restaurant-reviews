"""
Import Flash, PyMongo, password hash and BSON dependencies - taken from
https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+NRDB_L5+2022_Q3/courseware/9e2f12f5584e48acb3c29e9b0d7cc4fe/579bbf01edaf47938e6a860b8f08f275/
"""
from datetime import datetime
import os
from flask import Flask, render_template, url_for, redirect, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# Import environment variables if they exist
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

# Configure Flask and MongoDB
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# function to check if the current user has administrator privileges
def check_admin(user_id):
    """
    Check stated user has administrator privileges
    """
    admin_status = mongo.db.users.find_one({"username": user_id})
    return admin_status["is_admin"]


# main index page
@app.route("/")
@app.route("/index")
def index():
    """
    Display featured restaurants on the homepage
    """
    featured_restaurants = list(mongo.db.restaurants.find({"featured": True}))
    return render_template("index.html",
                           featured_restaurants=featured_restaurants)


# index page search for restaurants function
@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Query restaurant collection with user search
    """
    if request.form.get("query"):
        query = request.form.get("query")
        restaurants = list(mongo.db.restaurants.find(
            {"$text": {"$search": query}}))
        return render_template("index.html",
                               restaurants=restaurants, search="yes")
    return redirect(url_for("index"))


# edit restaurant details function
@app.route("/edit_restaurant/<restaurant_id>", methods=["GET", "POST"])
def edit_restaurant(restaurant_id):
    """
    Check user logged in as admin, retrieve restaurant and sumbit user edits.
    """
    user_id = session.get('user')
    if user_id:
        admin = check_admin(user_id)
        if admin == "yes":
            if request.method == "POST":
                if request.form.get("featured") == "on":
                    is_featured = True
                else:
                    is_featured = False
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
                        "image_url": request.form.get("image"),
                        "featured": is_featured
                    }
                }
                restaurant = mongo.db.restaurants.find_one(
                    {"_id": ObjectId(restaurant_id)})
                mongo.db.restaurants.update_one(
                    {"_id": ObjectId(restaurant_id)}, submit)
                cuisines = list(
                    mongo.db.restaurant_types.find().sort("type", 1))
                message = "Restaurant Successfully Updated"
                return render_template("edit_restaurant.html",
                                       restaurant=restaurant, message=message,
                                       cuisines=cuisines)
            restaurant = mongo.db.restaurants.find_one(
                {"_id": ObjectId(restaurant_id)})
            # Get list of restaurant types to populate the cuisine select list
            cuisines = list(mongo.db.restaurant_types.find().sort("type", 1))
            return render_template("edit_restaurant.html",
                                   restaurant=restaurant, cuisines=cuisines)
        return redirect(url_for("not_authorised"))
    return redirect(url_for("log_in"))


# add a restaurant
@app.route("/add_restaurant", methods=["GET", "POST"])
def add_restaurant():
    """
    Check user logged in and add submitted restaurant details to database
    """
    user_id = session.get('user')
    if user_id:
        admin = check_admin(user_id)
        if admin == "yes":
            if request.method == "POST":
                if request.form.get("featured") == "on":
                    is_featured = True
                else:
                    is_featured = False
                submit = {
                        "name": request.form.get("name"),
                        "url": request.form.get("url"),
                        "type": request.form.get("type"),
                        "address": request.form.get("address"),
                        "town": request.form.get("town"),
                        "county": request.form.get("county"),
                        "postcode": request.form.get("postcode"),
                        "description": request.form.get("description"),
                        "image_url": request.form.get("image"),
                        "featured": is_featured
                }
                mongo.db.restaurants.insert_one(submit)
                message = "Restaurant Successfully Added"
                cuisines = list(
                    mongo.db.restaurant_types.find().sort("type", 1))
                print(request.form.get("featured"))
                return render_template("add_restaurant.html", message=message,
                                       cuisines=cuisines)
            # Get list of restaurant types to populate the cuisine select list
            cuisines = list(mongo.db.restaurant_types.find().sort("type", 1))
            return render_template("add_restaurant.html", cuisines=cuisines)
        return redirect(url_for("not_authorised"))
    return redirect(url_for("log_in"))


# display a particular restaurant
@app.route("/display_restaurant/<restaurant_id>")
def display_restaurant(restaurant_id):
    """
    Retrieve requested restaurant from the restaurant collection
    """
    admin = ""
    user_id = session.get('user')
    if user_id:
        admin = check_admin(user_id)
    restaurant = mongo.db.restaurants.find_one(
        {"_id": ObjectId(restaurant_id)})
    reviews = list(mongo.db.reviews.find(
        {"restaurant_id": restaurant_id}).sort("review_date", -1))
    return render_template("display_restaurant.html", restaurant=restaurant,
                           reviews=reviews, admin=admin)


# delete a specified restaurant
@app.route("/delete_restaurant/<restaurant_id>")
def delete_restaurant(restaurant_id):
    """
    Check user is logged in as admin and delete restaurant
    and reviews from database
    """
    user_id = session.get('user')
    if user_id:
        admin = check_admin(user_id)
        if admin == "yes":
            mongo.db.restaurants.delete_one({"_id": ObjectId(restaurant_id)})
            message = "Restaurant Successfully Deleted"
            restaurants = list(mongo.db.restaurants.find().sort("type", 1))
            # clean up reviews linked to deleted restaurant
            mongo.db.reviews.delete_many({"restaurant_id": restaurant_id})
            return render_template("restaurants.html", message=message,
                                   restaurants=restaurants)
        return redirect(url_for("not_authorised"))
    return redirect(url_for("log_in"))


# get all categories
@app.route("/get_categories")
def get_categories():
    """
    Display a list of categories from the categories collection
    """
    admin = ""
    user_id = session.get('user')
    if user_id:
        admin = check_admin(user_id)
    categories = list(mongo.db.restaurant_types.find().sort("type", 1))
    return render_template("categories.html", categories=categories,
                           admin=admin)


# display restaurants for a particular category/cuisine
@app.route("/restaurants/<category_name>")
def get_restaurants(category_name):
    """
    Retrieve and display a list of restaurants from requested category
    """
    admin = ""
    user_id = session.get('user')
    if user_id:
        admin = check_admin(user_id)
    restaurants = list(mongo.db.restaurants.find({"type": category_name}))
    return render_template("restaurants.html", restaurants=restaurants,
                           category_name=category_name, admin=admin)


# add a category
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    """
    Check user is logged in as admin and add submitted category to the database
    """
    user_id = session.get('user')
    if user_id:
        admin = check_admin(user_id)
        if admin == "yes":
            if request.method == "POST":
                submit = {
                    "type": request.form.get("type")
                }
                mongo.db.restaurant_types.insert_one(submit)
                message = "Category Successfully Added"
                categories = list(
                    mongo.db.restaurant_types.find().sort("type", 1))
                categories = list(
                    mongo.db.restaurant_types.find().sort("type", 1))
                categories = list(
                    mongo.db.restaurant_types.find().sort("type", 1))
                return render_template("categories.html", message=message,
                                       categories=categories)
            return render_template("add_category.html")
        return redirect(url_for("not_authorised"))
    return redirect(url_for("log_in"))


# edit a specified category
@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    """
    Check user is logged in as admin, retrieve category and submit edited
    details
    """
    user_id = session.get('user')
    if user_id:
        admin = check_admin(user_id)
        if admin == "yes":
            if request.method == "POST":
                submit = {
                    "$set": {
                        "type": request.form.get("type")
                    }
                }
                mongo.db.restaurant_types.update_one(
                    {"_id": ObjectId(category_id)}, submit)
                categories = list(
                    mongo.db.restaurant_types.find().sort("type", 1))
                message = "Category Successfully Updated"
                return render_template("categories.html", message=message,
                                       categories=categories)
            category = mongo.db.restaurant_types.find_one(
                {"_id": ObjectId(category_id)})
            # Get list of restaurant types to populate the cuisine select list
            return render_template("edit_category.html", category=category)
        return redirect(url_for("not_authorised"))
    return redirect(url_for("log_in"))


# delete a specified category
@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    """
    Check user is logged in as admin and delete submitted category from the
    category collection
    """
    user_id = session.get('user')
    if user_id:
        admin = check_admin(user_id)
        if admin == "yes":
            mongo.db.restaurant_types.delete_one(
                {"_id": ObjectId(category_id)})
            message = "Category Successfully Deleted"
            categories = list(mongo.db.restaurant_types.find().sort("type", 1))
            return render_template("categories.html", message=message,
                                   categories=categories)
        return redirect(url_for("not_authorised"))
    return redirect(url_for("log_in"))


# add a review for a restaurant
@app.route("/add_review/<restaurant_id>", methods=["GET", "POST"])
def add_review(restaurant_id):
    """
    Check user is logged in and add submitted details to reviews collection
    """
    if request.method == "POST":
        user_id = session.get('user')
        if user_id:
            restaurant = mongo.db.restaurants.find_one(
                {"_id": ObjectId(restaurant_id)})
            now = datetime.now()
            review = {
                "title": request.form.get("title"),
                "review_date": now.strftime("%B %d, %Y"),
                "user_id": user_id,
                "food_rating": request.form.get("food_rating"),
                "service_rating": request.form.get("service_rating"),
                "overall_rating": request.form.get("overall_rating"),
                "restaurant_id": restaurant_id,
                "review_content": request.form.get("review_content")
            }
            mongo.db.reviews.insert_one(review)
            message = "Review Successfully Added"
            reviews = list(mongo.db.reviews.find(
                {"restaurant_id": restaurant_id}))
            return render_template("display_restaurant.html", message=message,
                                   restaurant=restaurant, reviews=reviews)
        else:
            return redirect(url_for("log_in"))
    user_id = session.get('user')
    if user_id:
        restaurant = mongo.db.restaurants.find_one(
            {"_id": ObjectId(restaurant_id)})
        return render_template("add_review.html", restaurant=restaurant)
    else:
        return redirect(url_for("log_in"))


# user administration function
@app.route("/user_admin")
def user_admin():
    """
    Check user is logged in as admin and retrieve users from users collection.
    This allows the admin user to change a users admin status or delete a user
    """
    user_id = session.get('user')
    if user_id:
        admin = check_admin(user_id)
        if admin == "yes":
            users = list(mongo.db.users.find().sort("username", 1))
            return render_template("user_admin.html", users=users)
        return redirect(url_for("not_authorised"))
    return redirect(url_for("log_in"))


# delete a user
@app.route("/delete_user/<user_id>")
def delete_user(user_id):
    """
    Check user is logged in as admin and delete a user from the users
    collection
    """
    current_user = session.get('user')
    if current_user:
        admin = check_admin(session["user"])
        if admin == "yes":
            mongo.db.users.delete_one({"_id": ObjectId(user_id)})
            message = "User Successfully Deleted"
            users = list(mongo.db.users.find().sort("username", 1))
            return render_template("user_admin.html", message=message,
                                   users=users)
        return redirect(url_for("not_authorised"))
    return redirect(url_for("log_in"))


# make or remove admin status from a user
@app.route("/toggle_admin/<user_id>/<admin_status>")
def toggle_admin(user_id, admin_status):
    """
    Check user is logged in as admin and change a users admin status in the
    database
    """
    admin_id = session.get('user')
    if admin_id:
        admin = check_admin(admin_id)
        if admin == "yes":
            if admin_status == "promote":
                submit = {
                    "$set": {
                        "is_admin": "yes"
                    }
                }
            else:
                submit = {
                    "$set": {
                        "is_admin": "no"
                    }
                }
            # user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            mongo.db.users.update_one({"_id": ObjectId(user_id)}, submit)
            message = "User Successfully Updated"
            users = list(mongo.db.users.find().sort("username", 1))
            return render_template("user_admin.html", message=message,
                                   users=users)
        return redirect(url_for("not_authorised"))
    return redirect(url_for("log_in"))


# register a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Create a user in the users collection with submitted username and password
    """
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            message = "Username already exists"
            return render_template("register.html", message=message)
        # check if passwords match
        if request.form.get("password1") != request.form.get("password2"):
            message = "Passwords do not match"
            return render_template("register.html", message=message)
        register_details = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password1")),
            "is_admin": "no"
        }
        mongo.db.users.insert_one(register_details)
        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        message = "Registration Successful!"
        return render_template("register.html", message=message)
    return render_template("register.html")


# log in function for website
@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    """
    Check submitted user exists in the users table and that the password
    matches.
    Set a session cookie if login is successful
    """
    if request.method == "POST":
        # check user exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                message = f"Welcome, {request.form.get("username")}"
                feat_restaurants = list(
                    mongo.db.restaurants.find({"featured": True}))
                if check_admin(request.form.get("username")) == "yes":
                    session["admin"] = "yes"
                return render_template("index.html", message=message,
                                       featured_restaurants=feat_restaurants)
            else:
                # invalid password match
                message = "Incorrect Username and/or Password"
                return render_template("login.html", message=message)
        else:
            # username doesn't exist
            message = "Incorrect Username and/or Password"
            return render_template("login.html", message=message)
    return render_template("login.html")


# log out function for website
@app.route("/logout")
def logout():
    """
    remove user from session cookie
    """
    user_id = session.get('user')
    if user_id:
        session.pop("user")
    admin = session.get('admin')
    if admin == "yes":
        session.pop("admin")
    return render_template("login.html", message="You have been logged out")


# Display not authorised page
@app.route("/not_authorised")
def not_authorised():
    """
    Display the not_authorised.html page if user tries to access a page which
    is admin only
    """
    return render_template("not_authorised.html")


# Custom 404 page
@app.errorhandler(404)
def page_not_found(e):
    """
    Display custom 404 page if page not found.
    Code from:
    https://zetbit.tech/categories/python/37/
    how-to-make-a-default-404-page-in-flask
    """
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"), debug=False)
