import psycopg2 
import click 
from flask import current_app, g
from flask.cli import with_appcontext
import datetime

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
    file1=current_app.open_resource('static/sql_code.sql')
    sql_code= file1.read()
    cur=conn.cursor()
    cur.execute(sql_code)
    conn.commit()
    cur.close()
    close_connection()
    return "Task Done"

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
  
    