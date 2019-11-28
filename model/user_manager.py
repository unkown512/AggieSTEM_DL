import mongoengine
import pymongo
import datetime
import json
import sys
from werkzeug.security import generate_password_hash, check_password_hash

'''
   Model team to fill in interations with DB, salts, and encryption for user information

'''

def unique_key():
  return "SUPPOSETOBEASECRET"

def validate_user(db, user, pw):
  print('\n\nVALIDATING USER\n\n')
  u_info = db['user'].find_one({'username':user})

  #Check if user exists
  if u_info is None:
    return False

  #Check user's password against what is stored in the database
  u_pw = db['security'].find_one({'user_id':u_info['user_id']})   #TODO: Handle hashing security info

  #Doubke check that user exists
  if u_pw is None:
    return False

  if u_pw['password'] == pw:
    return True
  
  if check_password_hash(u_pw['password'], pw):
    return True

  return False

def add_user(db, user_data):
  '''
    user_data = [username, password, email, position, phone]
  '''
  us = db['user'].find()
  next_id = 0
  for i in us:
    if i['user_id'] > next_id:
      next_id = i['user_id']
  next_id += 1

  # Access Levels. 1 will be for a user that has some content to view
  access_level = 0
  if(user_data[3] == "D"):
    access_level = 3
  elif(user_data[3] == "S"):
    access_level = 2
  else:
    access_level = 0

  # Create the data JSON
  db['user'].insert_one({
      'user_id': next_id,
      'username': user_data[0],
      'access_level': access_level,
      'email': user_data[2],
      'phone': user_data[4],
      'position': user_data[3],
      'security_questions': []
  })

  db['security'].insert_one({
      'user_id': next_id,
      'password': generate_password_hash(user_data[1]),
      'security_answers': []
  })

  # Insert user into DB
  return True

def get_user_profile(db, user):
  # Return one user prof
  return db['user'].find_one({'username':user})

def get_all_users(db):
  data = []
  for i in db['user'].find():
    data.append(i)

  return data

def update_user(db, user_data):
  #TODO
  return True

def delete_user(db, user):
  # TODO
  return True

def get_last_login(db, user):
  # TODO: RETURN LAST LOGIN TIME
  return 0

