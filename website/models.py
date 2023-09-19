from . import mongo
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, _id, email, password, first_name, last_name, age, address, security_key):
        self._id = _id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.address = address
        self.security_key = security_key

    # Optional: You can define a method to save the user data to MongoDB
    def save(self):
        user_data = {
            '_id': self._id,
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'address': self.address,
            'security_key': self.security_key
        }
        mongo.db.users.insert_one(user_data)

    @classmethod
    def find_by_email(cls, email):
        return mongo.db.users.find_one({'email': email})

    def get_id(self):
        return str(self._id)
    
    @classmethod
    def update_password(cls, id, password):
        mongo.db.users.update_one({'_id': id}, {'$set': {'password': password}})

    @classmethod
    def find_and_update(cls, id, firstName, lastName, age, address):
        mongo.db.users.update_one(
            {'_id': id},
            {'$set': {
                'first_name': firstName,
                'last_name': lastName,
                'age': age,
                'address': address
            }})
    
class Note:
    def __init__(self, data, user_id):
        self.data = data
        self.user_id = user_id

    # Optional: You can define a method to save the note data to MongoDB
    def save(self):
        note_data = {
            'data': self.data,
            'user_id': self.user_id
        }
        mongo.db.notes.insert_one(note_data)

    @classmethod
    def find_notes_by_user_id(cls, user_id):
        return list(mongo.db.notes.find({'user_id': user_id}))
    
    @classmethod
    def find_note(cls, id):
        return mongo.db.notes.find_one({'_id': id})

    @classmethod
    def find_and_delete(cls, id):
        mongo.db.notes.delete_one({'_id': id})