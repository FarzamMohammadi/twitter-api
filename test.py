import unittest
from main import app
import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)
conn.execute("DROP TABLE IF EXISTS users")
conn.execute("CREATE TABLE IF NOT EXISTS users (username, password)")
conn.commit()


class RegisterTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.post('/register/farzamTest/Farzam123@')

    def test_invalid_password(self):
        response = self.app.post('/register/farzamTest/farzam123')
        self.assertEqual(500, response.status_code)

    def test_existing_user(self):
        response = self.app.post('/register/farzamTest/Farzam123@')
        self.assertEqual(409, response.status_code)


class LoginTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.post('/register/farzamTest/Farzam123@')

    def test_invalid_credentials(self):
        response = self.app.post('/login/farzamTest/farzam123')
        self.assertEqual(401, response.status_code)

    def test_valid_credentials(self):
        response = self.app.post('/login/farzamTest/Farzam123@')
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
