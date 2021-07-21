from flask import current_app, render_template, url_for, flash,Blueprint
from werkzeug.utils import redirect
from . import forms

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
        if form.email.data == 'milanroy.in@gmail.com' and form.password.data == '12345':
            flash('Log in Successfull', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please check email and password', 'success')
    return render_template('login.html',
                           _class=['nav-link ',
                                   'nav-link active', 'nav-link '],
                           ariacurrent=[' ', 'aria-current="page"', ''],
                           form=form)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.regform()
    if form.validate_on_submit():
        flash('Congratulation, you are now a Votacion member.', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html',
                           _class=['nav-link ', 'nav-link ',
                                   'nav-link active'],
                           ariacurrent=['', 'aria-current="page"', ''],
                           form=form)
