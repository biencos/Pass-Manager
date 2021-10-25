from datetime import datetime, timedelta
from flask import flash, redirect, request, url_for, session
from uuid import uuid4

from .models.utils import *
from .models.validation import *
from ..database.manager import AuthDbManager

from . import auth

db = AuthDbManager()


@auth.route('/register', methods=['POST'])
def register():
    if is_empty(request.form):
        return redirect(url_for('website.register'))
    user = {}
    for n in ['username', 'email', 'password', 'password1', 'master_password', 'master_password1']:
        user[n] = request.form.get(n)
    if not is_user_valid(user):
        return redirect(url_for('website.register'))
    hashed = hash_password(user['password'])
    mhashed = hash_password(user['master_password'])
    db.register_user(user['username'], user['email'], hashed, mhashed)
    return redirect(url_for('website.login'))


@auth.route('/login', methods=['POST'])
def login():
    if is_empty(request.form):
        handle_wrong_login("Nazwa użytkownika ani hasło nie może być puste!")
    username = request.form.get('username')
    password = request.form.get('password')
    if not is_username_login_valid(username):
        handle_wrong_login("Podano niepoprawną nazwę użytkownika!")
    if not is_password_login_valid(password):
        handle_wrong_login("Podano niepoprawne hasło!")
    if db.is_registred(username):
        hashed = db.get_user_password(username)
        if hashed:
            if verify_hashed_password(password, hashed):
                session["username"] = username
                session["logged-at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
                return redirect(url_for('website.dashboard'))
            else:
                save_login_attempt(username)
                return handle_wrong_login("Nieprawidłowe dane logowania!")
    else:
        return handle_wrong_login("Nieprawidłowe dane logowania!")


@auth.route('/reset', methods=['POST'])
def handle_reset_request():
    if is_empty(request.form):
        return redirect(url_for('website.reset'))
    email = request.form.get('email')
    if not is_email_valid(email):
        return redirect(url_for('website.reset'))
    if db.is_email_registered(email):
        if db.is_resetting_already(email):
            flash("Niepoprawny email, popraw go i spróbuj ponownie!")
            return redirect(url_for('website.reset'))
        reset_id = uuid4().hex + uuid4().hex
        experience_date = datetime.utcnow() + timedelta(hours=24)
        db.save_reset_request(email, reset_id, experience_date)
        reset_link = generate_reset_link(reset_id)
        send_link_to_user_via_email(email, reset_link)
        flash("Link do zresetowania hasła został wysłany na twój email!")
        return redirect(url_for('website.reset'))
    else:
        flash("Na podany adres email wysłano link do zresetowania hasła.")
        return redirect(url_for('website.reset'))


@auth.route('/reset/<reset_id>', methods=['POST'])
def reset_password(reset_id):
    if not db.is_allowed_for_resetting(reset_id):
        flash("Wystąpił błąd!")
        return redirect(url_for('website.home'))
    if not db.is_reset_link_valid(reset_id):
        db.delete_reset_link(reset_id)
        flash("Wystąpił błąd!")
        return redirect(url_for('website.home'))
    email = db.get_email_with_reset_id(reset_id)
    print(email)
    if email == None:
        flash("Wystąpił błąd!")
        return redirect(url_for('website.home'))
    password = request.form.get('password')
    password1 = request.form.get('password1')
    if not is_passwords_safe(password, password1, ""):
        return redirect(url_for('website.reset_with_token', reset_id=reset_id))
    hashed = hash_password(password)
    db.change_user_password(email, hashed)
    db.delete_reset_link(reset_id)
    flash(f"Twoje hasło zostało zmienione")
    return redirect(url_for('website.login'))
