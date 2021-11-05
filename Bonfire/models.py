from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref
from Bonfire import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

user_identifier = db.Table('user_identifier',
    db.Column('c_id', db.Integer, db.ForeignKey('communities.id')),
    db.Column('u_id', db.Integer, db.ForeignKey('users.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(),primary_key = True)
    username = db.Column(db.String(length = 30), nullable = False, unique = True)
    emailId = db.Column(db.String(length = 50), nullable = False, unique = True)
    password_hash = db.Column(db.String(length = 64), nullable = False)
    

    def __init__(self, username, emailId, password):
        self.username = username
        self.emailId = emailId
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def __repr__(self):
        return f'User {self.username}'

    def checkpswrd(self, attempted_pswrd):
        return bcrypt.check_password_hash(self.password_hash,attempted_pswrd)

class Communities(db.Model):
    __tablename__ = "communities"
    id = db.Column(db.Integer, primary_key=True)
    community_name = db.Column(db.String(length = 100), nullable = False, unique = True)
    community_description = db.Column(db.String(length = 300), nullable = False)
    community_admin = db.Column(db.Integer(), nullable = False)
    members = db.relationship("User", secondary = user_identifier, backref = db.backref("myCommunities", lazy = 'dynamic'))

    def __init__(self, community_name, community_description, community_admin):
        self.community_name = community_name
        self.community_description = community_description
        self.community_admin = community_admin


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community_name = db.Column(db.String(length = 100))
    channel_name = db.Column(db.String(length = 100))
    date_posted = db.Column(db.String(length = 30))
    time_posted = db.Column(db.String(length = 30))
    name = db.Column(db.String(length = 100), default='')
    content = db.Column(db.String(length = 500), default='')  