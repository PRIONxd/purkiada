import os
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = os.urandom(25)
    WTF_CSRF_SECRET_KEY = os.urandom(25)
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/student.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(30)