from flask import Flask, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from model import Job, app, Posting, load_jobs, connect_to_db, Skill, User, UserSkill, db
from jinja2 import StrictUndefined
from sqlalchemy.orm import load_only, relationship




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
    name = request.form['name']
    password = request.form['password']
    new_user = User(name=name, email=email, password=password)

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
    user = User.query.filter_by(email=email).first()

    # check if this is a user and if the password matchs
    if not user:
        flash("no such user")
        return redirect('/login')

    if user.password != password:
        flash("Password does not match.")
        return redirect('/login')

    session["user_id"] = user.user_id

    flash('You are logged in')
    return redirect(f"/profile/{user.user_id}")


@app.route('/logout')
def logout():
    """logs the user out"""

    del session["user_id"]
    flash('log out succesful')
    return redirect('/')


@app.route('/profile/<int:user_id>', methods=['GET'])
def view_profile(user_id):
    """shows the user profile"""

    user_id = session.get("user_id")
    user = User.query.filter_by(user_id=user_id).first()
    name = user.name
    skills = user.user_skills
    if skills:
        # create a set to hold all of the jobs
        all_jobs = {}
        counter = 0
        # find the jobs for each skill
        for skill in skills:
            skill_label = Skill.query.filter_by(skill_id=skill.skill_id).first()
            # get the list of jobs through the relationship
            jobs = skill_label.jobs
            # use set comprehension to create a set of the job titles
            titles = set(job.job.title for job in jobs)
            # add the skills to the main set with set math intersection
            if counter < 1:
                all_jobs = titles
            else:
                all_jobs = all_jobs & titles

            counter += 1

    return render_template('profile.html',
                            user_skills=skills,
                            name=name,
                            user_id=user_id,
                            all_jobs=all_jobs)


@app.route('/profile/<int:user_id>', methods=['POST'])
def add_skill(user_id):
    """Adds or remove a skill for the user"""
    user_id = session.get("user_id")
    user = User.query.filter_by(user_id=user_id).first()
    name = user.name


    # get the user's skill from form
    skill_label = request.form['skill']
    # get the user from the session
    # find the skill in the skill table
    skill = Skill.query.filter_by(skill=skill_label).first()
    user_skills = user.user_skills

    # add skill to association table
    new_skill = (UserSkill(user_id=user_id, skill_id=skill.skill_id))
    db.session.add(new_skill)
    db.session.commit()
    flash("skill added")
    flash(skill.skill)

    return redirect(f"/profile/{user_id}")


@app.route('/profile/<int:user_id>/del', methods=['POST'])
def remove_skill(user_id):
    """removes a skill from the users skill list"""
    # retrieve user and the associated skill
    user_id = session.get("user_id")
    user = User.query.filter_by(user_id=user_id).first()

    delete_skill = request.form['delete_this']
    # specify the skill to be removed
    delete_id = Skill.query.filter_by(skill=delete_skill).first()
    delete = UserSkill.query.filter_by(skill_id=delete_id.skill_id, user_id=user_id).first()
    # del that skill from the user skills table
    db.session.delete(delete)
    db.session.commit()
    # redirect back to the profile page
    return redirect(f"/profile/{user.user_id}")


# @app.route('/profile/<int:user_id>', methods=['GET'])
# def show_potential jobs(user_skills):
#     # get the user 
#     user_id = session.get("user_id")
#     user = User.query.filter_by(user_id=user_id).first()
#     # get this users skills
#     skills = user.user_skills
#     # create a set to hold all of the jobs
#     all_jobs = {}
#     # find the jobs for each skill
#     for skill in skills:
#         # get the list of jobs through the relationship
#         jobs = skill.jobs
#         # user set comprehension to create a set of the job titles
#         titles = set(job.job.title for job in jobs)
#         # add the skills to the main set with set math intersection
#         all_jobs = all_jobs & titles




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
    skill = Skill.query.filter(Skill.skill==skill_search).first()
    jobs = skill.jobs


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
