import datetime
import logging
from flask import session
import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)


# DB users table creation
def create_tweet_table():
    # Drops table if it already exists
    # conn.execute("DROP TABLE IF EXISTS tweets")
    conn.execute("CREATE TABLE IF NOT EXISTS tweets (id INTEGER PRIMARY KEY, username, tweet, date, like, retweet)")
    conn.commit()


def create_tweet(data):
    create_tweet_table()
    username = session.get('username')
    tweet = data['tweet']
    params = (username, tweet, datetime.datetime.now(), None, None)

    try:
        if username:
            conn.execute("""INSERT INTO tweets (username, tweet, date, like, retweet)
                                                   VALUES(?,?,?,?,?)""", params)
            conn.commit()
            return True

    except Exception as e:
        logging.exception(e)
        return False


def get_user_tweets():
    username = session.get('username')
    try:
        if username:
            user_tweets = conn.execute("SELECT * FROM tweets WHERE username=?", (username,))
            return user_tweets.fetchall()
    except Exception as e:
        logging.exception(e)
        return None


def update_tweet(data):
    try:
        tweet_id = data['id']
        tweet = data['tweet']
        username = session.get('username')
        if username:
            params = (tweet, tweet_id, username)
            conn.execute("UPDATE tweets SET tweet=? WHERE id=? AND username=?", params)
            conn.commit()
            return True
    except Exception as e:
        logging.exception(e)
        return False


def delete_tweet(data):
    tweet_id = data['id']
    username = session.get('username')
    params = (tweet_id, username)
    try:
        if username:
            conn.execute("DELETE FROM tweets WHERE id=? AND username=?", params)
            conn.commit()
            return True

    except Exception as e:
        logging.exception(e)
        return False
