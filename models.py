from flask_marshmallow import Marshmallow
from Rest import app
from flask_sqlalchemy import SQLAlchemy
import click
from werkzeug.security import generate_password_hash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
import random

class Article(db.Model): 
       __tablename__ = 'article'
       id     = db.Column(db.Integer, primary_key=True)
       title   = db.Column(db.String(180))
       slug = db.Column(db.String(180))
       content_text  = db.Column(db.String(180))
       def __init__(self, title, content_text):
           self.title = title
           self.slug = f'{title}-{random.random()}'.replace(' ', '-').replace(':','-')
           self.content_text = content_text

       def __repr__(self):
        return '<Article {},{},{} >'.format(self.slug,
            self.content_text,self.title)

class UserManajement(db.Model):
      id       = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(50), unique=1)
      password = db.Column(db.String(60))
      role_id = db.Column(db.Integer)
      def __init__(self, username, password):
          self.password = generate_password_hash(password)
          self.role_id = 2
          self.username = str(username).lower()
      def __repr__(self):
          return "<UserManajement {},{}>".format(self.username, self.password)

ma = Marshmallow(app)
class AricleSeriallizer(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ['id', 'title', 'slug', 'content_text']

class UserSerial(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ['username', 'role_id']


@app.cli.command("migrate")
@click.argument("name")
def migration(name):
    if name == 'create':
       db.create_all()
       print('Success Create database')
    elif name == 'drop':
        db.drop_all()
        print('Success Drop database')
    else:
        print('Not Four')