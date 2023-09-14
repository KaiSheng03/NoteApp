from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_pymongo import PyMongo
from bson import ObjectId

class Note():
    def __init__(self, user_id, data):
        self.user_id = user_id
        self.data = data

class User():
    def __init__(self, email, firstName, lastName, age, address, password, securityKey):
        self.id = ObjectId()
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.address = address
        self.password = password
        self.securityKey = securityKey