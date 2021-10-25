from .. import db


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(250))
    master_password = db.Column(db.String(250))

    def __init__(self, username, email, password, master_password):
        self.username = username
        self.email = email
        self.password = password
        self.master_password = master_password


class passwords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    service_name = db.Column(db.String(250))
    password = db.Column(db.String(250))

    def __init__(self, username, service_name, password):
        self.username = username
        self.service_name = service_name
        self.password = password


class attempts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    ip_address = db.Column(db.String(100))
    time = db.Column(db.String(100))

    def __init__(self, username, ip_address, time):
        self.username = username
        self.ip_address = ip_address
        self.time = time


class resets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    reset_id = db.Column(db.String(250))
    end_time = db.Column(db.String(100))

    def __init__(self, email, reset_id, end_time):
        self.email = email
        self.reset_id = reset_id
        self.end_time = end_time


class passwords_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    service_name = db.Column(db.String(250))
    password = db.Column(db.String(250))
    time = db.Column(db.String(100))

    def __init__(self, username, service_name, password, time):
        self.username = username
        self.service_name = service_name
        self.password = password
        self.time = time


class services_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    service_name = db.Column(db.String(250))
    user_name = db.Column(db.String(100))
    service_url = db.Column(db.String(250))
    image_url = db.Column(db.String(250))

    def __init__(self, username, service_name, user_name, service_url, image_url):
        self.username = username
        self.service_name = service_name
        self.user_name = user_name
        self.service_url = service_url
        self.image_url = image_url
