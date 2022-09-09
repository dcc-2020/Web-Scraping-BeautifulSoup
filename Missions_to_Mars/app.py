from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_app')


@app.route("/")
def index():
    mars_data = mongo.db.collection.find_one()
    return render_template('index.html', mars=mars_data)


@app.route("/scrape")
def scraping():
    data = scrape_mars.scrape()
    mongo.db.collection.update_one({}, {'$set': data}, upsert=True)
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run(debug=True)