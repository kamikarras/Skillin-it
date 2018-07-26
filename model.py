from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

    titles = Posting.query.all()
    titles = set(titles)

    for title in titles:
        job = Job(title=title.title)

        db.session.add(job)
        db.session.commit()


def sort_id2():
    """sort through the words of posting_id 2"""

    posting_2 = Posting.query.filter(Posting.title == "Software Engineer").all()
    all_words = []

    for posting in posting_2:
        words = posting.qualifications.lower().split()
        all_words.extend(words)

    main_words ={}
    with open('quiz_answers.txt') as filler:
        del_words = filler.read()
        for word in all_words:
            word = word.strip("-()/\,.:;*")
            if word not in del_words:
                if word in main_words:
                    main_words[word] += 1
                else:
                    main_words[word] = 1

    x = 1
    choice = ""
    for word in main_words:
        if main_words[word] > x:
            choice = word
            x = main_words[word]

    print(sorted(main_words))
    print(len(main_words))
    print(choice)
    print(x)

def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///postings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)




app = Flask(__name__)

if __name__ == "__main__":
    connect_to_db(app)
    # load_jobs()
    sort_id2()
    # db.create_all()
