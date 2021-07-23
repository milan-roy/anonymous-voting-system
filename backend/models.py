from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from . import login_manager
from . import db

@login_manager.user_loader
def load_user(user_id):
    return db.filter_user(user_id=user_id)
        

class User(UserMixin):
    id = None
    username =None
    email =None
    image_file =None
    last_login =None

    
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