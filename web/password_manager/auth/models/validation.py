from os import getenv
from re import match, search, compile

from flask import flash
from ...database.manager import AuthDbManager

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


def is_username_valid(username):
    if len(username) < USERNAME_MIN_LENGTH:
        flash("Nazwa użytkownika jest zbyt krótka")
        return False
    if len(username) > USERNAME_MAX_LENGTH:
        flash("Nazwa użytkownika jest zbyt długa")
        return False
    if not match('^[a-z]+$', username):
        flash("Nazwa użytkownika może składać się tylko z małych liter!")
        return False
    return True


def is_email_valid(email):
    if len(email) < EMAIL_MIN_LENGTH:
        flash("Email jest zbyt krótki")
        return False
    if len(email) > EMAIL_MAX_LENGTH:
        flash(f"Email nie może być dłuższy niż {EMAIL_MAX_LENGTH} znaków")
        return False
    if not search('[^@]+@[^@]+\.[^@]+', email):
        flash("Niepoprawny email, popraw go i spróbuj ponownie!")
        return False
    return True


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


def is_passwords_safe(password, password1, prfx):
    if not is_password_safe(password, prfx):
        return False
    if password != password1:
        flash(f"Podane hasła {prfx} nie pasują do siebie!")
        return False
    return True


def is_user_valid(user):
    if not is_username_valid(user['username']) or not is_email_valid(user['email']):
        return False
    if not is_passwords_safe(user['password'], user['password1'], "") or not is_passwords_safe(user['master_password'], user['master_password1'], "główne"):
        return False
    db = AuthDbManager()
    if db.is_registred(user['username']):
        flash("Niepoprawna nazwa użytkownika, popraw ją i spróbuj ponownie")
        return False
    return True


def is_username_login_valid(username):
    if len(username) < USERNAME_MIN_LENGTH or len(username) > USERNAME_MAX_LENGTH:
        return False
    return True


def is_password_login_valid(password):
    if len(password) < PASSWORD_MIN_LENGTH or len(password) > PASSWORD_MAX_LENGTH:
        return False
    return True
