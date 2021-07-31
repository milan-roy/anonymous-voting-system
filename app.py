from flask import Flask
import db
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY = '216d998a37a90347dfc7b1b729932202',
    DATABASE='postgres://ejnatrvfztnojm:1df41ba287d48d1203edeb1a957630e0782bb1f3aee8c38c94d3d4ebd8be8d09@ec2-23-23-164-251.compute-1.amazonaws.com:5432/do6h4l6f1gn2i')

login_manager = LoginManager(app)  
login_manager.login_view = 'votacion.login'
login_manager.login_message_category = 'info'
import votacion    
app.register_blueprint(votacion.bp) 
db.init_app(app)

if __name__ == "__main__":
    app.run()
   
