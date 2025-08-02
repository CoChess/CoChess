from flask import current_app

def get_user_by_email(email):
    db = current_app.get_db()
    return db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

def insert_user(user_data):
    db = current_app.get_db()
    db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
               (user_data["username"], user_data["email"], user_data["password"]))
    db.commit()

def update_user_password(email, new_password):
    db = current_app.get_db()
    db.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
    db.commit()

def update_user_nickname(email, new_nickname):
    db = current_app.get_db()
    db.execute("UPDATE users SET username = ? WHERE email = ?", (new_nickname, email))
    db.commit()

