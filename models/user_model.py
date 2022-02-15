import sqlite3
import jwt

DB_PATH = './models/my_data.db'

class UserModel:
    def __init__(self, firstName, lastName, username, password, email):
        self.firstname = firstName
        self.lastName = lastName
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def add_user(cls, firstName, lastName, username, password, email):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            insert_command = "INSERT INTO Users (firstName, lastName, username, password, email) VALUES (?,?,?,?,?);"
            try:
                c.execute(insert_command, (firstName, lastName, username, password, email))
            except Exception:
                return None
            else:
                return cls(firstName, lastName, username, password, email)

    @classmethod
    def find_by_username(cls, username):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            query_command = "SELECT * FROM Users WHERE username=?"
            c.execute(query_command, (username,))
            rs = c.fetchone()
            if rs:
                instance = cls(*rs[1:])
                instance.id = rs[0]
                return instance
            else:
                return None

    @classmethod
    def find_by_id(cls, _id):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            query_command = "SELECT * FROM Users WHERE id=?"
            c.execute(query_command, (_id,))
            rs = c.fetchone()
            if rs:
                instance = cls(*rs[1:])
                instance.id = rs[0]
                return instance
            else:
                return None

    @staticmethod
    def id_decode(token):
        return jwt.decode(token, options={"verify_signature": False})['identity']