import csv
# from pprint import pprint

rows = []

with open('data job posts.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        rows.append(row)
