from flask import Flask, render_template, url_for


def create_app():
    app = Flask("webapp")

    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('base.html', _class=['nav-link active', 'nav-link ', 'nav-link '], ariacurrent=['aria-current="page"', '', ''])

    @app.route('/login')
    def login():
        return render_template('base.html', _class=['nav-link ', 'nav-link active', 'nav-link '], ariacurrent=[' ', 'aria-current="page"', ''])

    @app.route('/signup')
    def signup():
        return render_template('base.html', _class=['nav-link ', 'nav-link ', 'nav-link active'], ariacurrent=['', 'aria-current="page"', ''])

    return app
