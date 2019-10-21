'''
    Most of this needs to be double checked for updated versions or new methods.
    We will probably want to just see if AWS can handle user login information for 
    us to avoid any responsibility. 
'''
import os

from flask import Flask
from flask import request
from flask import render_template, redirect
from flask import url_for
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template, mobilized
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)
#app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)
Mobility(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'


# TODO: CHANGE THIS 
app.config['SECRET_KEY'] = 'ASECRETYOUFOOL'


'''
    
    user_list needs to be changed to be inside a class/db
    TEMP_LOGIN_DB is temporary for testing the login system.
'''
user_list = list()
TEMP_LOGIN_DB = []

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
    
    
@login_manager.user_loader
def load_user(user_id):
    return User.get_user(int(user_id))

'''

   Everything below this defines the url routes for the website

'''
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if(form.validate_on_submit()):
        user = form.username.data
        pw = form.password.data
        #TODO MODEL: This if statement will be changed with the salt/encryption or etc to valid user information
        #Once validated, leave the rest the same with correct data
        if(user == "Andy" and pw == "Andy1234" or (user == TEMP_LOGIN_DB[0][0] and pw == TEMP_LOGIN_DB[0][1])):
          user_list.append(User(user, form.password.data, 1))
          new_user = User(User, form.password.data, 1)
          login_user(new_user, remember=form.remember.data)
          return redirect(url_for('dashboard'))
        else:
          message = "Incorrect username or password"
    message = "Invalid Form" 
    return render_template("signin.html", form=form, error=message)
 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if(request.method == 'GET'):
        return render_template('signup.html', form=form)
    elif(request.method == 'POST'):
      if(form.validate_on_submit()):
        #TODO MODEL: Insert into the DB and create salt and etc....
        TEMP_LOGIN_DB.append([form.username.data, form.password.data])
        return redirect(url_for('signin'))
      else:
        print("INVALID FORM")
        return redirect(url_for('signin'))
    else:
      return redirect(url_for('signin'))
  
@app.route('/recov_username', methods=['GET', 'POST'])
def recov_username():
    form = RegisterForm()
    if(request.method == 'GET'):
      return render_template('recov_username.html', form=form)
    elif(request.method == 'POST'):
      return render_template('recov_username.html', form=form)
    else:
      return render_template('signin.html', form=form)
        
    
@app.route('/recov_pw', methods=['GET', 'POST'])
def recov_pw():
    form = RegisterForm()
    if(request.method == 'GET'):
        return render_template('recov_pw.html', form=form)
    elif(request.method == 'POST'):
        return render_template('recov_pw.html', form=form)
    else:
         return render_template('signin.html', form=form)
    
@app.route('/')
@login_required
def landing_page():
    return render_template('index.html')
    
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')




if __name__ == "__main__":
    app.run(host = os.getenv('IP','0.0.0.0'), port=int(os.getenv('PORT',8080)), debug=True)
