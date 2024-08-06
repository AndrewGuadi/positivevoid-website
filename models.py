from extensions import db

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))

    def __init__(self, content):
        self.content = content