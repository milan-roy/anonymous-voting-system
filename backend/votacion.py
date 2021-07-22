from flask import current_app, render_template, url_for, flash,Blueprint
from werkzeug.utils import redirect
from . import forms
from . import db


bp = Blueprint("votacion","votacion", url_prefix='')


@bp.route('/')
@bp.route('/home')
def home():
    return render_template('base.html',
                           _class=['nav-link active',
                                   'nav-link ', 'nav-link '],
                           ariacurrent=['aria-current="page"', '', ''])


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.logform()
    if form.validate_on_submit():
        if not db.does_email_exist(form.email.data):
            flash("This email is not registered.")
            return redirect(url_for('votacion.login'))
        elif not db.does_email_and_password_match(form.email.data, form.password.data):
            flash("Incorrect Password")
            return redirect(url_for('votacion.login'))
        flash('Log in Successfull', 'success')
        return redirect(url_for('votacion.home'))
    return render_template('login.html',
                           _class=['nav-link ',
                                   'nav-link active', 'nav-link '],
                           ariacurrent=[' ', 'aria-current="page"', ''],
                           form=form)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.regform()
    if form.validate_on_submit():
        db.adds_user(form)
        flash('Registration Successfull. You can now Login.', 'success')
        return redirect(url_for('votacion.login'))
    return render_template('signup.html',
                           _class=['nav-link ', 'nav-link ',
                                   'nav-link active'],
                           ariacurrent=['', 'aria-current="page"', ''],
                           form=form)
