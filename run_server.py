'''
    Most of this needs to be double checked for updated versions or new methods.
    We will probably want to just see if AWS can handle user login information for
    us to avoid any responsibility.
'''
import os

# Flask Server Imports
from flask import Flask
from flask import request
from flask import render_template, redirect
from flask import url_for
from flask import send_file
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template, mobilized
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

# Imports for forms and login mods
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from wtforms import ValidationError

# Model Imports for storing and retrieving user information
from model import user_manager

# MongoDB imports
import pymongo

# Start of server
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

Mobility(app)
Bootstrap(app)
app.config['SECRET_KEY'] = user_manager.unique_key()
'''
    user_list needs to be changed to be inside a class/db
    TEMP_LOGIN_DB is temporary for testing the login system.
'''
# Initlaize login_manager
def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'signin'
    user_list = list()
    TEMP_LOGIN_DB = [] # Remove with insert into database
    return(login_manager, user_list, TEMP_LOGIN_DB)

(login_manager, user_list, TEMP_LOGIN_DB) = init_login_manager(app)

'''
  Class User: Managers user methods for session
  Class LoginForm: Generates the flask wtf form for the signin view and input checking
  Class RegisterForm: Generates the flask wtf form for the signup view and input checking
  Class ForgotUser: Generates the flask wtf form for the forgot user action
  Class ForgotPw: Generates the flask wtf form for the forgot password action
'''
class User(UserMixin):
    def __init__(self, username, password, id):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get_user(user_id):
        for xuser in user_list:
            if(xuser.id == user_id):
                return xuser

    @staticmethod
    def remove_user(user_name):
        for xuser in user_list:
            if(xuser.username == user_name):
                user_list.remove(xuser)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    #TODO: Password length should be much longer than 80
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    #phone number
    username = StringField('Username <p class="text-info">First Initial + Last Name<p>'
      , validators=[InputRequired(), Length(min=4, max=15)])
    position = SelectField('Position', validators=[InputRequired()], choices=[('',''),('D','Director'),('S','Senior Doc'),('R','Researcher')])
    phone = StringField('Phone', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    conf_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=250)])
    conf_email = StringField('Confirm Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=250)])

class ForgotUser(FlaskForm):
  email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=250)])
  security_question = StringField('Secruity Question', validators=[InputRequired(), Length(min=4, max=80)])

class ForgotPw(FlaskForm):
  username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
  email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=250)])
  security_question = StringField('Secruity Question', validators=[InputRequired(), Length(min=4, max=80)])

# Get function for user during session
@login_manager.user_loader
def load_user(user_id):
  return User.get_user(int(user_id))

'''
  Starting of server routes and controller section of the application
  NOTE: @app.route defines a url case from the client, as follows: https://<ip>:<port>/<route>
'''

# Root route -- Redirects to login page if not logged in
@app.route('/')
@login_required
def landing_page():
  return render_template('index.html', user=current_user.username)

# Landing Page -- Redirects to login page if not logged in
@app.route('/dashboard')
@login_required
def dashboard():
  return render_template('index.html', user=current_user.username)

# Login Page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = LoginForm()
  message = ""
  if(request.method == 'POST'):
    if(form.validate_on_submit()):
      user = form.username.data
      pw = form.password.data
      try:
        client = pymongo.MongoClient("mongodb://128.194.140.214:27017/")
      except pymongo.errors.ServerSelectionTimeoutError as err:
        print(err)
      db = client["AggieSTEM"]

      if(user_manager.validate_user(db, user, pw)):
        user_list.append(User(user, form.password.data, 1))
        new_user = User(User, form.password.data, 1)
        login_user(new_user, remember=form.remember.data)
        return redirect(url_for('dashboard', user=current_user.username))
      else:
        message = "Incorrect username or password"
    else:
       message = "Invalid Form"
  elif(request.method == 'GET'):
    render_template("signin.html", form=form)
  return render_template("signin.html", form=form, error=message)

# Registration page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = RegisterForm()
  if(request.method == 'GET'):
    return render_template('signup.html', form=form)
  elif(request.method == 'POST'):
    if(form.validate_on_submit()):
      '''
        TODO MODEL TEAM: Update the 'add_user' function to
        insert into DB and create salts/hash/encryption for user etc...

        NOTE: TEMP_LOGIN_DB WILL BE REMOVED ONCE 'user_manager' is complete!!!
      '''
      user_data = [form.username.data, form.password.data, form.email.data,
        form.position.data, form.phone.data]
      try:
        client = pymongo.MongoClient("mongodb://128.194.140.214:27017/")
      except pymongo.errors.ServerSelectionTimeoutError as err:
        print(err)
      db = client["AggieSTEM"]
      user_manager.add_user(db, user_data)
      return redirect(url_for('signin'))
    else:
      print("INVALID FORM")
      return redirect(url_for('signin'))
  else:
    return redirect(url_for('signin'))

# User Profile
@app.route('/userProfile', methods=['GET', 'POST'])
@login_required
def userProfile():
  if(request.method == 'GET'):
    username = current_user.username
    try:
      client = pymongo.MongoClient("mongodb://128.194.140.214:27017/")
    except pymongo.errors.ServerSelectionTimeoutError as err:
      print(err)
    db = client["AggieSTEM"]
    userdata = user_manager.get_user_profile(db, username)
    phonenumber = userdata['phone']
    email = userdata['email']
    position = userdata['position']
    if(position == "D"):
      position = "Director"
    elif(position == "S"):
      position = "Senior Doc"
    else:
      position = "Researcher"
    return render_template('userProfile.html', user=username,
      email= email, phonenumber=phonenumber, position = position)
  elif(request.method == 'POST'):
    data = {}
    return render_template('userProfile.html', data=data)
  else:
    return render_template('userProfile.html', data=data, error="ERROR: Try Again")

# Logout User
@app.route('/logout', methods=['GET'])
@login_required
def logout():
  User.remove_user(current_user.username)
  logout_user()
  return redirect(url_for('signin'))

@app.route('/loadpdf')
@login_required
def loadpdf():
  directory = os.path.join(APP_ROOT, 'data/')
  pdf_name = "data_request_form.pdf"
  docx_name = "data_request_form.docx"
  dest = "/".join([directory, pdf_name])
  return send_file(dest)

# Recover Username Page
@app.route('/recov_username', methods=['GET', 'POST'])
def recov_username():
  form = ForgotUser()
  if(request.method == 'GET'):
    return render_template('recov_username.html', form=form)
  elif(request.method == 'POST'):
    return render_template('recov_username.html', form=form)
  else:
    return render_template('signin.html', form=form, error="TEST")

# Recover Password Page
@app.route('/recov_pw', methods=['GET', 'POST'])
def recov_pw():
  form = ForgotPw()
  if(request.method == 'GET'):
    return render_template('recov_pw.html', form=form)
  elif(request.method == 'POST'):
    return render_template('recov_pw.html', form=form)
  else:
    return render_template('signin.html', form=form, error="TEST")

@app.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
  if(request.method == 'GET'):
    '''
    TODO:
    MODEL TEAM:

       1) Finish user_manager.last_login(db,user)

       2) group_manager.get_all_groups(db, username)

    username = request.args.get('ID')

    '''
    try:
      client = pymongo.MongoClient("mongodb://128.194.140.214:27017/")
    except pymongo.errors.ServerSelectionTimeoutError as err:
      print(err)
    db = client["AggieSTEM"]
    temp = user_manager.get_all_users(db)
    data = []
    for row in temp:
      tmp = []
      tmp.append(row['username'])
      tmp.append(row['position'])
      tmp.append(row['access_level'])
      tmp.append(row['email'])
      tmp.append(row['phone'])
      tmp.append("bob")
      tmp.append("TBA")
      data.append(tmp)
    return render_template('manage_users.html', user=current_user.username, data = data)
  elif(request.method == 'POST'):
    return render_template('manage_users.html', user=current_user.username)
  else:
    return render_template('index.html', user=current_user.username, error="TEST")

@app.route('/manage_groups', methods=['GET', 'POST'])
@login_required
def manage_groups():
  if(request.method == 'GET'):
    '''
    TODO: Get all users and display on page
    MODEL TEAM: Handle requests to function in group_manager.py

    TO GET PARARMS BASED ON ID:

    username = request.args.get('ID')
    groups = group_manage.<method>

    This can change based on a version of python, so could be request(s)
    '''
    return render_template('manage_groups.html', user=current_user.username)
  elif(request.method == 'POST'):
    return render_template('manage_groups.html', user=current_user.username)
  else:
    return render_template('index.html', user=current_user.username, error="TEST")

@app.route('/message_users', methods=['GET', 'POST'])
@login_required
def message_users():
  # TODO: CHECK IF USER IS ADMIN
  if(request.method == 'GET'):
    '''
    TODO:
    MODEL TEAM:

       1) group_manager.get_all_groups(db, username)

    username = request.args.get('ID')

    '''
    try:
      client = pymongo.MongoClient("mongodb://128.194.140.214:27017/")
    except pymongo.errors.ServerSelectionTimeoutError as err:
      print(err)
    db = client["AggieSTEM"]
    temp = user_manager.get_all_users(db)
    # TODO: make subarray of relevent columns, username[0], phonenumber[4], groups[5]
    data = []
    groups = ["bob", "jan", "don"]
    for row in temp:
      tmp = []
      tmp.append(row['user_id'])
      tmp.append(row['username'])
      tmp.append(row['phone'])
      tmp.append("bob") #Todo replace with group_manager.get_all_groups(db, username)
      data.append(tmp)

    return render_template('message_users.html', user=current_user.username, data = data, groups = list(groups))
  elif(request.method == 'POST'):
    return render_template('message_users.html', user=current_user.username)
  else:
    return render_template('index.html', user=current_user.username, error="TEST")


if __name__ == "__main__":
  IP = '128.194.140.214'
  app.run(host = os.getenv('IP',IP), port=int(os.getenv('PORT',8080)), debug=True)
