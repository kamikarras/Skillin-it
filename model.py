from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only

db = SQLAlchemy()


class Posting(db.Model):
    """Posting Model"""

    __tablename__ = "postings"

    posting_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company = db.Column(db.String, nullable=True)
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
                    qualifications={self.requirements}>"""


class Job(db.Model):
    """Job Model"""

    __tablename__ = "jobs"

    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)

    def __repr__(self):
        """shows job"""

        return f"<Job job_id={self.job_id} title={self.title}>"


def load_jobs():
    """load jobs table from data in postings dataset"""

    Job.query.delete()

    titles = db.session.query(Posting.title).all()
    titles = set(titles)
    titles = list(titles)

    for title in titles:
        job = Job(title=title.title)

        db.session.add(job)
        db.session.commit()


class Skill(db.Model):
    """Skills Model"""

    __tablename__ = "skills"

    skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill = db.Column(db.String, nullable=False)

    def __repr__(self):
        """shows skill"""

        return f"<Skill skill_id={self.skill_id} skill={self.skill}>"


def load_skills():
    """load JobSKills table from postings"""

    Skill.query.delete()

    # get all the qualifications text from postings
    postings = db.session.query(Posting.qualifications).all()
    # combine qualifications into a list
    all_skills = []
    with open('filler.txt') as filler:
        del_words = filler.read()
        for post in postings:
            words = post.qualifications.lower().split()
        # iterate through a list of those skills
            for word in words:
                word = word.strip("-()/\,.:;* 1234567890")
                # check to see if that word isn't in our filler document
                # if not, add it to the table
                if word not in del_words and word not in all_skills:
                    all_skills.append(word)
                    skill = Skill(skill=word)
                    db.session.add(skill)
                    db.session.commit()



def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///postings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)




app = Flask(__name__)

if __name__ == "__main__":
    connect_to_db(app)
    load_jobs()
    load_skills()
    db.create_all()
