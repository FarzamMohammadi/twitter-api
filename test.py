import unittest
from main import app
import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)
conn.execute("DROP TABLE users")
conn.execute("CREATE TABLE IF NOT EXISTS users (username, password)")
conn.commit()


# 'step' added to functions names to ensure test runs in desired order
class Step1RegisterTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_step1_registration_invalid_password(self):
        response = self.app.post('/register/farzamMoTest/farzam123')
        self.assertEqual(500, response.status_code)

    def test_step2_registration_valid_password(self):
        response = self.app.post('/register/farzamMoTest/Farzam123@')
        self.assertEqual(201, response.status_code)

    def test_step3_existing_user(self):
        response = self.app.post('/register/farzamMoTest/Farzam123@')
        self.assertEqual(409, response.status_code)


class Step2LoginTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_step4_invalid_credentials(self):
        response = self.app.post('/login/farzamMoTest/farzam123')
        self.assertEqual(401, response.status_code)

    def test_step5_valid_credentials(self):
        response = self.app.post('/login/farzamMoTest/Farzam123@')
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
