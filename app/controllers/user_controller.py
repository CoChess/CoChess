from flask import render_template, request, redirect, url_for, flash, current_app, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user_model import get_user_by_email, update_user_password, update_user_nickname, create_game, save_move
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
    email = request.args.get('email')
    game_id = create_game("tt", "jh", "jc", "mv", "")
    return render_template('game.html', game_id=game_id)
    
def suggest_move():
    if request.method == 'GET':
        game_id = request.args.get('game_id')
        return render_template('suggest_move.html', game_id=game_id)

    move = request.form.get('move')
    game_id = request.form.get('game_id')

    if not move:
        flash('Você precisa informar um movimento.', 'error')
        return redirect(url_for('suggest_move', game_id=game_id))

    save_move(game_id, None, None, move)
    flash('Sugestão enviada com sucesso!', 'success')
    return redirect(url_for('game_detail', game_id=game_id))

def move():
    if request.method == 'POST':
        data = request.get_json()
        game_id = data.get('game_id')
        from_pos = data.get('from')  # Exemplo: [linha, coluna]
        to_pos = data.get('to')
        piece = data.get('piece')

        is_valid = False
        # Exemplo simples de validação para peão
        if piece == "pawn":
            # Movimento normal: 1 ou 2 casas na mesma coluna
            if from_pos[1] == to_pos[1] and abs(from_pos[0] - to_pos[0]) in [1, 2]:
                is_valid = True
            # Captura: 1 casa na diagonal
            elif abs(from_pos[0] - to_pos[0]) == 1 and abs(from_pos[1] - to_pos[1]) == 1:
                is_valid = True
        elif piece == "rook":
            if from_pos[0] == to_pos[0] or from_pos[1] == to_pos[1]:
                is_valid = True
        elif piece == "knight":
            if (abs(from_pos[0] - to_pos[0]) == 2 and abs(from_pos[1] - to_pos[1]) == 1) or \
               (abs(from_pos[0] - to_pos[0]) == 1 and abs(from_pos[1] - to_pos[1]) == 2) or \
               (abs(from_pos[0] - to_pos[0]) == 4 and abs(from_pos[1] - to_pos[1]) == 2) or \
               (abs(from_pos[0] - to_pos[0]) == 2 and abs(from_pos[1] - to_pos[1]) == 4):
                is_valid = True
        elif piece == "bishop":
            if abs(from_pos[0] - to_pos[0]) == abs(from_pos[1] - to_pos[1]):
                is_valid = True
        elif piece == "queen":
            if (from_pos[0] == to_pos[0] or from_pos[1] == to_pos[1]) or \
               (abs(from_pos[0] - to_pos[0]) == abs(from_pos[1] - to_pos[1])):
                is_valid = True
        elif piece == "king":
            if abs(from_pos[0] - to_pos[0]) <= 1 and abs(from_pos[1] - to_pos[1]) <= 1:
                is_valid = True
        else:
            # Outras peças: sempre válido (ajuste conforme sua lógica)
            is_valid = True

        if is_valid:
            save_move(game_id, from_pos, to_pos, piece)
            return jsonify({'status': 'ok'})
        else:
            return jsonify({'status': 'invalid'}), 400

    return jsonify({'status': 'error', 'message': 'Método não permitido'}), 405

