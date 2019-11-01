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
  
def add_user(user, pw, email):
  # TODO
  # Insert user into DB
  return True
  
def get_user_profile(user):
  # TODO
  # Return one user prof
  return True
  
def get_all_users():
  # TODO
  
  # Replace data[] with query of all users
  data = [
    [ "Tiger_Nixon", "Professor", "3", "tiger_nixon@tamu.edu", "610-432-2121", "Star, Spec","01/13/2019(21:45 GMT)"],
    [ "Garrett_Winters", "Research Assistant", "1", "garrett_winters@tamu.edu", "230-845-5846", "Web, Hrbb","10/24/2019(5:30 GMT)"],
    [ "James_Brown", "Research Assistant", "1", "j_brown@tamu.edu", "430-765-3446", "Spy, Nxt","08/01/2019(8:32 GMT)"]
  ]
  return data
  
def delete_user():
  # TODO
  return True
  
#TODO: TRAVIS ADD get_all_users_function here
#have it return data like shown in manage_users.js