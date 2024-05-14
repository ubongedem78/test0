from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
# import environment variables from a .env file
from decouple import config
app = Flask(__name__)

print("Template Folder Path:", app.template_folder)

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# MongoDB connection string with the database name included
mongo_uri = config('MONGO_URI')

# Initialize MongoClient and connect to the database
client = MongoClient(mongo_uri)
db = client['Facial_Recognition_Attendance']  # Use the same database name as specified in the connection string

# Import routes from the routes.py file
from app import routes
