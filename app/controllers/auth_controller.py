from flask import render_template, request, redirect, url_for, flash, current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.dao.user_dao import UserDAO
from app.utils.validators import validate_input_match, is_email_registered

def home():
    return render_template('home.html')

def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

def forget_password():
    if request.method == 'POST':
        email = request.form.get('email')
        #current_password = request.form.get('password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        if not validate_input_match(new_password, confirm_new_password, "Passwords don't match!"):
            return redirect(url_for('reset_password_authenticated'))

        user = UserDAO.get_by_email(email)
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('reset_password_authenticated'))

        #if not check_password_hash(user.password, current_password):
        #    flash("Wrong current password.", "error")
        #    return redirect(url_for('reset_password_authenticated'))

        hashed_password = generate_password_hash(new_password)
        UserDAO.update_password(email, hashed_password)
        flash("Password updated!", "success")
        return redirect(url_for('home'))

    return render_template('forget_password.html')


def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = UserDAO.get_by_email(email)

        if user and check_password_hash(user.password, password):
            session['user_email'] = user.email
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
