from flask import (Flask, render_template, redirect, request, flash, session)
from flask_sqlalchemy import SQLAlchemy
from model import Job, app, Posting, load_jobs, connect_to_db, Skill
from jinja2 import StrictUndefined


db = SQLAlchemy()



app = Flask(__name__)

app.secret_key = "ABC"

@app.route('/')
def show_home():
    """shows the hompage"""

    return render_template("homepage.html")


@app.route('/all_jobs')
def job_list():
    """displays a list of all jobs"""

    jobs = Job.query.all()

    return render_template("all_jobs.html", jobs=jobs)


@app.route('/skill_search', methods=["GET"])
def get_skill():
    """displays skill seach form"""

    return render_template("skill_search.html")


@app.route('/skill_search', methods=["POST"])
def show_jobs():
    """displays skill seach form"""

    skill_search = request.form.get('skill_search')
    skill_search2 = request.form.get('another_skill')
    skill = Skill.query.filter(Skill.skill==skill_search).one()
    job_ids = skill.jobs
    jobs = []

    for job_id in job_ids:
        job_title = db.session.query(Job.title).filter(Job.job_id == job_id.job_id).one()
        jobs.append(job_title[0])

    return render_template("skill_search.html",
                            jobs=jobs,
                            skill_search=skill_search)


@app.route('/job_skills', methods=["GET"])
def get_title():
    """displays skills form"""


    return render_template("job_skills.html")


@app.route('/job_skills', methods=["POST"])
def show_skills():
    """get skills and show them"""

    job_title = request.form.get('title')
    length = request.form.get('list_total')
    length = int(length)

    job = Job.query.filter(Job.title == job_title).one()
    skill_ids = job.skills
    skills = []
    for skill_id in skill_ids:
        skill_name = db.session.query(Skill.skill).filter(Skill.skill_id == skill_id.skill_id).all()
        skill_count = skill_id.count
        skills.append([skill_count, skill_name[0][0]])

    skills = sorted(skills, reverse=True)[:length]


    return render_template("job_skills.html",
                            skills=skills,
                            job_title=job_title,
                            length=length)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)


    app.run(port=5000, host='0.0.0.0')
