from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import get_user_by_email, insert_user
from app.utils.validators import validate_input_match, is_email_registered

def home():
    return render_template('home.html')

def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)

        if user and check_password_hash(user['password'], password):
            flash(f"Bem-vindo de volta, {user['username']}!", "success")
            return redirect(url_for('lobby'))

        flash("Credenciais inválidas. Tente novamente!", "error")

    return render_template('login.html')

def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        confirm_email = request.form.get('confirm_email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not validate_input_match(email, confirm_email, "Os e-mails não coincidem.") or \
           not validate_input_match(password, confirm_password, "As senhas não coincidem.") or \
           is_email_registered(email):
            return redirect(url_for('create_account'))

        hashed_password = generate_password_hash(password)
        user_data = {"username": username, "email": email, "password": hashed_password}
        insert_user(user_data)

        flash("Conta criada com sucesso!", "success")
        return redirect(url_for('home'))

    return render_template('create_account.html')
