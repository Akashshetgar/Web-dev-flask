from flask_bcrypt import Bcrypt
from Bonfire import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(),primary_key = True)
    username = db.Column(db.String(length = 30), nullable = False, unique = True)
    emailId = db.Column(db.String(length = 50), nullable = False, unique = True)
    password_hash = db.Column(db.String(length = 64), nullable = False)
    #memberOf = db.relationship....to know if a user belongs to a community

    def __init__(self, username, emailId, password):
        self.username = username
        self.emailId = emailId
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def __repr__(self):
        return f'User {self.username}'

    def checkpswrd(self, attempted_pswrd):
        return bcrypt.check_password_hash(self.password_hash,attempted_pswrd)
    