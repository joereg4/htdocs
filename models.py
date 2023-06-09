#models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(50), nullable=False)
    count = db.Column(db.Integer, default=0)
