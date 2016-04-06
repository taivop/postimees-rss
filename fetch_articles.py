import feedparser
import sqlite3
import hashlib
import time
import logging

def md5(s):
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()

def setup_db(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS article (id integer primary key autoincrement,
                 title text, hash text, summary text, link text, published datetime, feed_id text,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, UNIQUE(title, hash))''')
    c.execute('''CREATE TABLE IF NOT EXISTS rating (id integer primary key autoincrement,
                 score integer, article_id integer, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY(article_id) REFERENCES articles(id))''')
    conn.commit()

def insert_article(conn, title, summary, link, published, feed_id):
    c = conn.cursor()
    hash = md5(title)
    published_string = time.strftime("%Y-%m-%d %H:%M:%S", a.published_parsed)
    c.execute('''INSERT OR IGNORE INTO article (title, hash, summary, link, published, feed_id)
                 VALUES (?, ?, ?, ?, ?, ?)''', (title, hash, summary, link, published_string, feed_id))
    conn.commit()
    c.close()

def get_all_articles(conn):
    c = conn.cursor()
    c.execute('''SELECT * FROM article ORDER BY hash''')
    return c.fetchall()

def get_all_ratings(conn):
    c = conn.cursor()
    c.execute('''SELECT * FROM rating''')
    return c.fetchall()

LOG_FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.DEBUG, filename='logs/fetch_articles.log',
                                filemode='w', format=LOG_FORMAT)

conn = sqlite3.connect('example.db')
feed = feedparser.parse('http://www.postimees.ee/rss/')
setup_db(conn)

logging.info("Fetching new articles from RSS.")

for a in feed.entries:
    insert_article(conn, a.title, a.summary, a.link, a.published_parsed, a.id)

#print(get_all_articles(conn))
#print(get_all_ratings(conn))


conn.close()