import json
import unittest
from main import app
import sqlite3
import random, string

conn = sqlite3.connect('database.db', check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS users (username, password)")
conn.commit()


def random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class RegisterTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        payload = json.dumps({
            "username": "farzamTest",
            "password": "Farzam123@"
        })
        self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

    def test_invalid_password(self):
        payload = json.dumps({
            "username": "farzamTest",
            "password": "farzam123"
        })
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(500, response.status_code)

    def test_existing_user(self):
        payload = json.dumps({
            "username": "farzamTest",
            "password": "WrongPassword123@"
        })
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(409, response.status_code)


class LoginTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        payload = json.dumps({
            "username": "farzamTest",
            "password": "Farzam123@"
        })
        self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

    def test_invalid_credentials(self):
        payload = json.dumps({
            "username": "farzamTest",
            "password": "WrongPassword123@"
        })
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(401, response.status_code)

    def test_valid_credentials(self):
        payload = json.dumps({
            "username": "farzamTest",
            "password": "Farzam123@"
        })
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(200, response.status_code)


class ChatTestCases(unittest.TestCase):
    def setUp(self):
        # First log in
        self.app = app.test_client()
        payload = json.dumps({
            "username": "farzam",
            "password": "Farzam123@"
        })
        # Then send message to user 'farzamTest'
        self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        payload = json.dumps({
            "message": "This message is for testing."
        })
        self.app.post('/chat/farzamTest', headers={"Content-Type": "application/json"}, data=payload)

    def test_getting_user_messages(self):
        # Log back into test user
        payload = json.dumps({
            "username": "farzamTest",
            "password": "Farzam123@"
        })
        # Then see messages sent to 'farzamTest'
        self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        # Gets messages for test user where the sender was 'farzam'
        response = self.app.get('/chat/farzam')
        self.assertEqual(200, response.status_code)

    def test_no_messages(self):
        # Gets messages for test user where the sender was 'billbob' who has never sent any messages
        response = self.app.get('/chat/billybob')
        self.assertEqual(401, response.status_code)


class TweetTestCases(unittest.TestCase):
    def setUp(self):
        # First log in
        self.app = app.test_client()
        payload = json.dumps({
            "username": "farzamTest",
            "password": "Farzam123@"
        })
        self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        conn.execute("CREATE TABLE IF NOT EXISTS users (username, password)")

    def test_sending(self):
        payload = json.dumps({
            "tweet": "This is my test tweet."
        })
        response = self.app.post('/tweet', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(200, response.status_code)

    def test_tweet_length(self):
        payload = json.dumps({
            "tweet": random_word(256)

        })
        response = self.app.post('/tweet', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(401, response.status_code)

    def test_updating(self):
        # Get the id from the tweet we just created
        cursor = conn.execute('SELECT max(id) FROM tweets')
        last_id = cursor.fetchone()[0]
        print(last_id)
        payload = json.dumps({
            "id": last_id,
            "tweet": "This is my updated test tweet."
        })
        response = self.app.put('/tweet', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(200, response.status_code)

    def test_deletion(self):
        # Get the id from the tweet we just created/updated
        cursor = conn.execute('SELECT max(id) FROM tweets')
        last_id = cursor.fetchone()[0]
        payload = json.dumps({
            "id": last_id,
        })
        response = self.app.delete('/tweet', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
