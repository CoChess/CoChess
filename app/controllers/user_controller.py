from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user_model import get_user_by_email, update_user_password, update_user_nickname
from app.utils.validators import validate_input_match

def change_password():
    if request.method == 'POST':
        email = request.form.get('email')
        current_password = request.form.get('password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        if not validate_input_match(new_password, confirm_new_password, "As senhas não coincidem."):
            return redirect(url_for('change_password'))

        user = get_user_by_email(email)
        if not user:
            flash("Usuário não encontrado.", "error")
            return redirect(url_for('change_password'))

        if not check_password_hash(user['password'], current_password):
            flash("Senha atual incorreta.", "error")
            return redirect(url_for('change_password'))

        hashed_password = generate_password_hash(new_password)
        update_user_password(email, hashed_password)
        flash("Senha alterada com sucesso!", "success")
        return redirect(url_for('home'))

    return render_template('change_password.html')

def change_nickname():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        nickname = request.form.get('nickname')

        if not validate_input_match(password, confirm_password, "As senhas não coincidem."):
            return redirect(url_for('change_nickname'))

        user = get_user_by_email(email)
        if not user or not check_password_hash(user['password'], password):
            flash("Senha incorreta.", "error")
            return redirect(url_for('change_nickname'))

        if not (5 <= len(nickname) <= 50):
            flash("Nickname deve ter entre 5 e 50 caracteres.", "error")
            return redirect(url_for('change_nickname'))

        update_user_nickname(email, nickname)
        flash("Nickname alterado com sucesso!", "success")
        return redirect(url_for('lobby'))

    return render_template('change_nickname.html')

def lobby():
    return render_template('lobby.html')

def train():
    return render_template('train.html')

def history():
    return render_template('history.html')

def game():
    return render_template('game.html')

