__author__ = 'Pedro'

from google.appengine.ext import db

class Peixe(db.Model):
    temperatura = db.IntegerProperty(required=True)
    ph = db.IntegerProperty(required=True)
    dureza = db.IntegerProperty(required=True)
    alcalinidade = db.IntegerProperty(required=True)
    nivelo2 = db.IntegerProperty(required=True)
    transparencia = db.IntegerProperty(required=True)
    data = db.DateTimeProperty(auto_now_add=True)

