import psycopg2
from psycopg2.extras import Json, DictCursor
import click
from flask import current_app, g
from flask.cli import with_appcontext
import datetime
from . import forms
from flask_bcrypt import Bcrypt
from. import models


def get_conn():
    if 'conn' not in g:
        dbname = current_app.config['DATABASE']
        try:
            g.conn = psycopg2.connect(f"dbname={dbname}")
        except:
            return None
    return g.conn


def close_connection(e=None):
    conn = g.pop('conn', None)
    if conn is not None:
        conn.close()


def get_bcrypt():
    if 'bcryt' not in g:
        g.bcrypt = Bcrypt(current_app)
    return g.bcrypt


def init_databse():
    conn = get_conn()
    if conn is None:
        return conn
    sql_file = current_app.open_resource('static/sql_code.sql')
    sql_code = sql_file.read()
    cur = conn.cursor()
    cur.execute(sql_code)
    conn.commit()
    cur.close()
    close_connection()
    return "Task Done"


def adds_user(form):
    conn = get_conn()
    cur = conn.cursor()
    bcrypt = get_bcrypt()
    hashed_password = bcrypt.generate_password_hash(
        form.password.data).decode('utf-8')
    cur.execute("INSERT INTO users (username,email,password) VALUES(%s,%s,%s)", [
                form.username.data, form.email.data, hashed_password])
    conn.commit()
    cur.close()


def does_username_exist(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username from users")
    username_list = cur.fetchall()
    cur.close()
    temp_tuple = (username,)
    return temp_tuple in username_list


def does_email_exist(email):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT email from users")
    email_list = cur.fetchall()
    cur.close()
    temp_tuple = (email,)
    return temp_tuple in email_list


def does_email_and_password_match(email, password):
    conn = get_conn()
    cur = conn.cursor()
    bcrypt = get_bcrypt()
    cur.execute("SELECT password from users where email=(%s)", (email,))
    hashed_password = cur.fetchone()[0]
    cur.close()
    return bcrypt.check_password_hash(hashed_password, password)


def filter_user(user_id=None, email=None, username=None):
    
    conn = get_conn()
    cur = conn.cursor()
    if user_id:
        cur.execute(
            "SELECT id,username,email,image_file from users where id=(%s)", (user_id,))
    if email:
        cur.execute(
            "SELECT id,username,email,image_file from users where email=(%s)", (email,))
    if username:
        cur.execute(
            "SELECT id,username,email,image_file from users where username=(%s)", (username,))
    temp = cur.fetchone()
    cur.close()
    user = models.User()
    user.id = temp[0]
    user.username = temp[1]
    user.email = temp[2]
    user.image_file = temp[3]
    return user

def delete_user(user_id):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute("delete from users where id=(%s)",(user_id,))
    conn.commit()
    cur.close()

def update_user(form,picture_file,user_id):
    conn=get_conn()
    cur=conn.cursor()
    bcrypt = get_bcrypt()
    hashed_password = bcrypt.generate_password_hash(
        form.password.data).decode('utf-8')
    cur.execute("update users set username=(%s),email=(%s),password=(%s),image_file=(%s)  where id=(%s)",[form.username.data,form.email.data,hashed_password,picture_file,user_id])
    conn.commit()
    cur.close()


def add_poll(title, options, end_date, auth_id):
    conn = get_conn()
    cur = conn.cursor()
    now = datetime.datetime.now()
    creation_date = now.strftime("%Y-%m-%d %H:%M:%S")
    options_vote = {}
    for i in options:
        options_vote[i] = 0
    emails=[]
    cur.execute("Insert into polls (title,options_votes,auth_id,emails,creation_date,end_date) Values(%s,%s,%s,%s,%s,%s)", [
                title, Json(options_vote), auth_id,emails, creation_date, end_date])
    conn.commit()
    cur.close


def get_new_poll_id():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("Select id from polls")
    id_list = cur.fetchall()
    return id_list[-1][0]


def get_poll(poll_id):
    
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        " Select title, options_votes, auth_id,emails, creation_date, end_date from polls where id =(%s)", (poll_id))
    temp = cur.fetchone()
    poll = models.Poll()
    poll.id = poll_id
    poll.title = temp[0]
    poll.options_votes = temp[1]
    poll.auth_id = temp[2]
    poll.emails=temp[3]
    poll.creation_date = temp[4]
    poll.end_date = temp[5]
    cur.close()
    return poll

def update_poll(poll):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute("update polls set options_votes=(%s),emails=(%s) where id=(%s)",[Json(poll.options_votes),poll.emails,poll.id])
    conn.commit()
    cur.close()

def get_all_polls(auth_id):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute("select id,title from polls where auth_id=(%s)",(auth_id,))
    polls=cur.fetchall()
    cur.close()
    return polls






@click.command('initdb', help='Initialise the database')
@with_appcontext
def init_db_command():
    val = init_databse()
    if val == None:
        click.echo("Cannot Initialise Database")
    elif val == "Task Done":
        click.echo("Database Initialised")


def init_app(app):
    app.teardown_appcontext(close_connection)
    app.cli.add_command(init_db_command)