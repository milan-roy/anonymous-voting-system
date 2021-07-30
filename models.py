
from flask import current_app
from flask_login import UserMixin
        

class User(UserMixin):
    id = None
    username =None
    email =None
    image_file =None

      
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Poll():
    id =None
    title =None
    options_votes =None
    auth_id =None
    emails=[' ']
    creation_date=None
    end_date=None
    

    def __repr__(self):
        return f"Poll('{self.title}', '{self.creation_date}')"