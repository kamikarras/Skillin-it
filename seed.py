"""Utility file to seed postings database from posting csv file"""

from model import Posting
from model import connect_to_db, db
from model import app
import csv


def load_postings():
    """load postings from job posting database."""

    with open('data job posts.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            title, company = row[2:4]
            description, requirements, qualifications = row[11:14]

            posting = Posting(title=title,
                              company=company,
                              description=description,
                              requirements=requirements,
                              qualifications=qualifications)

            db.session.add(posting)


    db.session.commit()



connect_to_db(app)
load_postings()
