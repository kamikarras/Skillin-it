from flask_sqlalchemy import SQLAlchemy


db =SQLAlchemy()


class Posting(db.Model):
    """Posting Model"""

    __tablename__ = "postings"

    posting_id = db.Column(db.Integer, primary_key=True, autincrement=True)
    company = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String, nullable=True)
    requirements = db.Column(db.String, nullable=True)
    qualifications = db.Column(db.String, nullable=False)

    def __repr__(self):
        """shows posting"""

        return f"""<Posting 
                    posting_id={self.posting_id}
                    company={self.company}
                    description={self.description}
                    requirements={self.requirements}
                    qualifications={self.requirements}"""

