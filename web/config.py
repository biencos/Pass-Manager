import os


class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'SecretKey')


class TestingConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'TestingKey')


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.getenv('SECRET_KEY')
