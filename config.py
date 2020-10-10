import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'how-well-can-you-guess-it'