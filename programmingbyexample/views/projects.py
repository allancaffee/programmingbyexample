"""Project management views."""

import re

from flask import Module, request, session, g, redirect, url_for, \
     abort, render_template, flash
from formalchemy import FieldSet
from formalchemy.base import ModelRenderer
from sqlalchemy.exceptions import IntegrityError

import model
from model import db

projects = Module(__name__)

project_form = FieldSet(model.Project)
project_form.configure(options=[
    project_form.description.textarea('70x20'),
    project_form.rating.hidden(),
    ])


model_re = re.compile('(\w+)-(\d*)-.*')

def split_model(fields):
    """Find the (ModelClass, id) of the first matching form field.

    The field names are like ModelClass-id-FieldName
    """
    for field_name, value in fields.items():
        m = model_re.match(field_name)
        if m:
            model_name, id = m.groups()
            if not id:
                id = None
            else:
                id = int(id)

            klass = getattr(model, model_name)
            return (klass, id)

def sync_form(Form, fields):
    klass, id = split_model(fields)
    if id is None:
        inst = klass()
    else:
        inst = klass.query.get(id)

    form = Form.bind(inst, data=fields)
    if fields and form.validate():
        form.sync()

        if id is None:
            db.session.add(inst)
        else:
            db.session.update(inst)


@projects.route('/projects/', methods=['GET'])
@projects.route('/projects/pages/<int:page_num>/')
def pages(page_num=1):
    projects = db.session.query(model.Project)
    page_links = [url_for('projects.pages', page_num=i)
                  for i in range(page_num, page_num+10)]
    return render_template('show-projects.html', projects=projects)


@projects.route('/projects/new', methods=['GET'])
def new():
    return render_template('edit-project.html', field_set=project_form)


@projects.route('/projects/<int:id>/edit')
def edit(id):
    fs = project_form.bind(model.Project.query.get_or_404(id))
    return render_template('edit-project.html', field_set=fs)


@projects.route('/projects/', methods=['POST'])
def submit(id=None):
    print request.form

    sync_form(project_form, request.form)

    try:
        db.session.commit()
        flash('Created a new project!')
        return redirect(url_for('projects.pages'))
    except IntegrityError:
        db.session.rollback()
        flash('A project by that name already exists')
        return redirect(url_for('projects.edit'))


@projects.route('/projects/<int:id>/')
def get(id):
    project = model.Project.query.get_or_404(id)
    return render_template('project-page.html', project=project)
