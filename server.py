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


@app.route('/register', methods=["GET"])
def show_registration():
    """shows the registration form"""

    return render_template("register.html")


@app.route('/register', methods=["POST"])
def register_user():
    """adds user to database"""

    # get email and password for new user from form
    email = request.form['email']
    password = request.form['password']
    new_user = User(email=email, password=password)

    # add the user to the user database
    db.session.add(new_user)
    db.session.commit()

    return redirect("/")


@app.route('/login', methods=['GET'])
def login_form():
    """shows the login form"""

    return render_template('login_form.html')

@app.route('/login', methods=['POST'])
def login_process():

    # get user details from form
    email = request.form['email']
    password = request.form['password']

    # query to get user from database
    user = User.query.filter(email=email).first()

    # check if this is a user and if the password matchs
    if not user:
        flash("no such user")
        return redirect('/login')

    if user.password != password:
        flash("Password does not match.")
        return redirect('/login')

    session["user_id"] = user.user_id

    flash('You are logged in')
    return redirect('/')


@app.route('/logout')
def logout():
    """logs the user out"""

    del session[user_id]
    flash('log out succesful')
    return redirect('/')

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
    # skill_search2 = request.form.get('another_skill')
    skill = Skill.query.filter(Skill.skill==skill_search).one()
    job_ids = skill.jobs
    # if skill_search2:
    #     skill2 = Skill.query.filter(Skill.skill==skill_search2).one()
    #     job_ids2 = skill2.jobs

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
