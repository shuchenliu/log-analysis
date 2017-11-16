#! /usr/bin/env python3

import psycopg2

# database
DB_NAME = "news"

# queries
most_viewed_art_query = """SELECT title, count
                           FROM ViewStats
                           ORDER BY count desc limit 3;"""

most_popular_authors = """SELECT authors.name, sum(ViewStats.count)
                          FROM authors JOIN ViewStats
                          ON authors.id = ViewStats.author
                          GROUP BY authors.name
                          ORDER BY sum(ViewStats.count) DESC;"""

error_rate_over = """SELECT date, errorrate
                     FROM ErrorRate
                     WHERE errorrate > 1
                     GROUP BY date, errorrate
                     ORDER BY errorrate DESC"""

# questions:
q1 = """1. What are the most popular 3articles of all time?\n"""
q2 = """2. Who are the most popular article authors of all time?\n"""
q3 = """3. On which days did more than 1% of requests lead to errors?\n"""


# Query Method

def fetchResult(query):
    try:
        db = psycopg2.connect(database=DB_NAME)
        cursor = db.cursor()
    except IOError:
        print("Error connecting the Database. Try again later.")
        return
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result

# Print Methods


def printViewResult(question, result):
    actualPrint(question, result, "views")


def printErrorResult(question, result):
    actualPrint(question, result, "% error")


def actualPrint(question, result, unit):
    print(question)
    for r in result:
        print("\t + {} --- {} {}".format(r[0], r[1], unit))

    print()

# Issue queries


article_result = fetchResult(most_viewed_art_query)
printViewResult(q1, article_result)


author_result = fetchResult(most_popular_authors)
printViewResult(q2, author_result)


error_result = fetchResult(error_rate_over)
printErrorResult(q3, error_result)
