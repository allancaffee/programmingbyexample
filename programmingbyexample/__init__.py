import logging

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import flask as f
from sqlalchemy.exceptions import IntegrityError

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            db.session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    db.session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/projects/', methods=['GET'])
@app.route('/projects/pages/<int:page_num>/')
def project_pages(page_num=1):
    projects = db.session.query(model.Project)
    page_links = [url_for('project_pages', page_num=i)
                  for i in range(page_num, page_num+10)]
    return render_template('show-projects.html', projects=projects)

@app.route('/projects/new', methods=['GET'])
def project_new():
    return render_template('edit-project.html', project=None)

@app.route('/projects/<int:id>/edit')
def project_edit(id):
    project = model.Project.query.get_or_404(id)
    return render_template('edit-project.html', project=project)

@app.route('/projects/', methods=['POST'])
def project_submit():
    p = model.Project(name=request.form['name'],
                      oneliner=request.form['oneliner'],
                      description=request.form['description'],
                      )
    db.session.add(p)
    try:
        db.session.commit()
        flash('Created a new project!')
        return redirect(url_for('project_pages'))
    except IntegrityError:
        db.session.rollback()
        flash('A project by that name already exists')
        return redirect(url_for('project_edit'))


@app.route('/projects/<int:id>')
def project_get(id):
    project = model.Project.query.get_or_404(id)
    return render_template('project-page.html', project=project)
    
