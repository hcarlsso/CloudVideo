from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

db = SQLAlchemy()

class Queue(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    url = db.Column(db.String(256), nullable=True)
    status = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Queue %s>' % self.uuid


manager = APIManager(flask_sqlalchemy_db=db)
manager.create_api(
    Queue,
    methods=['GET', 'POST', 'DELETE', 'PUT'],
    collection_name = 'queue',
    url_prefix='/v1')
