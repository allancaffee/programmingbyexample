import logging

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

import model
from model import db


DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('PBE_SETTINGS', silent=True)
db.create_all()

# Register additional modules.
from programmingbyexample.views.projects import projects
from programmingbyexample.views.users import users
app.register_module(projects)
app.register_module(users)

@app.route('/')
def root():
    return render_template('welcome.html')

