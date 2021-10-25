from flask import Flask
from extensions import *


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.DevelopmentConfig")

    db.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        from .auth.routes import auth
        app.register_blueprint(auth, url_prefix="/api/auth")

        from .passwords.routes import passwords
        app.register_blueprint(passwords, url_prefix="/api/passwords")

        from .website.routes import website
        app.register_blueprint(website)

        db.create_all()

        return app
