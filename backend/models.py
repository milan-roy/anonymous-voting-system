from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from flask_login import LoginManager
from . import db


login_manager = LoginManager(current_app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_user_by_id(user_id)
        

class User(UserMixin):
    id = 0
    username = ""
    email = ""
    image_file = ""
    last_login =""

    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post():
    id =0
    title = ""
    content = ""
    auth_id = 0
    creation_date= ""
    end_date=""
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"