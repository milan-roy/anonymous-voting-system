from flask import Flask
from . import db
from flask_login import LoginManager


app = Flask("webapp")
app.config.from_mapping(
    SECRET_KEY = '216d998a37a90347dfc7b1b729932202',
     DATABASE='votacion')


login_manager = LoginManager(app)  
login_manager.login_view = 'votacion.login'
login_manager.login_message_category = 'info'
from . import votacion    
app.register_blueprint(votacion.bp)
db.init_app(app)
   
