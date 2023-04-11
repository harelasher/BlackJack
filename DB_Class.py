# Import module
import sqlite3
import datetime
import random
from t import encrypt, decrypt
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
            is_online BOOL,
            WinLossPush TEXT)""")
        self.conn.commit()

    def create_user(self, username, password):
        if 3 <= len(username) < 10 and 3 <= len(password) < 10:
            self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if self.cursor.fetchone() is None:
                # Randomly select a profile picture between four options
                pfp_pic = random.randint(0, 3)
                self.cursor.execute("""INSERT INTO users (username, password, score, highscore, pfp_pic, last_seen, is_online, WinLossPush)
                                    VALUES (?,?,?,?,?,?,?,?)""",
                                    (username, encrypt(password), 100000, 100000, pfp_pic, datetime.datetime.now(), 1, "0/0/0"))
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
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if self.cursor.fetchone() is None or not (score.isdigit() or (score.startswith('-') and score[1:].isdigit())):
            return False
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
        self.cursor.execute("SELECT * FROM users WHERE username = ? and is_online=0", (username,))
        if self.cursor.fetchone() is None:
            return False, "username already logged in or non existent"
        self.cursor.execute("SELECT password FROM users WHERE username=? and is_online=0", (username, ))
        password_enc = self.cursor.fetchone()[0]
        if decrypt(password_enc).decode() == password:
            self.cursor.execute("UPDATE users SET is_online=1 WHERE username=?", (username,))
            self.conn.commit()
            return True, f"{username} logged in"
        else:
            return False, f"the username and password combination is not correct"

    def logout(self, username):
        self.cursor.execute("UPDATE users SET is_online=0 WHERE username=?", (username,))
        self.conn.commit()
        return True

    def get_user_info(self, username):
        self.cursor.execute(
            "SELECT id, username, score, highscore, pfp_pic, last_seen, is_online, WinLossPush FROM users WHERE username=?",
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

    def change_pfp_pic(self, username, pfp_pic):
        self.cursor.execute("UPDATE users SET pfp_pic=? WHERE username=?", (pfp_pic, username))
        self.conn.commit()
        return True

    def __del__(self):
        self.conn.close()

    def get_top_users(self):
        self.cursor.execute("SELECT username, pfp_pic, highscore FROM users ORDER BY highscore DESC LIMIT 5")
        top_users = self.cursor.fetchall()
        return top_users

    def update_win_loss_push(self, username, result):
        self.cursor.execute("SELECT WinLossPush FROM users WHERE username=?", (username,))
        win_loss_push_str = self.cursor.fetchone()[0]
        win_loss_push = list(map(int, win_loss_push_str.split("/")))
        if result == "win":
            win_loss_push[0] += 1
        elif result == "loss":
            win_loss_push[1] += 1
        else:
            win_loss_push[2] += 1
        win_loss_push_str = "/".join(map(str, win_loss_push))
        self.cursor.execute("UPDATE users SET WinLossPush=? WHERE username=?", (win_loss_push_str, username))
        self.conn.commit()