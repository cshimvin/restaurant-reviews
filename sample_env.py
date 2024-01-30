Set environment variables for app
"""
import os

# Variables to connect to Mongo DB
os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("SECRET_KEY", "your-secret-key")
os.environ.setdefault("MONGO_URI", "mongo-URI")
os.environ.setdefault("MONGO_DBNAME", "restaurant_review")
