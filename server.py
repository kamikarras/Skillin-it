from flask import (Flask, render_template, redirect, request, flash, session)
from flask_sqlalchemy import SQLAlchemy
from model import Job, app, Posting, load_jobs, connect_to_db
from jinja2 import StrictUndefined



db = SQLAlchemy()



app = Flask(__name__)

app.secret_key = "ABC"

@app.route('/job_skills', methods=["GET"])
def get_title():
    """displays skills form"""


    return render_template("job_skills.html")


@app.route('/job_skills', methods=["POST"])
def show_skills():
    """get skills and show them"""

    job_title = request.form.get('title')

    postings = Posting.query.filter(Posting.title == job_title).all()
    all_words = []

    for posting in postings:
        words = posting.qualifications.lower().split()
        all_words.extend(words)

    word_counts = {}
    with open('filler.txt') as filler:
        del_words = filler.read()
        for word in all_words:
            word = word.strip("-()/\,.:;* 1234567890")
            if word not in del_words:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

    skills = []

    for count in range(len(word_counts)):
        skill_count = 0
        for word in word_counts:
            if word_counts[word] > skill_count:
                skill_count = word_counts[word]
                skill = word
        skills.append(skill)
        del word_counts[skill]

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
