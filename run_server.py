'''
    Most of this needs to be double checked for updated versions or new methods.
    We will probably want to just see if AWS can handle user login information for
    us to avoid any responsibility.
'''
import os
import json
import random

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

# Model Imports for storing and retrieving user, group, and library information
from model import user_manager
from model import group_manager
from model import library_manager

# email imports
import smtplib, ssl

#sms import
import boto3

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
  def __init__(self, username, password, id, access):
    self.id = id
    self.username = username
    self.password = password
    self.access = access

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
  return User.get_user(str(user_id))

'''
  Starting of server routes and controller section of the application
  NOTE: @app.route defines a url case from the client, as follows: https://<ip>:<port>/<route>
'''

# Root route -- Redirects to login page if not logged in
@app.route('/')
@login_required
def landing_page():
  return render_template('index.html', user=current_user.username, access_level=current_user.access)

# Landing Page -- Redirects to login page if not logged in
@app.route('/dashboard')
@login_required
def dashboard():
  return render_template('index.html', user=current_user.username, access_level=current_user.access)

# Login Page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = LoginForm()
  message = ""
  if(request.method == 'POST'):
    if(form.validate_on_submit()):
      user = form.username.data
      pw = form.password.data

      db = db_client()
      print(user)

      if(user_manager.validate_user(db, user, pw)):
        user_profile = user_manager.get_username_profile(db, user)
        user_access_level = user_manager.get_access_level(db, user)
        new_user = User(user, form.password.data, str(user_profile['_id']), user_access_level)
        user_list.append(new_user)
        login_user(new_user, remember=form.remember.data)
        return redirect(url_for('dashboard', user=current_user.username, access_level=current_user.access))
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

      #unique_number = ''  #'#' + str(random.randrange(10000)).zfill(4)
      user_data = [form.username.data, form.password.data, form.email.data, form.position.data, form.phone.data]
      db = db_client()
      user_manager.add_user(db, user_data)

      print("User: " + user_data[0] + " successfully created...")
      return redirect(url_for('signin'))
    else:
      print("INVALID FORM")
      return redirect(url_for('signin'))
  else:
    return redirect(url_for('signin'))

# Send SMS
@app.route('/send_sms', methods=['GET'])
@login_required
def send_sms():
  if(request.method == 'GET'):
    client = boto3.client('sns')
    phone_number='18322740571'
    message='AggieSTEM sms test'
    client.publish(PhoneNumber=phone_number, Message=message)
    return("SMS SENT")

# Send Emails
@app.route('/send_email', methods=['GET'])
@login_required
def send_email():
  if(request.method == 'GET'):
    port = 465
    password = "ASECRET"

    context = ssl.create_default_context()
    sender = "aggiestem.dl@gmail.com"
    reciever = "theinformantherod@gmail.com"
    smtp_server = "smtp.gmail.com"


    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
      server.login(sender, password)
      server.sendmail(sender, reciever, "HELLO IT WORKED")
    return("EMAIL SENT")

# User Profile
@app.route('/userProfile', methods=['GET', 'POST'])
@login_required
def userProfile():
  if(request.method == 'GET'):
    username = current_user.username
    db = db_client()
    userdata = user_manager.get_username_profile(db, username)
    phonenumber = userdata['phone']
    email = userdata['email']
    position = userdata['position']
    if(position == "D"):
      position = "Director"
    elif(position == "S"):
      position = "Senior Doc"
    else:
      position = "Researcher"
    return render_template('user_profile.html', user=username,
      email= email, phonenumber=phonenumber, position = position)
  elif(request.method == 'POST'):
    data = {}
    return render_template('user_profile.html', data=data)
  else:
    return render_template('user_profile.html', data=data, error="ERROR: Try Again")

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

# Recover Password Page
@app.route('/request_data_form', methods=['GET', 'POST'])
@login_required
def request_data_form():
  form = ForgotPw()
  if(request.method == 'GET'):
    return render_template('request_data_form.html', form=form, user=current_user.username)
  elif(request.method == 'POST'):
    print("POST FROM REQUEST DATA FORM")
    return render_template('request_data_form.html', form=form, user=current_user.username)
  else:
    return render_template('signin.html', form=form, error="TEST")

@app.route('/table_reload', methods=['GET', 'POST'])
@login_required
def table_reload():
  print("TEST AJAX RELOAD")
  db = db_client()
  group_user_list = user_manager.get_all_users(db)
  # TODO: Fix get_all_groups()
  temp = []
  for row in group_user_list:
    user_data = {}
    user_data['uid'] = str(row['_id'])
    user_data['username'] = row['username']
    user_data['position'] = row['position']
    user_data['access_level'] = row['access_level']
    user_data['email'] = row['email']
    user_data['phone'] = row['phone']
    user_data['groups'] = 'TODO'#group_manager.get_all_groups(db, str(row['_id']))
    user_data['last_login'] = row['login_timestamp'][0:16]
    user_data['deleted'] = str(row['deleted'])
    temp.append(user_data)
  data = {}
  data['data'] = temp
  return data


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
    db = db_client()
    if(user_manager.get_access_level(db, current_user.username) < 2):
      return redirect(url_for('dashboard', user=current_user.username, access_level=current_user.access))

    group_user_list = user_manager.get_all_users(db)
    # TODO: Fix get_all_groups()
    temp = []
    for row in group_user_list:
      user_data = {}
      user_data['uid'] = str(row['_id'])
      user_data['username'] = row['username']
      user_data['position'] = row['position']
      user_data['access_level'] = row['access_level']
      user_data['email'] = row['email']
      user_data['phone'] = row['phone']
      user_data['groups'] = 'TODO'#group_manager.get_all_groups(db, str(row['_id']))
      user_data['last_login'] = row['login_timestamp'][0:16]
      user_data['deleted'] = str(row['deleted'])
      temp.append(user_data)
    data = {}
    data['data'] = temp
    return render_template('manage_users.html', user=current_user.username, data = data, access_level=current_user.access)
  elif(request.method == 'POST'):
    db = db_client()
    post_args = json.loads(request.values.get("data"))
    print("POST REQUEST")
    print(post_args)
    user_id = next(iter(post_args['data']))
    if(post_args['action'] == "remove"):
      result = user_manager.delete_user(db, user_id)
      if(result == False):
        print("FAILED")
      return {}
    elif(post_args['action'] == "unremove"):
      print("HERE UNREMOVE USER")
      #TODO: fix the post dat sent to match others
      user_id = post_args['data']['uid']
      user_manager.update_user(db, user_id, {"deleted": False})
      return {}
    else:
      response_data = {}
      response_data['data'] = []
      post_args['data'][user_id]['uid'] = user_id
      response_data['data'].append(post_args['data'][user_id])

      new_user_data = {}
      new_user_data['access_level'] = int(response_data['data'][0]['access_level'])
      new_user_data['position'] = response_data['data'][0]['position']

      user_manager.update_user(db, user_id, new_user_data)
      return response_data
  else:
    print("SHIT")
    return render_template('index.html', user=current_user.username, error="TEST", access_level=current_user.access)

@app.route('/manage_groups', methods=['GET', 'POST'])
@login_required
def manage_groups():
  db = db_client()
  if(user_manager.get_access_level(db, current_user.username) < 2):
    return redirect(url_for('dashboard', user=current_user.username, access_level=current_user.access))
  if(request.method == 'GET'):
    '''
    TODO: Get all users and display on page
    MODEL TEAM: Handle requests to function in group_manager.py

    TO GET PARARMS BASED ON ID:

    username = request.args.get('ID')
    groups = group_manage.<method>

    This can change based on a version of python, so could be request(s)
    '''
    return render_template('manage_groups.html', user=current_user.username, access_level=current_user.access)
  elif(request.method == 'POST'):
    return render_template('manage_groups.html', user=current_user.username, access_level=current_user.access)
  else:
    return render_template('index.html', user=current_user.username, access_level=current_user.access, error="TEST")

@app.route('/message_users', methods=['GET', 'POST'])
@login_required
def message_users():
  # TODO: CHECK IF USER IS ADMIN
  if(request.method == 'GET'):
    '''
    TODO:
    MODEL TEAM:

       1) group_manager.get_all_groups(db, username)
    '''
    db = db_client()
    db = db_client()
    if(user_manager.get_access_level(db, current_user.username) != 3):
      return redirect(url_for('dashboard', user=current_user.username, access_level=current_user.access))
    message_user_list = user_manager.get_all_users(db)

    groups = ["Camp A", "Camp B", "Camp C", "Camp D"]
    temp = []
    i = 0
    for row in message_user_list:
      user_data = {}
      user_data['uid'] = str(row['_id'])
      user_data['username'] = row['username']
      user_data['phone'] = row['phone']
      user_data['groups'] = groups[i] #Make sure it works with multigroups/user
      temp.append(user_data)
      i += 1
      if(i>3):
        i=0
    data = {}
    data['data'] = temp

    return render_template('message_users.html', user=current_user.username, data = data, groups = list(groups),
      access_level=current_user.access)
  elif(request.method == 'POST'):
    return render_template('message_users.html', user=current_user.username, access_level=current_user.access)
  else:
    return render_template('index.html', user=current_user.username, error="TEST", access_level=current_user.access)

def db_client():
  try:
    client = pymongo.MongoClient("mongodb://128.194.140.214:27017/")
    #client = pymongo.MongoClient("mongodb://localhost:27017/")
  except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)
  db = client["AggieSTEM"]
  return db

if __name__ == "__main__":
  IP = '128.194.140.214'
  #IP = '127.0.0.1'
  app.run(host = os.getenv('IP',IP), port=int(os.getenv('PORT',8080)), debug=True)
