import sqlite3
import csv

def get_all_rated_articles(conn):
    c = conn.cursor()
    c.execute('''
        SELECT article.id, title, score FROM article LEFT JOIN rating ON article.id = rating.article_id
        WHERE rating.id IS NOT NULL
    ''')
    return c.fetchall()

conn = sqlite3.connect('example.db')
rated = get_all_rated_articles(conn)

filename = "training_data.csv"

with open(filename, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['article_id', 'title', 'label'])
    writer.writerows(rated)

    print("Exported %d rated articles." % (len(rated)))

