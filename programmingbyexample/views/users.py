"""User management module."""

from flask import Module, request, session, g, redirect, url_for, \
     abort, render_template, flash

import model
from model import db

users = Module(__name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != users.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != users.config['PASSWORD']:
            error = 'Invalid password'
        else:
            db.session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@users.route('/logout')
def logout():
    db.session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
