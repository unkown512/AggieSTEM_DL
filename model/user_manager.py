'''
   Model team to fill in interations with DB, salts, and encryption for user information
   
'''

def unique_key():
  return "SUPPOSETOBEASECRET"

def validate_user(user, pw, TEMP_LOGIN_DB):
  # REMOVE EVERYTHING RELATED TO TEMP_LOGIN_DB WHEN YOU MAKE DATABASE 
  if(len(TEMP_LOGIN_DB)>0):
    if(user == "Andy" and pw == "Andy1234" or (user == TEMP_LOGIN_DB[0][0] and pw == TEMP_LOGIN_DB[0][1])):
      return True
  else:
    if(user == "Andy" and pw == "Andy1234"):
      return True
  return False
  
def add_user(user, pw, email, sq1, sq2):
  # TODO
  # Insert user into DB
  return True
  
def get_user_profile(userObject):
  # TODO
  # Return one user prof
  return True
  
def get_all_users():
  # TODO
  # Return a list of users and their phone/email
  return True
  
def delete_user():
  # TODO
  return True
  
#TODO: TRAVIS ADD get_all_users_function here
#have it return data like shown in manage_users.js