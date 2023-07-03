import os
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class Counter:
    def __init__(self):
        self.client = MongoClient(os.environ.get("MONGODB_URI"))
        self.db = self.client.get_default_database()
        self.pages = self.db.pages
        self.visits = self.db.visits

    def increment(self, page, visitor_id):
        self.pages.update_one(
            {'page': page},
            {'$inc': {'count': 1}, '$addToSet': {'unique_visitors': visitor_id}},
            upsert=True)
        self.visits.update_one(
            {'date': str(datetime.now().date())},
            {'$inc': {'count': 1}},
            upsert=True)

    def get_count(self, page):
        doc = self.pages.find_one({'page': page})
        return doc['count'] if doc else 0

    def get_unique_visitors(self, page):
        doc = self.pages.find_one({'page': page})
        return len(doc['unique_visitors']) if doc else 0

    def get_daily_visits(self):
        daily_visits = {doc['date']: doc['count'] for doc in self.visits.find()}
        return daily_visits


counter = Counter()
