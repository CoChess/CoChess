from flask import current_app
from app.models.user_model import User

class UserDAO:
    @staticmethod
    def get_by_email(email):
        db = current_app.get_db()
        row = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if row:
            return User(row["id"], row["username"], row["email"], row["password"])
        return None

    @staticmethod
    def insert(user_data):
        db = current_app.get_db()
        cursor = db.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (user_data["username"], user_data["email"], user_data["password"])
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_password(email, new_password):
        db = current_app.get_db()
        cursor = db.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_nickname(email, new_nickname):
        db = current_app.get_db()
        cursor = db.execute("UPDATE users SET username = ? WHERE email = ?", (new_nickname, email))
        db.commit()
        return cursor.lastrowid
