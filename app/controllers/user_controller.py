from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from app.dao.user_dao import UserDAO
from app.dao.game_dao import GameDAO
from app.dao.move_dao import MoveDAO
from app.utils.validators import validate_input_match

# =========================
# Usuário
# =========================

def change_password():
    if 'user_email' not in session:
        flash("You must be logged in to change your password.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form.get('password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        if not validate_input_match(new_password, confirm_new_password, "Passwords don't match!"):
            return redirect(url_for('change_password'))

        email = session['user_email']
        user = UserDAO.get_by_email(email)

        if not user:
            flash("User not found.", "error")
            return redirect(url_for('change_password'))

        if not check_password_hash(user.password, current_password):
            flash("Wrong current password.", "error")
            return redirect(url_for('change_password'))

        hashed_password = generate_password_hash(new_password)
        UserDAO.update_password(email, hashed_password)
        flash("Password updated successfully!", "success")
        return redirect(url_for('home'))

    return render_template('change_password.html')


def change_nickname():
    if 'user_email' not in session:
        flash("You must be logged in to change your nickname.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        nickname = request.form.get('nickname')

        if not validate_input_match(password, confirm_password, "Passwords don't match!"):
            return redirect(url_for('change_nickname'))

        email = session['user_email']
        user = UserDAO.get_by_email(email)

        if not user:
            flash("User not found.", "error")
            return redirect(url_for('change_nickname'))

        if not check_password_hash(user.password, password):
            flash("Wrong password.", "error")
            return redirect(url_for('change_nickname'))

        if not (5 <= len(nickname) <= 50):
            flash("Nickname must be between 5 and 50 characters.", "error")
            return redirect(url_for('change_nickname'))

        UserDAO.update_nickname(email, nickname)
        flash("Nickname updated successfully!", "success")
        return redirect(url_for('lobby'))

    return render_template('change_nickname.html')


def lobby():
    return render_template('lobby.html')


def train():
    return render_template('train.html')


def history():
    return render_template('history.html')


# =========================
# Jogos
# =========================
def game():
    game_id = GameDAO.create("tt", "jh", "jc", "mv", "")
    return render_template('game.html', game_id=game_id)


def suggest_move():
    if request.method == 'GET':
        game_id = request.args.get('game_id')
        partners = GameDAO.get_partners(game_id)
        return render_template('suggest_move.html', game_id=game_id, partners=partners)

    move = request.form.get('move')
    game_id = request.form.get('game_id')
    to_player_id = request.form.get('to_player_id')

    if not move:
        flash('Need to inform a move suggestion.', 'error')
        return redirect(url_for('suggest_move', game_id=game_id))

    MoveDAO.save(game_id, None, to_player_id, move)
    flash('Move suggestion sent!', 'success')
    return redirect(url_for('game', game_id=game_id))


def move():
    if request.method == 'POST':
        data = request.get_json()
        game_id = data.get('game_id')
        from_pos = data.get('from')  # Exemplo: [linha, coluna]
        to_pos = data.get('to')
        piece = data.get('piece')

        is_valid = validate_chess_move(piece, from_pos, to_pos)

        if is_valid:
            MoveDAO.save(game_id, from_pos, to_pos, piece)
            return jsonify({'status': 'ok'})
        else:
            return jsonify({'status': 'invalid'}), 400

    return jsonify({'status': 'error', 'message': 'Method not allowed'}), 405


# =========================
# Validação de movimentos
# =========================
def validate_chess_move(piece, from_pos, to_pos):
    if piece == "pawn":
        if from_pos[1] == to_pos[1] and abs(from_pos[0] - to_pos[0]) in [1, 2]:
            return True
        elif abs(from_pos[0] - to_pos[0]) == 1 and abs(from_pos[1] - to_pos[1]) == 1:
            return True
    elif piece == "rook":
        if from_pos[0] == to_pos[0] or from_pos[1] == to_pos[1]:
            return True
    elif piece == "knight":
        if (abs(from_pos[0] - to_pos[0]) == 2 and abs(from_pos[1] - to_pos[1]) == 1) or \
           (abs(from_pos[0] - to_pos[0]) == 1 and abs(from_pos[1] - to_pos[1]) == 2):
            return True
    elif piece == "bishop":
        if abs(from_pos[0] - to_pos[0]) == abs(from_pos[1] - to_pos[1]):
            return True
    elif piece == "queen":
        if (from_pos[0] == to_pos[0] or from_pos[1] == to_pos[1]) or \
           (abs(from_pos[0] - to_pos[0]) == abs(from_pos[1] - to_pos[1])):
            return True
    elif piece == "king":
        if max(abs(from_pos[0] - to_pos[0]), abs(from_pos[1] - to_pos[1])) == 1:
            return True
    return False

