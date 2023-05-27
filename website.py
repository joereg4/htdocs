from flask import Flask, render_template
import feedparser

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/blog/')
def blogfeed():
    # Parse the RSS feed
    feed = feedparser.parse('http://jregenstein.com/feed')

    # Pass the feed title and entries to the template
    return render_template('blogfeed.html', title=feed.feed.title, entries=feed.entries)


@app.route('/social/')
def social():
    return render_template('social.html')


@app.route('/now/')
def now():
    return render_template('now.html')


@app.route('/book/')
def book():
    return render_template('book.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
