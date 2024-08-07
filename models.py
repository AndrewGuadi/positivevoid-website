from extensions import db
import json
from datetime import datetime

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))

    def __init__(self, content):
        self.content = content

class ProcessedThought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.String(500), nullable=False)
    pass_fail = db.Column(db.String(50), nullable=False)
    emotions = db.Column(db.String(500), nullable=True)
    sentiment_basic = db.Column(db.String(50), nullable=True)
    sentiment_score = db.Column(db.Integer)
    tldr = db.Column(db.String(500), nullable=True)
    time_stamp = db.Column(db.String(50), nullable=False)
    keywords = db.Column(db.String(500), nullable=True)

    def __init__(self, original_text, pass_fail, emotions, sentiment_basic, sentiment_score, tldr, time_stamp, keywords):
        self.original_text = original_text
        self.pass_fail = pass_fail
        self.emotions = json.dumps(emotions)  # Convert list to JSON string
        self.sentiment_basic = sentiment_basic
        self.sentiment_score = sentiment_score
        self.tldr = tldr
        self.time_stamp = time_stamp
        self.keywords = json.dumps(keywords)  # Convert list to JSON string

class FailedThought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.String(500), nullable=False)
    pass_fail = db.Column(db.String(50), nullable=False)
    emotions = db.Column(db.String(500), nullable=True)
    sentiment_basic = db.Column(db.String(50), nullable=True)
    sentiment_score = db.Column(db.Integer)
    tldr = db.Column(db.String(500), nullable=True)
    time_stamp = db.Column(db.String(50), nullable=False)
    keywords = db.Column(db.String(500), nullable=True)

    def __init__(self, original_text, pass_fail, emotions, sentiment_basic, sentiment_score, tldr, time_stamp, keywords):
        self.original_text = original_text
        self.pass_fail = pass_fail
        self.emotions = json.dumps(emotions)  # Convert list to JSON string
        self.sentiment_basic = sentiment_basic
        self.sentiment_score = sentiment_score
        self.tldr = tldr
        self.time_stamp = time_stamp
        self.keywords = json.dumps(keywords)  # Convert list to JSON string




class BadIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50), nullable=False, unique=True)
    time_stamp = db.Column(db.String(50), nullable=False)

    def __init__(self, ip):
        self.ip = ip
        self.time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')