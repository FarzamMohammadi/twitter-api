import unittest
from main import app
import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)
conn.execute("DROP TABLE users")
conn.execute("CREATE TABLE IF NOT EXISTS users (username, password)")
conn.commit()


# 'step' added to functions names to ensure test runs in desired order
class RegisterTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def step1_test_registration_invalid_password(self):
        response = self.app.post('/register/farzamMoTest/farzam123', headers={"Content-Type": "application/json"})
        self.assertEqual(500, response.status_code)

    def step2_test_registration_valid_password(self):
        response = self.app.post('/register/farzamMoTest/Farzam123@', headers={"Content-Type": "application/json"})
        self.assertEqual(201, response.status_code)

    def step3_test_existing_user(self):
        response = self.app.post('/register/farzamMoTest/Farzam123@', headers={"Content-Type": "application/json"})
        self.assertEqual(409, response.status_code)


if __name__ == '__main__':
    unittest.main()
