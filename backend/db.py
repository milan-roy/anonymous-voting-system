import psycopg2 
import click 
from flask import current_app, g
from flask.cli import with_appcontext
import datetime
from . import forms
from flask_bcrypt import Bcrypt


def get_conn():
    if 'conn' not in g:
        dbname=current_app.config['DATABASE']
        try:
            g.conn=psycopg2.connect(f"dbname={dbname}")
        except:
            return None
    return g.conn

def close_connection(e=None):
    conn=g.pop('conn',None)
    if conn is not None:
        conn.close()

def get_bcrypt():
    if 'bcryt' not in g:
        g.bcrypt=Bcrypt(current_app)
    return g.bcrypt

def init_databse():
    conn=get_conn()
    if conn is None:
        return conn
    sql_file=current_app.open_resource('static/sql_code.sql')
    sql_code= sql_file.read()
    cur=conn.cursor()
    cur.execute(sql_code)
    conn.commit()
    cur.close()
    close_connection()
    return "Task Done"

def adds_user(form):
    conn=get_conn()
    cur=conn.cursor()
    bcrypt=get_bcrypt()
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    cur.execute("INSERT INTO users (username,email,password,last_login) VALUES(%s,%s,%s,%s)",[form.username.data,form.email.data,hashed_password,datetime.datetime.now()])
    conn.commit()
    cur.close()

def does_username_exist(username):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute("SELECT username from users")
    username_list=cur.fetchall()
    cur.close()
    temp_tuple=(username,)
    return temp_tuple in username_list

def does_email_exist(email):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute("SELECT email from users")
    email_list=cur.fetchall()
    cur.close()
    temp_tuple=(email,)
    return temp_tuple in email_list

def does_email_and_password_match(email,password):
    conn=get_conn()
    cur=conn.cursor()
    bcrypt=get_bcrypt()
    cur.execute("SELECT password from users where email=(%s)",(email,))
    hashed_password=cur.fetchone()[0]
    cur.close()
    return bcrypt.check_password_hash(hashed_password,password)

def filter_user(user_id=None,email=None,username=None):
    from. import models
    conn=get_conn()
    cur=conn.cursor()
    if user_id :
        cur.execute("SELECT id,username,email,image_file,last_login from users where id=(%s)",(user_id,))
    if email:
        cur.execute("SELECT id,username,email,image_file,last_login from users where email=(%s)",(email,))
    if username:
        cur.execute("SELECT id,username,email,image_file,last_login from users where username=(%s)",(username,))
    temp=cur.fetchone()
    cur.close()
    user=models.User()
    user.username=temp[1]
    user.id=temp[0]
    user.email=temp[2]
    user.image_file=temp[3]
    user.last_login=temp[4]
    return user

def update_last_login(email):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute("update users set last_login=(%s) where email=(%s)",[datetime.datetime.now(),email])
    cur.close()

@click.command('initdb', help='Initialise the database')
@with_appcontext
def init_db_command():
    val=init_databse()
    if val==None:
        click.echo("Cannot Initialise Database")
    elif val=="Task Done":
        click.echo("Database Initialised")

def init_app(app):
    app.teardown_appcontext(close_connection)
    app.cli.add_command(init_db_command)
  
    