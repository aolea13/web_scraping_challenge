#import
from flask import Flask, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
import scrape_mars

#Flask set up
app = Flask(__name__)

#PyMongo
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

#Flask Routes
@app.route('/')
def index():
    mars_data = mongo.db.mars.find_one()
    return render_template('index.html', mars_data=mars_data)

@app.route('/scrape')
def scrapper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert = True)
    return 'Scraping Successful'

#Main Behavior
if __name__ == '__main__':
    app.run()
