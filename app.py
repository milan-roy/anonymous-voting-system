from flask import Flask
import db
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY = '216d998a37a90347dfc7b1b729932202',
     DATABASE='postgres://ymldmoccoalkwh:62e95d9b373d0192937168649333ab3147da01b7dcc12625071410af5a193696@ec2-54-211-160-34.compute-1.amazonaws.com:5432/db9l1uemtpj0fp')


login_manager = LoginManager(app)  
login_manager.login_view = 'votacion.login'
login_manager.login_message_category = 'info'
import votacion    
app.register_blueprint(votacion.bp) 
db.init_app(app)

if __name__ == "__main__":
    app.run()
   
