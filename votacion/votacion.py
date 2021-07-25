from flask import current_app, render_template, url_for, flash,Blueprint,request
from werkzeug.utils import redirect
from . import forms,db,models
from flask_login import login_user, current_user, logout_user, login_required


bp = Blueprint("votacion","votacion", url_prefix='')


@bp.route('/')
@bp.route('/home',methods=['GET'])
def home():
    return render_template('home.html',
                           _class=['nav-link active',
                                   'nav-link ', 'nav-link '],
                           ariacurrent=['aria-current="page"', '', ''])


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('votacion.home'))

    form = forms.log_form()
    if form.validate_on_submit():
        if not db.does_email_exist(form.email.data):
            flash("This email is not registered.")
            return redirect(url_for('votacion.login'))
        elif not db.does_email_and_password_match(form.email.data, form.password.data):
            flash("Incorrect Password")
            return redirect(url_for('votacion.login'))

        db.update_last_login(form.email.data)
        user=db.filter_user(email=form.email.data)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        flash('Log in Successfull')
        return redirect(url_for('votacion.home'))

    return render_template('login.html',
                           _class=['nav-link ',
                                   'nav-link active', 'nav-link '],
                           ariacurrent=[' ', 'aria-current="page"', ''],
                           form=form)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('votacion.home'))

    form = forms.reg_form()
    if form.validate_on_submit():
        db.adds_user(form)
        flash('Registration Successfull. You can now Login.')
        return redirect(url_for('votacion.login'))
        
    return render_template('signup.html',
                           _class=['nav-link ', 'nav-link ',
                                   'nav-link active'],
                           ariacurrent=['', 'aria-current="page"', ''],
                           form=form)

@bp.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('votacion.home'))


@bp.route("/profile",methods=['GET', 'POST'])
@login_required
def profile():
    form=forms.update_profile_form()
    return render_template('profile.html', _class=['nav-link ',
                                   'nav-link active', 'nav-link '],
                           ariacurrent=[' ', 'aria-current="page"', ''], form=form)
                        
@bp.route("/create_poll",methods=['GET', 'POST'])
@login_required
def create_poll():
    if request.method == 'POST':
        options = request.form.getlist('options[]')
        print(options)
    
    return render_template('create_poll.html', _class=['nav-link ',
                                   'nav-link', 'nav-link '],
                           ariacurrent=['', '', ''])