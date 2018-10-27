from app import db
from hashutils import make_pw_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    pw_hash = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, username, password, email=None):
        self.username = username
        self.pw_hash = make_pw_hash(password)
        self.email = email

