from flask import Flask, render_template, url_for
from forms import logform,regform


def create_app():
    app = Flask("webapp")
    app.config['SECRET_KEY'] = '216d998a37a90347dfc7b1b729932202'

    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('base.html', 
        _class=['nav-link active', 'nav-link ', 'nav-link '], 
        ariacurrent=['aria-current="page"', '', ''])

    @app.route('/login')
    def login():
        form=logform()
        return render_template('login.html', 
        _class=['nav-link ', 'nav-link active', 'nav-link '], 
        ariacurrent=[' ', 'aria-current="page"', ''],
        form=form)

    @app.route('/signup')
    def signup():
        form=regform()
        return render_template('signup.html', 
        _class=['nav-link ', 'nav-link ', 'nav-link active'], 
        ariacurrent=['', 'aria-current="page"', ''],
        form=form)

    return app
