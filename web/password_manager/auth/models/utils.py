from os import getenv
from datetime import datetime
from random import randint
from time import sleep

from flask import flash, redirect, url_for
from flask_limiter.util import get_remote_address
from bcrypt import hashpw, gensalt, checkpw

from ...database.manager import AuthDbManager


def save_login_attempt(username):
    db = AuthDbManager()
    db.save_attempt(username, get_remote_address(), datetime.now())


def handle_wrong_login(msg):
    flash(msg)
    start = 200
    end = 900
    d = randint(start, end)/1000
    sleep(d)
    return redirect(url_for('website.login'))


def generate_reset_link(reset_id):
    base_url = getenv("BASE_URL")
    path = url_for('website.reset_with_token', reset_id=reset_id)
    return base_url + path


def send_link_to_user_via_email(email, reset_link):
    # Create in v2.0
    print(f'Wysyłam link {reset_link} pod {email}')


def hash_password(password):
    salt_length = int(getenv("SALT_LENGTH"))
    return hashpw(password.encode(), gensalt(salt_length)).decode()


def verify_hashed_password(password, hashed_password):
    return checkpw(password.encode(), hashed_password.encode())
