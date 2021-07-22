from flask import Flask,g,current_app
from . import votacion
from . import db



def create_app():
    app = Flask("webapp")
    app.config.from_mapping(
        SECRET_KEY = '216d998a37a90347dfc7b1b729932202',
        DATABASE='votacion')

    
    app.register_blueprint(votacion.bp)
    db.init_app(app)
   
   
    return app
