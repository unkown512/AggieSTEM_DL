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

# Model Imports for storing and retrieving user information
from model import user_manager

# Start of server
app = Flask(__name__)
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
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
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
      '''
      TODO MODEL TEAM: Change the 'validate_user' function to interact with db and validate user
      NOTE: Once DB is setup, remove the TEMP_LOGIN_DB variable everywhere~!!!!
      '''
      if(user_manager.validate_user(user, pw, TEMP_LOGIN_DB)):
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
      user_manager.add_user(form.username.data, form.password.data)
      TEMP_LOGIN_DB.append([form.username.data, form.password.data])
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
    data = {}
    return render_template('userProfile.html', data=data)
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

# Recover Username Page
@app.route('/recov_username', methods=['GET', 'POST'])
def recov_username():
  form = ForgotUser()
  if(request.method == 'GET'):
    return render_template('recov_username.html', form=form)
  elif(request.method == 'POST'):
    return render_template('recov_username.html', form=form)
  else:
    return render_template('signin.html', form=form)
    
# Recover Password Page
@app.route('/recov_pw', methods=['GET', 'POST'])
def recov_pw():
  form = ForgotPw()
  if(request.method == 'GET'):
    return render_template('recov_pw.html', form=form)
  elif(request.method == 'POST'):
    return render_template('recov_pw.html', form=form)
  else:
    return render_template('signin.html', form=form)

if __name__ == "__main__":
  app.run(host = os.getenv('IP','0.0.0.0'), port=int(os.getenv('PORT',8080)), debug=True)
