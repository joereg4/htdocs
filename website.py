import os
from flask import Flask, render_template, g, request, make_response, jsonify
import feedparser
from counter import counter
import uuid
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = MongoClient(os.environ.get("MONGODB_URI"))
app.db = client.get_default_database()


@app.before_request
def before_request():
    visitor_id = request.cookies.get('visitor_id')
    if not visitor_id:
        visitor_id = str(uuid.uuid4())
        g.visitor_id = visitor_id
        resp = make_response()
        resp.set_cookie('visitor_id', visitor_id)
    else:
        g.visitor_id = visitor_id


@app.route('/')
def home():
    counter.increment('home', g.visitor_id)
    return render_template('index.html')


@app.route('/blog/')
def blogfeed():
    counter.increment('blog', g.visitor_id)
    # Parse the RSS feed
    feed = feedparser.parse('http://jregenstein.com/feed')

    # Pass the feed title and entries to the template
    return render_template('blogfeed.html', title=feed.feed.title, entries=feed.entries)


@app.route('/social/')
def social():
    counter.increment('social', g.visitor_id)
    return render_template('social.html')


@app.route('/now/')
def now():
    counter.increment('now', g.visitor_id)
    return render_template('now.html')


@app.route('/book/')
def book():
    counter.increment('book', g.visitor_id)
    return render_template('book.html')


@app.route('/counts/')
def counts():
    counts = {doc['page']: {'count': doc['count'], 'unique_visitors': len(doc['unique_visitors'])} for doc in
              counter.pages.find()}
    return render_template('counts.html', counts=counts)


@app.route('/data')
def data():
    return jsonify(counter.get_daily_visits())


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.run(host='0.0.0.0', port=5000)
