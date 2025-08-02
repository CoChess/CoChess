from flask import flash
from app.models.user_model import get_user_by_email

def validate_input_match(input1, input2, error_message):
    if input1 != input2:
        flash(error_message, "error")
        return False
    return True

def is_email_registered(email):
    if get_user_by_email(email):
        flash("Email já registrado.", "error")
        return True
    return False

