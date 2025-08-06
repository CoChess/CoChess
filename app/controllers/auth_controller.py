from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.dao.user_dao import UserDAO
from app.utils.validators import validate_input_match, is_email_registered

def home():
    return render_template('home.html')

def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = UserDAO.get_by_email(email)

        if user and check_password_hash(user.password, password):
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for('lobby'))

        flash("Invalid Input. Try Again!", "error")

    return render_template('login.html')

def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        confirm_email = request.form.get('confirm_email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not validate_input_match(email, confirm_email, "E-mails don't match.") or \
           not validate_input_match(password, confirm_password, "Passwords don't match.") or \
           is_email_registered(email):
            return redirect(url_for('create_account'))

        hashed_password = generate_password_hash(password)
        user_data = {"username": username, "email": email, "password": hashed_password}
        UserDAO.insert(user_data)

        flash("Account created!", "success")
        return redirect(url_for('home'))

    return render_template('create_account.html')
