# Import module
import sqlite3
import datetime

DatabasePath = 'blackjack.db'


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DatabasePath, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            username TEXT, 
            password TEXT, 
            score INTEGER, 
            highscore INTEGER, 
            last_seen TIMESTAMP)""")
        self.conn.commit()

    def create_user(self, username, password):  # register the user
        if 3 <= len(username) < 10 and 3 <= len(password) < 10:
            self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if self.cursor.fetchone() is None:
                self.cursor.execute("""INSERT INTO users (username, password, score, highscore,last_seen)
                                    VALUES (?,?,?,?,?)""",
                                    (username, password, 100000, 100000, datetime.datetime.now()))
                self.conn.commit()
                return True, ""
            else:
                return False, "This Username Is Already Taken"
        else:
            return False, "Username And Password Length Should Be At Least 3 Characters And Less Than 10"

    def delete_user(self, username):
        self.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        self.conn.commit()
        return True

    def update_user_score(self, username, score):
        self.cursor.execute("UPDATE users SET score=score+? WHERE username=?", (score, username))
        self.conn.commit()
        self.update_user_highscore(username)
        return True

    def update_user_highscore(self, username):
        self.cursor.execute("SELECT score FROM users WHERE username=?", (username,))
        current_score = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT highscore FROM users WHERE username=?", (username,))
        current_highscore = self.cursor.fetchone()[0]
        if current_score > current_highscore:
            self.cursor.execute("UPDATE users SET highscore=? WHERE username=?", (current_score, username))
            self.conn.commit()

    def login_check(self, username, password):  # login for user
        self.cursor.execute("SELECT * FROM users WHERE username=? and password=?", (username, password))
        user = self.cursor.fetchone()
        if user:
            return True, f"{username} logged in"
        else:
            return False, f"The Username Or Password Is Not Correct"

    def check_date(self):
        pass

    def __del__(self):
        self.conn.close()


#######################################################################################################################
'''
This code does not consider security measures for login,
such as salting and hashing passwords,
which is a must for any production system.
'''
'''
add a protocol that goes over tcp. he builds and parses the messages that sent to the socket.
(encrypted too)
'''
#######################################################################################################################
'''
add is_online to user Database
add picture to user Database
'''
#######################################################################################################################
'''
add login and register error message - username and password are not in the right letters range(3-9)
username is already taken
for login checks if the username checks out for the password
'''
#######################################################################################################################