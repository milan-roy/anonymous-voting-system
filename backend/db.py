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
    bcrypt=Bcrypt(current_app)
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    cur.execute("INSERT INTO users (username,email,password,last_login) VALUES(%s,%s,%s,%s)",[form.username.data,form.email.data,hashed_password,datetime.datetime.now()])
    conn.commit()
    cur.close()

def does_username_exist(username):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute("SELECT username from users")
    username_list=cur.fetchall()
    conn.commit()
    cur.close()
    temp_tuple=(username,)
    return temp_tuple in username_list

def does_email_exist(email):
    conn=get_conn()
    cur=conn.cursor()
    cur.execute("SELECT email from users")
    email_list=cur.fetchall()
    conn.commit()
    cur.close()
    temp_tuple=(email,)
    return temp_tuple in email_list



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
  
    