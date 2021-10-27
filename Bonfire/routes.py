from flask.templating import DispatchingJinjaLoader
from flask_login.utils import login_required
import socketio
from Bonfire import app, db, socketio
from flask import render_template, url_for, redirect, flash,request
from Bonfire.forms import RegistrationForm, LoginForm
from Bonfire.models import *
from flask_login import login_user, logout_user
from flask_socketio import SocketIO,send

@app.route("/")
@app.route("/home")
def homePage():
    return render_template("home.html")

@app.route("/contact")
def contactPage():
    return render_template("contact.html")

@app.route("/features")
def featuresPage():
    return render_template("features.html")

@app.route("/communities")
@login_required
def communitiesPage():
    allcmty = Communities.query.all()
    return render_template("communities.html",communities=allcmty)

@app.route("/addcommunity",methods= ['GET','POST'])
@login_required
def addcommunity():
    if request.method=='POST':
        check = Communities(community_name=request.form.get("c_name"))
        db.session.add(check)
        db.session.commit()
        return redirect(url_for('communitiesPage'))
    return render_template("addcommunity.html")


@app.route("/register", methods = ['GET','POST'])
def registerPage():
    form = RegistrationForm()
    if form.validate_on_submit():
        created_user = User(form.username.data,form.email.data,form.password.data)
        db.session.add(created_user)
        db.session.commit()
        login_user(created_user)
        flash(f'You are logged in as {created_user.username}')
        return redirect(url_for('homePage'))
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(f'Please fill the form correctly: {error_msg}',category= 'danger')
    return render_template("register.html", regForm = form)

@app.route("/login",methods = ['GET', 'POST'])
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        if attempted_user and attempted_user.checkpswrd(form.password.data):
            login_user(attempted_user)
            flash(f'Logged in as {attempted_user.username}', category= 'success')
            return redirect(url_for('homePage'))
        else:
            flash('Username and password do not match', category= 'danger')

    return render_template('login.html', logForm =form)

@app.route("/logout")
def logoutPage():
    logout_user()
    return redirect(url_for("homePage"))

@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    send(data)

@app.route("/chat/<int:no>")
def chat(no):
    chat_community = Communities.query.filter_by(id=no).first()
    return render_template("chat1.html",ch_no=chat_community)