from flask.templating import DispatchingJinjaLoader
from flask_login.utils import login_required
from flask_socketio import send, emit, join_room, leave_room 
from Bonfire import app, db, socketio
from flask import render_template, url_for, redirect, flash, request
from Bonfire.forms import DeleteCommunityForm, JoinCommunityForm, LeaveCommunityForm, RegistrationForm, LoginForm, CreateCommunityForm
from Bonfire.models import *
from flask_login import login_user, logout_user, current_user
from time import localtime, strftime

@app.route("/")        # Home Page
@app.route("/home")
def homePage():
    return render_template("home.html")

@app.route("/about")    # About Section
def about():
    return render_template("about.html")

@app.route("/contact")    # Contact Section
def contactPage():
    return render_template("contact.html")

@app.route("/features")   # features
def featuresPage():
    return render_template("features.html")

@app.route("/communities", methods = ['GET','POST'])
@login_required
def communitiesPage():                
    form = CreateCommunityForm()
    deleteForm = DeleteCommunityForm()
    leaveForm = LeaveCommunityForm()
    joinForm = JoinCommunityForm()
    user_communities = list(current_user.myCommunities)

    if request.method=='POST':
        if form.validate_on_submit():
            created_community = Communities(form.community_name.data, form.community_description.data, form.community_admin.data)
            created_community.members.append(current_user)
            db.session.add(created_community)
            db.session.commit()
            return redirect(url_for('communitiesPage'))

        if deleteForm.validate_on_submit():
            deleteById = deleteForm.toBeDeleted.data
            # address_table = user_identifier('address', metadata, autoload=True)
            addresses = db.session.query(user_identifier).filter(user_identifier.c.c_id == deleteById)
            addresses.delete(synchronize_session=False)
            db.session.commit()
            delcomm = Communities.query.filter_by(id = deleteById).first()
            # print("\n\n\nprinted ",deleteById)
            if delcomm:
                db.session.delete(delcomm)
                db.session.commit()
        
        if joinForm.validate_on_submit():
            communityId = joinForm.toBeAdded.data
            community = Communities.query.filter_by(id = communityId).first()
            community.members.append(current_user)
            db.session.commit()
            return redirect(url_for('communitiesPage'))

        if leaveForm.validate_on_submit():
            leaveById = leaveForm.toBeLeft.data
            remRel = db.session.query(user_identifier).filter(user_identifier.c.c_id == leaveById)
            remRel.delete(synchronize_session=False)
            db.session.commit()
            return redirect(url_for('communitiesPage'))

        if form.errors != {}:
            for error_msg in form.errors.values():
                flash(f'Error occured: {error_msg}',category= 'danger')
        
    if request.method=='GET':
        allcmty = Communities.query.all()
        return render_template("communities.html", communities=allcmty, createForm = form,user_communities = user_communities, cur_usr = current_user, deleteForm = deleteForm, leaveForm = leaveForm, joinForm = joinForm )



@app.route("/register", methods = ['GET','POST'])
def registerPage():           # Registering of Users
    form = RegistrationForm()
    if form.validate_on_submit():
        created_user = User(form.username.data,form.email.data,form.password.data) # Registration Form
        db.session.add(created_user)
        db.session.commit()
        login_user(created_user)
        flash(f'You are logged in as {created_user.username}')
        return redirect(url_for('chat'))
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(f'Please fill the form correctly: {error_msg}',category= 'danger')
    return render_template("register.html", regForm = form)

@app.route("/login",methods = ['GET', 'POST'])
def loginPage():        # Log-in for Users
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        if attempted_user and attempted_user.checkpswrd(form.password.data):
            login_user(attempted_user)
            return redirect(url_for('chat'))
        else:
            flash('Username and password do not match', category= 'danger')

    return render_template('login.html', logForm =form)

@app.route("/logout")
def logoutPage():  # Log-out for Users
    logout_user()
    return redirect(url_for("homePage"))



@app.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():
    user_communities = list(current_user.myCommunities)

    # if not current_user.is_authenticated:
    #     flash('Please login', 'danger')
    #     return redirect(url_for('login'))

    return render_template('chat.html', username = current_user.username, user_communities = user_communities)

@socketio.on('message')
def message(data):
    # print("hello")
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': strftime('%H:%M %d-%m-%Y', localtime())}, room = data['room'])
    
@socketio.on('join')
def join(data):
    join_room(data['room'])  
    send({'msg': data['username'] + " has joined this community"}, room = data['room'])

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])  
    send({'msg': data['username'] + " has left this community"}, room = data['room'])

@app.errorhandler(404)     # Handling 404 error
def invalid_route(e): 
    return render_template("404error.html")

@app.route('/cnt', methods = ['GET','POST'])
def contact():        # Contact Us 
    if request.method=="POST":
        email = request.form['c-mail']
        mess = request.form['c-message']
        obj = ContactMess(email,mess)
        db.session.add(obj)
        db.session.commit()
    return redirect(url_for('contactPage'))

