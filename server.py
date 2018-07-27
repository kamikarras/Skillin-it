from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import Job
from model import Posting
from model import load_jobs
from model import app


db = SQLAlchemy()

def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///postings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def sort_id2():
    """sort through the words of posting_id 2"""

    posting_2 = Posting.query.filter_by(posting_id=2).one()




if __name__ == "__main__":
    connect_to_db(app)
    sort_id2()
