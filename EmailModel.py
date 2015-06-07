__author__ = 'Pedro'

from google.appengine.ext import db

class Email(db.Model):
    email = db.StringProperty(required=True)
