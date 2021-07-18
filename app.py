from flask import Flask, render_template,url_for

def create_app():
    app=Flask("webapp")
    @app.route('/')
    def home():
        return render_template('home.html')


    return app


