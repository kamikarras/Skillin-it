from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only, relationship

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
    JobSkillCount.query.delete()
    Job.query.delete()

    titles = db.session.query(Posting.title).all()
    titles = set(titles)

    for title in titles:
        title = title.lower()
        job = Job(title=title[0])

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


class JobSkillCount(db.Model):
    """Job Skill Count model"""

    __tablename__ = "jobskillcounts"

    skill_count_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.job_id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.skill_id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    job = db.relationship('Job', backref=db.backref('skills', order_by=skill_count_id))
    skill = db.relationship('Skill', backref=db.backref('jobs', order_by=skill_count_id))


def load_job_skill_counts():
    """load the counts for each skill a job has into a relationship table"""


    jobs = Job.query.all()
    with open('filler.txt') as filler:
        del_words = filler.read()

    #for loop going through each job title in the jobs table
    for job in jobs:
        all_words = []
        word_counts = {}
        # all the related postings in the postings table
        postings = db.session.query(Posting.qualifications).filter(Posting.title == job.title).all()
        # combine all text for job
        for posting in postings:
            words = posting.qualifications.lower().split()
            all_words.extend(words)
        #word counts get added to a dictionary
        for word in all_words:
            word = word.strip("-()/\,.:;* 1234567890")
            if word not in del_words:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1
        print("word_counting is done\n\n\n")
        print(word_counts)
        for word in word_counts:
            print(word)
            skill = db.session.query(Skill.skill_id).filter(Skill.skill == word)
            job_skill = JobSkillCount(job_id=job.job_id,
                                      skill_id=skill,
                                      count=word_counts[word])
            db.session.add(job_skill)
            db.session.commit()

        # when done with each title, words counts get added to the table with
        # the reference id from the skills table.





class User(db.Model):
    """User table"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


class UserSkill(db.Model):
    """user skills table"""

    __tablename__ = "user_skills"

    user_skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.skill_id'), index=True)
    in_progress = db.Column(db.Boolean)

    skill = db.relationship('Skill',
                            backref=db.backref('user_skills'), order_by=skill_id)
    user = db.relationship('User',
                            backref=db.backref('user_skills'), order_by=user_id)


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
    # load_skills()
    # load_job_skill_counts()
    db.create_all()
