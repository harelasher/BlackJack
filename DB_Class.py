# Import module
import sqlite3
import datetime
import random

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
            pfp_pic INTEGER, 
            last_seen TIMESTAMP,
            is_online BOOL)""")
        self.conn.commit()

    def create_user(self, username, password):
        if 3 <= len(username) < 10 and 3 <= len(password) < 10:
            self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if self.cursor.fetchone() is None:
                # Randomly select a profile picture between four options
                pfp_pic = random.randint(0, 3)
                self.cursor.execute("""INSERT INTO users (username, password, score, highscore, pfp_pic, last_seen, is_online)
                                    VALUES (?,?,?,?,?,?,?)""",
                                    (username, password, 100000, 100000, pfp_pic, datetime.datetime.now(), 1))
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

    def login_check(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=? and password=? and is_online=0", (username, password))
        user = self.cursor.fetchone()
        if user:
            self.cursor.execute("UPDATE users SET is_online=1 WHERE username=?", (username,))
            self.conn.commit()
            return True, f"{username} logged in"
        else:
            return False, f"The username is already online or the username and password combination is not correct"

    def logout(self, username):
        self.cursor.execute("UPDATE users SET is_online=0 WHERE username=?", (username,))
        self.conn.commit()
        return True

    def get_user_info(self, username):
        self.cursor.execute(
            "SELECT id, username, score, highscore, pfp_pic, last_seen, is_online FROM users WHERE username=?",
            (username,))
        user_info = self.cursor.fetchone()
        if user_info:
            return user_info
        else:
            return False

    def make_all_users_offline(self):
        self.cursor.execute("UPDATE users SET is_online=0")
        self.conn.commit()

    def check_date(self):
        pass

    def __del__(self):
        self.conn.close()


#######################################################################################################################
#######################################################################################################################
