from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref
from Bonfire import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#table to store many to many relations
user_identifier = db.Table('user_identifier',
    db.Column('c_id', db.Integer, db.ForeignKey('communities.id')),
    db.Column('u_id', db.Integer, db.ForeignKey('users.id'))
)

#user model
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

#community model
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

#contact form model
class ContactMess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mess_mail = db.Column(db.String(length = 100))
    mess_text = db.Column(db.String(length = 500))

    def __init__(self,mail,mess):
        self.mess_mail = mail 
        self.mess_text = mess