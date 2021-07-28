from flask import current_app, render_template, url_for, flash,Blueprint,request
from werkzeug.utils import redirect
from . import forms,db,models
from flask_login import login_user, current_user, logout_user, login_required
import datetime
from . import login_manager
import os
import secrets
from PIL import Image

bp = Blueprint("votacion","votacion", url_prefix='')
@login_manager.user_loader
def load_user(user_id):
    return db.filter_user(user_id=user_id)


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


def save_picture(form_picture):
    print(1)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img/profile', picture_fn)
    print(picture_path)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@bp.route("/profile",methods=['GET', 'POST'])
@login_required
def profile():
    form=forms.update_profile_form()
    if form.validate_on_submit():
        if form.picture.data:
            print(2)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.update_user(form,current_user.image_file,current_user.id) 
        flash('Your account has been updated!')
        return redirect(url_for('votacion.profile'))    

    
    return render_template('profile.html', _class=['nav-link ',
                                   'nav-link active', 'nav-link '],
                           ariacurrent=[' ', 'aria-current="page"', ''], form=form)




@bp.route("/user_polls",methods=['GET', 'POST'])
@login_required
def user_polls():
    polls=db.get_all_polls(current_user.id)
    return render_template('user_polls.html', _class=['nav-link ',
                                   'nav-link ', 'nav-link '],
                           ariacurrent=[' ', ' ', ''], polls=polls)


@bp.route("/create_poll",methods=['GET', 'POST'])
@login_required
def create_poll():
    today=datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    poll_url=None

    if request.method == 'POST':
        options = request.form.getlist('options[]')
        title=request.form.get('title')
        date=request.form.get('date')
        time=request.form.get('time')
        
        end_date=date+' '+time
        
        if '' not in options and title!=None and date!=None and time!=None:
            db.add_poll(title,options,end_date,current_user.id)
            poll_id=db.get_new_poll_id()
            poll_url=str(request.url_root)+'poll/'+str(poll_id)

            
    return render_template('create_poll.html', _class=['nav-link ',
                                   'nav-link', 'nav-link '],
                           ariacurrent=['', '', ''],today=today, current_time=current_time,poll_url=poll_url)

@bp.route('/poll/<poll_id>', methods=['GET','POST'])
def show_poll(poll_id):
    poll=db.get_poll(poll_id)
  
    if datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") > poll.end_date:
        flash("Voting Period for this poll has ended")
        return redirect(url_for('votacion.home'))

    if request.method == 'POST':
        option=request.form.get('option')
        email=request.form.get('email')
        if option == None:
            flash("Please pick an option")
        elif email in poll.emails:
            flash("A vote from this email as already been cast. Please enter another emai.")
        else:
            value=poll.options_votes[option]
            poll.options_votes[option]=value+1
            poll.emails.append(email)
            db.update_poll(poll)
            flash("Thank you for voting.")  
            return redirect(url_for('votacion.home'))          
    
    return render_template('show_poll.html',_class=['nav-link ',
                                   'nav-link', 'nav-link '],
                           ariacurrent=['', '', ''],poll=poll)

@bp.route("/delete_account",methods=['GET', 'POST'])
@login_required
def delete_account():
    user_id=current_user.id
    logout_user()
    db.delete_user(user_id)
    flash("Your account has been deleted.")
    return redirect(url_for('votacion.home'))
