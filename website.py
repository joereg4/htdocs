from flask import Flask, render_template
import os
import feedparser
from models import db, Counter
from flask_migrate import Migrate

app = Flask(__name__)

migrate = Migrate(app, db)

# Configure the SQLite database URI
database_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
database_file = os.path.join(database_dir, 'count.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the data directory if it doesn't exist
if not os.path.exists(database_dir):
    os.makedirs(database_dir)

db.init_app(app)


def increment_page_counter(page_name):
    page_counter = Counter.query.filter_by(page=page_name).first()
    if page_counter:
        page_counter.count += 1
    else:
        page_counter = Counter(page=page_name, count=1)
        db.session.add(page_counter)
    db.session.commit()


@app.route('/')
def home():
    increment_page_counter('home')
    return render_template('index.html')


@app.route('/blog/')
def blogfeed():
    increment_page_counter('blog')
    # Parse the RSS feed
    feed = feedparser.parse('http://jregenstein.com/feed')

    # Pass the feed title and entries to the template
    return render_template('blogfeed.html', title=feed.feed.title, entries=feed.entries)


@app.route('/social/')
def social():
    increment_page_counter('social')
    return render_template('social.html')


@app.route('/now/')
def now():
    increment_page_counter('now')
    return render_template('now.html')


@app.route('/book/')
def book():
    increment_page_counter('book')
    return render_template('book.html')


@app.route('/counts/')
def counts():
    counts = Counter.query.all()
    return render_template('counts.html', counts=counts)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
