from flask import Flask, render_template
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
    app.run(port=8000)
