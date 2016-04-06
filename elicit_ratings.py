import sqlite3

def insert_rating(conn, score, article_id):
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO rating (score, article_id) VALUES (?, ?)''', (score, article_id))
    conn.commit()
    c.close()

def get_all_unrated_articles(conn):
    c = conn.cursor()
    c.execute('''
        SELECT * FROM article LEFT JOIN rating ON article.id = rating.article_id
        WHERE rating.id IS NULL
    ''')
    return c.fetchall()

def get_all_rated_articles(conn):
    c = conn.cursor()
    c.execute('''
        SELECT article.id, title, score FROM article LEFT JOIN rating ON article.id = rating.article_id
        WHERE rating.id IS NOT NULL
    ''')
    return c.fetchall()

conn = sqlite3.connect('example.db')
unrated = get_all_unrated_articles(conn)
rated = get_all_rated_articles(conn)

print("%d unrated articles, %d rated articles." % (len(unrated), len(rated)))
print("Type 'q' to quit, 'x' to skip, '1' to classify into positive class, and anything else to classify into negative"
      " class.")

for article in unrated:
    article_id = article[0]
    article_title = article[1]
    rating = input(article_title + ": ").strip()

    if rating == 'q':
        break
    elif rating == 'x': # Don't want to rate
        continue
    elif rating == '1':
        score = 1
    else:
        score = 0

    insert_rating(conn, score, article_id)

print("Done.")

conn.close()