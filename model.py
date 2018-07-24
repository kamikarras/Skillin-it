from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Posting(db.Model):
    """Posting Model"""

    __tablename__ = "postings"

    posting_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company = db.Column(db.String(64), nullable=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    requirements = db.Column(db.String, nullable=True)
    qualifications = db.Column(db.String, nullable=False)

    def __repr__(self):
        """shows posting"""

        return f"""<Posting
                    posting_id={self.posting_id}
                    company={self.company}
                    title={self.title}
                    description={self.description}
                    requirements={self.requirements}
                    qualifications={self.requirements}"""


def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///postings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

app = Flask(__name__)

if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()
