from os import getenv
from re import search, compile

from flask import flash

USERNAME_MIN_LENGTH = int(getenv("USERNAME_MIN_LENGTH"))
USERNAME_MAX_LENGTH = int(getenv("USERNAME_MAX_LENGTH"))
EMAIL_MIN_LENGTH = int(getenv("EMAIL_MIN_LENGTH"))
EMAIL_MAX_LENGTH = int(getenv("EMAIL_MAX_LENGTH"))
PASSWORD_MIN_LENGTH = int(getenv("PASSWORD_MIN_LENGTH"))
PASSWORD_MAX_LENGTH = int(getenv("PASSWORD_MAX_LENGTH"))
SERVICE_NAME_MIN_LENGTH = int(getenv("SERVICE_NAME_MIN_LENGTH"))
SERVICE_NAME_MAX_LENGTH = int(getenv("SERVICE_NAME_MAX_LENGTH"))


def is_empty(form):
    empty_fields = [f for f in form.values() if not f]
    if len(empty_fields) != 0:
        flash("W twoim formularzu są puste pola! Wypełnij go i spróbuj ponownie")
        return True
    return False


def is_password_safe(password, prfx):
    if not password:
        flash(f"Hasło {prfx} nie może być puste!")
        return False
    if len(password) < PASSWORD_MIN_LENGTH:
        flash(
            f"Hasło {prfx} musi mieć conajmniej {PASSWORD_MIN_LENGTH} znaków!")
        return False
    if len(password) > PASSWORD_MAX_LENGTH:
        flash(f"Hasło {prfx} jest zbyt długie!")
        return False
    regex = ("^(?=.*[a-z])(?=." + "*[A-Z])(?=.*\\d)" +
             "(?=.*[-+_!@#$%^&*., ?]).+$")
    if not search(compile(regex), password):
        flash(f"Hasło {prfx} musi składać się przynajmniej: z jednej dużej litery, z jednego małego znaku, z jednej cyfry oraz z jednego znaku specjalnego!")
        return False
    return True


def is_service_name_valid(name):
    if len(name) < SERVICE_NAME_MIN_LENGTH or len(name) > SERVICE_NAME_MAX_LENGTH:
        return False
    return True
