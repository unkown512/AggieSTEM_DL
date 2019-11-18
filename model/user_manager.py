import mongoengine
import pymongo
import datetime
import json
import sys

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

  return False

def add_user(db, user, pw, email):
  # TODO Get the next valid user_id
  us = db['user'].find()
  next_id = 0
  for i in us:
    if i['user_id'] > next_id:
      next_id = i['user_id']
  next_id += 1

  # Create the data JSON
  db['user'].insert_one({
      'user_id': next_id,
      'username': user,
      'access_level': 0,
      'email': email,
      'phone': '',
      'position': '',
      'security_questions': []
  })

  db['security'].insert_one({
      'user_id': next_id,
      'password': pw,
      'security_answers': []
  })

  # Insert user into DB
  return True

def get_user_profile(db, user):
  # Return one user prof
  return db['user'].find_one({'username':user})

def get_all_users(db):
  # TODO
  data = []
  for i in db['user'].find():
    data.append(i)

  return data

def delete_user(db, user):
  # TODO
  return True

