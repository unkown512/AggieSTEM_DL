# -*- coding: utf-8 -*-
"""
Created on Fri Nov 01 22:22:25 2019

@author: Carson
"""
from mongoengine import *
import datetime
import pymongo
import json


# User account schema
class User(Document):
  user_id = IntField(required=True)
  username = StringField(required=True, max_length=40) # username#number
  '''
    `access_level` for library/content.
      0 -> Guest
      1 -> Member
      2 -> Admin
  '''
  access_level = IntField(required=True)
  email = StringField(required=True, max_length=100)
  phone = StringField(required=True, max_length=20)
  position = StringField(required=True, max_length=100) # Job title
  security_questions = ListField(required=True)

class Group(Document):
  group_id = IntField(required=True)
  owner_id = IntField(required=True)
  group_name = StringField(required=True, max_length=30)
  access_level = IntField(required=True)
  user_ids = ListField(required=True)

class Security(Document):
  user_id = IntField(required=True)
  password = StringField(required=True, max_length=40)
  security_answers = ListField(required=True)

class UserLibraryAccess(Document):
  user_id = IntField(required=True)
  library_ids = ListField(required=True)
  library_access = ListField(required=True)


class Library(Document):
  library_id = IntField(required=True)
  owner_id = IntField(required=True)
  min_permission = IntField(required=True)
  content_ids = ListField(required=True)

class Content(Document):
  content_id = IntField(required=True)
  data = StringField(required=True)


#----------------------------------------------------------------

def init_database():
  print("Connection to mongoclient")
  try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
  except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)

  if "AggieSTEM" not in client.list_database_names():
    db = client["AggieSTEM"]
    # Setup tables within the db.
    Setup(db, client)
  else:
    print("AggieSTEM DB already exists")

# Quickly sets up a local MongoDB database.
def Setup(db, client):
  # Create dummy content
  user_table = db["user"]
  security_table = db["security"]
  group_table = db["group"]
  user_library_access_table = db["user_library_access"]
  library_table = db["library"]
  content_table = db["content"]

  db['user'].find_one_and_update({'user_id':0}, {'$set':{'username': 'Andy', 'email':'andy@tamu.edu', 'access_level':3, 'position':'Admin'}})
  db['security'].find_one_and_update({'user_id':0}, {'$set':{'password': 'Andy1234'}})

  user = User(user_id=0,
    username='admin#1510',
    access_level=3,
    email='chingy1510@tamu.edu',
    phone='254-555-0123',
    position='Admin',
    security_questions=['What does a duck do?', 'How does a fox quack?'])

  security = Security(user_id=0,
    password='pw1234',
    security_answers=['quack', 'bark'])

  group = Group(group_id=0,
    owner_id=0,
    group_name='IsGroup',
    access_level=0,
    user_ids=[0])

  access = UserLibraryAccess(user_id=0,
    library_ids=[0],
    library_access=[3])

  library = Library(library_id=0,
    owner_id=0,
    min_permission=0,
    content_ids=[0,1])

  content = Content(content_id=0,
    data='HasContent')


  # Create the tables by injecting the dummy data
  print("check 1")
  user_table.insert_one(json.loads(user.to_json()))
  user_library_access_table.insert_one(json.loads(access.to_json()))
  security_table.insert_one(json.loads(security.to_json()))
  group_table.insert_one(json.loads(group.to_json()))
  library_table.insert_one(json.loads(library.to_json()))
  content_table.insert_one(json.loads(content.to_json()))


  print("check 2")
  # Create indicies
  user_table.create_index([('user_id', pymongo.TEXT)], name='user_search', default_language='english')

  user_table.create_index([('group_id', pymongo.TEXT)], name='group_search', default_language='english')

  security_table.create_index([('user_id', pymongo.TEXT)], name='security_search', default_language='english')

  user_library_access_table.create_index([('user_id', pymongo.TEXT)], name='user_search', default_language='english')
  #user_library_access_table.create_index([('library_ids', pymongo.TEXT)], name='user_lib_search', default_language='english')

  library_table.create_index([('library_id', pymongo.TEXT)], name='lib_search', default_language='english')
  #library_table.create_index([('owner_id', pymongo.TEXT)], name='owner_lib_search', default_language='english')

  content_table.create_index([('content_id', pymongo.TEXT)], name='content_search', default_language='english')

  # Show that this name is successfully there
  dblist = client.list_database_names()

#----------------------------------------------------------------

'''
# Quickly sets up a local MongoDB database.
def Import(data_file = None):
  if data_file is None:
    print('Unable to open file.')
  else:
    # Parse the json data file
    with open(data_file, 'r') as f:
      data = json.load(f)

    user_table.insert_many(data['user'])
    security_table.insert_many(data['security'])
    group_table.insert_many(data['group'])
    user_library_access_table.insert_many(data['access'])
    library_table.insert_many(data['library'])
    content_table.insert_many(data['content'])

    # Show that this name is successfully there
    dblist = client.list_database_names()
    print(dblist)
'''

if __name__ == '__main__':
  init_database()
