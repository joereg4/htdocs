from flask import Flask, render_template
import logging
import feedparser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog/')
def blogfeed():
    # Parse the RSS feed
    feed = feedparser.parse('http://jregenstein.com/feed')

    # Pass the feed title and entries to the template
    return render_template('blogfeed.html', title=feed.feed.title, entries=feed.entries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
