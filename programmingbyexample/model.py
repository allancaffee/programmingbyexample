import creoleparser
import flask
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy import (Column, Integer, String, ForeignKey,
                        Unicode, Index, DDL, DateTime, Boolean)
from werkzeug import generate_password_hash, check_password_hash

class Policies(object):
    """A SQLAlchemy mix-in for base policies."""

    __table_args__ = {'mysql_engine':'InnoDB',
                      'mysql_charset':'utf8'}

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
Base = db.Model


class User(Base, Policies):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(50))


class ProgrammingLanguage(Base, Policies):
    __tablename__ = 'programming_languages'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(50), nullable=False)


class Project(Base, Policies):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    oneliner = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=False)
    rating = Column(Integer, nullable=False, default=0)

    @property
    def link(self):
        """Get a link to the project page.

        FIXME: It's kind of terrible having this here.
        """

        return '<a href="%s">%s</a>' % (flask.url_for('project_get', id=self.id),
                                        self.name)

    @property
    def rendered_description(self):
        """The description after it's been rendered to html."""

        return creoleparser.creole2html(self.description)


class Implementation(Base, Policies):
    __tablename__ = 'implementations'

    id = Column(Integer, nullable=False, primary_key=True)
    
    language_id = Column(Integer, ForeignKey(ProgrammingLanguage.id))
    language = db.relation('ProgrammingLanguage',
                           primaryjoin=(language_id == ProgrammingLanguage.id))
    rating = Column(Integer, nullable=False)

    project_id = Column(Integer, ForeignKey(Project.id))
    project = db.relation(Project, primaryjoin=(project_id == Project.id))

    creator_id = Column(Integer, ForeignKey(User.id))
    creator = db.relation('User', primaryjoin=(creator_id == User.id))
