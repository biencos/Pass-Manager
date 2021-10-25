from datetime import datetime
from flask import flash, redirect, request, url_for, session, jsonify

from .models.validation import *
from .models.utils import *
from ..database.manager import PasswordsDbManager


from . import passwords

db = PasswordsDbManager()


@passwords.route('/', methods=["GET"])
def get_passwords():
    username = session.get("username")
    if not username:
        flash("Ta akcja wymaga zalogowania!")
        return redirect(url_for('website.home'))
    res = db.get_user_passwords(username)
    response = {}
    if res != None:
        passes = []
        for r in res:
            p = {}
            p['service_name'] = r.service_name
            p['username'] = r.username
            passes.append(p)
        response['passes'] = passes
    else:
        return "Podczas pobierania wystąpił błąd!", 400
    return jsonify(response), 200


@passwords.route('/', methods=["POST"])
def add_passwords():
    username = session.get("username")
    if not username:
        flash("Ta akcja wymaga zalogowania!")
        return redirect(url_for('website.home'))
    ERROR_MESSAGE = "Podczas dodawania wystąpił błąd, czy jesteś pewien że poprawnie wypełniłeś wszystkie pola?"
    if is_empty(request.form):
        return ERROR_MESSAGE, 400
    name = request.form.get("add-name")
    password = request.form.get("add-password")
    master_password = request.form.get("add-master")
    if not is_service_name_valid(name) or not is_password_safe(password, "") or not is_password_safe(master_password, "główne"):
        return ERROR_MESSAGE, 400
    if verify_master(username, master_password):
        password = encrypt_password(password, master_password)
        db.add_user_password(username, name, password)
        return "Dodano nowe hasło", 201
    else:
        return ERROR_MESSAGE, 401


@passwords.route('/', methods=["PUT"])
def change_passwords():
    username = session.get("username")
    if not username:
        flash("Ta akcja wymaga zalogowania!")
        return redirect(url_for('website.home'))
    ERROR_MESSAGE = "Podczas zmiany hasła wystąpił błąd, czy jesteś pewien że poprawnie wypełniłeś wszystkie pola?"
    if is_empty(request.form):
        return ERROR_MESSAGE, 400
    name = request.form.get("change-name")
    password = request.form.get("change-password")
    master_password = request.form.get("change-master")
    if not is_service_name_valid(name) or not is_password_safe(password, "") or not is_password_safe(master_password, "główne"):
        return ERROR_MESSAGE, 400
    if verify_master(username, master_password):
        password = encrypt_password(password, master_password)
        db.change_user_pass(username, name, password)
        now = datetime.now()
        db.insert_password_to_history(username, name, password, now)
        return "Hasło zostało zmienione", 200
    else:
        return ERROR_MESSAGE, 400


@passwords.route('/decrypt', methods=["POST"])
def decrypt():
    username = session.get("username")
    if not username:
        flash("Ta akcja wymaga zalogowania!")
        return redirect(url_for('website.home'))
    ERROR_MESSAGE = "Podczas odszyfrowywania wystąpił błąd, czy jesteś pewien że poprawnie wypełniłeś wszystkie pola?"
    if is_empty(request.form):
        return ERROR_MESSAGE, 400
    service_name = request.form.get("decrypt-name")
    master_password = request.form.get("decrypt-master")
    if not is_service_name_valid(service_name) or not is_password_safe(master_password, ""):
        return ERROR_MESSAGE, 400
    if verify_master(username, master_password):
        res = db.get_user_pass(username, service_name)
        if res != None:
            response = {}
            response['pass'] = decrypt_password(master_password, res)
            return jsonify(response), 200
        else:
            return ERROR_MESSAGE, 400
    else:
        return ERROR_MESSAGE, 401


@passwords.route('/history', methods=["POST"])
def history():
    username = session.get("username")
    if not username:
        flash("Ta akcja wymaga zalogowania!")
        return redirect(url_for('website.home'))
    ERROR_MESSAGE = "Podczas pobierania historii hasła wystąpił błąd, czy jesteś pewien że poprawnie wypełniłeś wszystkie pola?"
    if is_empty(request.form):
        return ERROR_MESSAGE, 400
    service_name = request.form.get("show-name")
    master_password = request.form.get("show-master")
    if not is_service_name_valid(service_name) or not is_password_safe(master_password, "główne"):
        return ERROR_MESSAGE, 400
    if verify_master(username, master_password):
        res = db.get_password_history(username, service_name)
        response = {}
        if res != None:
            history = []
            for r in res:
                h = {}
                h['password'] = decrypt_password(master_password, r.password)
                h['time'] = r.time
                history.append(h)
            response['history'] = history
        return jsonify(response), 200
    else:
        return ERROR_MESSAGE, 400


@passwords.route('/info/<service_name>', methods=["GET"])
def get_info(service_name):
    username = session.get("username")
    if not username:
        flash("Ta akcja wymaga zalogowania!")
        return redirect(url_for('website.home'))
    ERROR_MESSAGE = "Podczas pobierania informacji wystąpił błąd, czy jesteś pewien że poprawnie wypełniłeś wszystkie pola?"
    res = db.get_service_info(username, service_name)
    if res != None:
        response = {}
        response['image_url'] = res.image_url
        response['service_url'] = res.service_url
        response['service_name'] = res.service_name
        response['user_name'] = res.username
        return jsonify(response), 200
    else:
        return ERROR_MESSAGE, 400


@passwords.route('/info', methods=["POST"])
def add_info():
    username = session.get("username")
    if not username:
        flash("Ta akcja wymaga zalogowania!")
        return redirect(url_for('website.home'))
    ERROR_MESSAGE = "Podczas dodawania informacji wystąpił błąd, czy jesteś pewien że poprawnie wypełniłeś wszystkie pola?"
    if is_empty(request.form):
        return ERROR_MESSAGE, 400
    name = request.form.get("addi-name")
    user_name = request.form.get("addi-username")
    service_url = request.form.get("addi-url")
    image_url = request.form.get("addi-image")
    master_password = request.form.get("addi-master")
    if not is_service_name_valid(name) or not is_password_safe(master_password, "główne"):
        return ERROR_MESSAGE, 400
    if verify_master(username, master_password):
        db.add_service_info(username, name, user_name, service_url, image_url)
        return "Dodano nowe informacje", 201
    else:
        return ERROR_MESSAGE, 401


@passwords.route('/generate/<pass_length>', methods=["GET"])
def generate(pass_length):
    username = session.get("username")
    if not username:
        flash("Ta akcja wymaga zalogowania!")
        return redirect(url_for('website.home'))
    response = {}
    if not pass_length:
        response['password'] = generate_password()
    else:
        response['password'] = generate_password(int(pass_length))
    return jsonify(response), 200
