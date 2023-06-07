from collections import defaultdict
import threading
from datetime import datetime


class Counter:
    def __init__(self):
        self.lock = threading.Lock()
        self.counter = defaultdict(int)
        self.unique_visitors = defaultdict(set)  # store unique visitors
        self.daily_visits = defaultdict(int)  # store daily visits

    def increment(self, page, visitor_id):
        with self.lock:
            self.counter[page] += 1
            self.unique_visitors[page].add(visitor_id)
            self.daily_visits[str(datetime.now().date())] += 1

    def get_count(self, page):
        with self.lock:
            return self.counter[page]

    def get_unique_visitors(self, page):
        with self.lock:
            return len(self.unique_visitors[page])

    def get_daily_visits(self):
        with self.lock:
            return dict(self.daily_visits)


counter = Counter()
