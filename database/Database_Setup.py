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
    _id                = IntField(required=True)
    username           = StringField(required=True, max_length=40)
    password           = StringField(required=True, max_length=40)
    permission_level   = StringField(required=True)
    email              = StringField(required=True, max_length=100)
    phone              = StringField(required=True, max_length=20)
    security_questions = ListField(required=True)
    security_answers   = ListField(required=True)
    
# Access credentials schema
class AccessCredentials(Document):
    user_id            = IntField(required=True)
    library_id         = IntField(required=True)
    permission_level   = StringField(required=True)

# Library schema
class Library(Document):
    user_id            = IntField(required=True)
    library_id         = IntField(required=True)
  
# Content schema
class Content(Document):
    library_id         = IntField(required=True)
    assets             = ListField(required=True)
        
# Quickly sets up a local MongoDB database.
def Setup():
    # Grab the local client
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    
    # Create reference to the correct DB.
    db = client["AggieSTEM"]
    
    # Setup tables within the db.
    db["user_information"].drop()         
    db["library_access"].drop()  
    db["library"].drop()  
    db["content"].drop()  
    user_information       = db["user_information"]            
    content_library_access = db["library_access"]
    user_shared_library    = db["library"]
    content_table          = db["content"]   
    
    # Create dummy content
    user    = User(_id='0', username='chingy1510', password='abcdefABCDEF', permission_level='admin',
                   phone='254-555-0123', security_questions=['What does a duck do?'], security_answers=['Quack'],
                   email='chingy1510@tamu.edu')
    access  = AccessCredentials(user_id='0', library_id='0', permission_level='admin')
    lib     = Library(user_id='0', library_id='0')
    content = Content(library_id='0', assets=['0', '1', '2', '3'])
    
    # Create the tables by injecting the dummy data
    user_information.insert_one(json.loads(user.to_json()))
    content_library_access.insert_one(json.loads(access.to_json()))
    user_shared_library.insert_one(json.loads(lib.to_json()))
    content_table.insert_one(json.loads(content.to_json()))
    
    # Create indicies
    user_information.create_index([('_id', pymongo.TEXT)], name='user_search', default_language='english')
    content_library_access.create_index([('user_id', pymongo.TEXT)], name='user_search', default_language='english')
    content_library_access.create_index([('library_id', pymongo.TEXT)], name='lib_search', default_language='english')
    user_shared_library.create_index([('user_id', pymongo.TEXT)], name='user_search', default_language='english')
    user_shared_library.create_index([('library_id', pymongo.TEXT)], name='lib_search', default_language='english')
    content_table.create_index([('library_id', pymongo.TEXT)], name='lib_search', default_language='english')

    # Show that this name is successfully there
    dblist = client.list_database_names()
    print(dblist)
    
Setup()
    