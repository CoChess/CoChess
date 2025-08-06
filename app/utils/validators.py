from flask import flash
from app.dao.user_dao import UserDAO

def validate_input_match(input1, input2, error_message):
    """
    Verifica se dois inputs são iguais. Se não forem, dispara uma mensagem flash de erro.
    """
    if input1 != input2:
        flash(error_message, "error")
        return False
    return True

def is_email_registered(email):
    """
    Verifica se um email já está registrado no banco.
    """
    if UserDAO.get_by_email(email):
        flash("Email já registrado.", "error")
        return True
    return False
