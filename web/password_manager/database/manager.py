from .models import db
from .models import users, passwords, attempts, resets, passwords_history, services_info
from .db_utils import validate_reset_link_date


class AuthDbManager(object):
    def is_registred(self, username):
        user = users.query.filter_by(username=username).first()
        return user != None

    def register_user(self, username, email, hashed, master_hashed):
        user = users(username, email, hashed, master_hashed)
        db.session.add(user)
        db.session.commit()

    def get_user_password(self, username):
        user = users.query.filter_by(username=username).first()
        return user.password

    def save_attempt(self, username, ip_address, date):
        attempt = attempts(username, ip_address, date)
        db.session.add(attempt)
        db.session.commit()

    def is_email_registered(self, email):
        user = users.query.filter_by(email=email).first()
        return user != None

    def is_resetting_already(self, email):
        user = resets.query.filter_by(email=email).first()
        return user != None

    def save_reset_request(self, email, reset_id, experience_date):
        reset = resets(email, reset_id, experience_date)
        db.session.add(reset)
        db.session.commit()

    def is_allowed_for_resetting(self, reset_id):
        user = resets.query.filter_by(reset_id=reset_id).first()
        return user != None

    def is_reset_link_valid(self, reset_id):
        reset_info = resets.query.filter_by(reset_id=reset_id).first()
        if reset_info != None:
            end_time = reset_info.end_time
            return validate_reset_link_date(end_time)
        return False

    def delete_reset_link(self, reset_id):
        reset_info = resets.query.filter_by(reset_id=reset_id).first()
        db.session.delete(reset_info)
        db.session.commit()

    def get_email_with_reset_id(self, reset_id):
        reset_info = resets.query.filter_by(reset_id=reset_id).first()
        if reset_info != None:
            return reset_info.email
        return None

    def change_user_password(self, email, hashed):
        user = users.query.filter_by(email=email).first()
        user.password = hashed
        db.session.commit()


class PasswordsDbManager(object):
    def get_user_passwords(self, username):
        res = passwords.query.filter_by(username=username).all()
        return res

    def add_user_password(self, username, service_name, password):
        password = passwords(username, service_name, password)
        db.session.add(password)
        db.session.commit()

    def get_user_master_password(self, username):
        res = users.query.filter_by(username=username).first()
        if res != None:
            return res.master_password
        return None

    def get_user_pass(self, username, service_name):
        res = passwords.query.filter_by(
            username=username, service_name=service_name).first()
        if res != None:
            return res.password
        return None

    def change_user_pass(self, username, service_name, hashed):
        res = passwords.query.filter_by(
            username=username, service_name=service_name).first()
        res.password = hashed
        db.session.commit()

    def insert_password_to_history(self, username, service_name, password, time):
        password_history = passwords_history(
            username, service_name, password, time)
        db.session.add(password_history)
        db.session.commit()

    def get_password_history(self, username, service_name):
        res = passwords_history.query.filter_by(
            username=username, service_name=service_name).all()
        return res

    def add_service_info(self, username, service_name, user_name, service_url, image_url):
        service_info = services_info(
            username, service_name, user_name, service_url, image_url)
        db.session.add(service_info)
        db.session.commit()

    def get_service_info(self, username, service_name):
        res = services_info.query.filter_by(
            username=username, service_name=service_name).first()
        return res
