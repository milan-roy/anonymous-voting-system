from flask import Flask, render_template, url_for, flash
from werkzeug.utils import redirect
from forms import logform, regform


def create_app():
    app = Flask("webapp")
    app.config['SECRET_KEY'] = '216d998a37a90347dfc7b1b729932202'

    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('base.html',
                               _class=['nav-link active',
                                       'nav-link ', 'nav-link '],
                               ariacurrent=['aria-current="page"', '', ''])

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = logform()
        if form.validate_on_submit():
            if form.email.data=='milanroy.in@gmail.com' and form.password.data=='12345':
                flash('Log in Successfull','success')
                return redirect(url_for('home'))
            else:
                flash('Please check email and password','success')
        return render_template('login.html',
                               _class=['nav-link ',
                                       'nav-link active', 'nav-link '],
                               ariacurrent=[' ', 'aria-current="page"', ''],
                               form=form)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = regform()
        if form.validate_on_submit():
            flash('Congratulation, you are now a Votacion member.', 'success')
            return redirect(url_for('home'))
        return render_template('signup.html',
                               _class=['nav-link ', 'nav-link ',
                                       'nav-link active'],
                               ariacurrent=['', 'aria-current="page"', ''],
                               form=form)

    return app
