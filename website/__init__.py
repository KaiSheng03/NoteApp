from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson import ObjectId

mongo = PyMongo()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ABCDEFGHI'
    app.config['MONGO_URI'] = "mongodb+srv://kai:KZqXP6fcS6Q73Ves@cluster0.mvr574p.mongodb.net/db?retryWrites=true&w=majority"
    mongo.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        objectId = ObjectId(id)
        user = mongo.db.users.find_one({'_id': objectId})
        if user:
            return User(user['_id'], user['email'], user['password'], user['first_name'], user['last_name'], user['age'], user['address'], user['security_key'])
      
    return app
