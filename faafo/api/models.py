from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Queue(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    url = db.Column(db.String(256), nullable=True)
    status = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Queue %s>' % self.uuid
