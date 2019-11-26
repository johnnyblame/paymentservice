import os
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = '/tmp'

class Config(object):
    SECRET_KEY = 'SecretKey01'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


