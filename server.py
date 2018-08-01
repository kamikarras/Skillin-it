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

    skill = request.form.get('skill')

    return render_template("skill_search.html")


@app.route('/job_skills', methods=["GET"])
def get_title():
    """displays skills form"""


    return render_template("job_skills.html")


@app.route('/job_skills', methods=["POST"])
def show_skills():
    """get skills and show them"""

    job_title = request.form.get('title')

    job = Job.query.filter(Job.title == job_title).one()
    skill_ids = job.skills
    skills = []
    for skill_id in skill_ids:
        skill_name = db.session.query(Skill.skill).filter(Skill.skill_id == skill_id.skill_id).all()
        skill_count = skill_id.count
        skills.append([skill_count, skill_name[0][0]])

    skills = sorted(skills, reverse=True)

    # all_words = []

    # for skills in job.skills:
    #     words = skills.qualifications.lower().split()
    #     all_words.extend(words)

    # word_counts = {}
    # with open('filler.txt') as filler:
    #     del_words = set(filler.read())
    #     for word in all_words:
    #         word = word.strip("-()/\,.:;* 1234567890")
    #         if word not in del_words:
    #             if word in word_counts:
    #                 word_counts[word] += 1
    #             else:
    #                 word_counts[word] = 1

    # skills = []

    # for count in range(len(word_counts)):
    #     skill_count = 0
    #     for word in word_counts:
    #         if word_counts[word] > skill_count:
    #             skill_count = word_counts[word]
    #             skill = word
    #     skills.append(skill)
    #     del word_counts[skill]

    return render_template("job_skills.html",
                            skills=skills,
                            job_title=job_title)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)


    app.run(port=5000, host='0.0.0.0')
