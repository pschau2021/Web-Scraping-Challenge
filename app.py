#################################################
# MongoDB and Flask Application
#################################################
# Dependencies and Setup
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Setup mongo connection 27017
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Use Flask_PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")

def index():
    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()
    
    # Return template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_data.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug=True)
