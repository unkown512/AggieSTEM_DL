# -*- coding: utf-8 -*-
"""
Created on Fri Nov 01 22:22:25 2019

@author: Carson
"""
from mongoengine import *
from pprint import pprint
import datetime
import pymongo
import json
import sys


# User account schema
class User(Document):
    user_id            = IntField(required=True)
    username           = StringField(required=True, max_length=40)      # username#number
    access_level       = IntField(required=True)                        # Defines default access level for library/content. 0 -> Guest, 1 -> Member, 2 -> Manager, 3 -> Admin
    email              = StringField(required=True, max_length=100)
    phone              = StringField(required=True, max_length=20)
    position           = StringField(required=True, max_length=100)     # Job title
    security_questions = ListField(required=True)


class Security(Document):   #Hashed
    user_id            = IntField(required=True)
    password           = StringField(required=True, max_length=40)
    security_answers   = ListField(required=True)
    
# User Library Access schema
class UserLibraryAccess(Document):
    user_id            = IntField(required=True)
    library_ids        = ListField(required=True)   # Library_ids a user has access to
    library_access     = ListField(required=True)   # User permission_level for each library_id


# Library schema
class Library(Document):
    library_id         = IntField(required=True)
    owner_id           = IntField(required=True)
    min_permission     = IntField(required=True)    # Minimum permission level a user needs to access without being given explicit access to the library
    content_ids        = ListField(required=True)


# Content schema
class Content(Document):
    content_id       = IntField(required=True)
    data             = StringField(required=True)


#----------------------------------------------------------------
#----------------------------------------------------------------

# Grab the local client
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Create reference to the correct DB.
db = client["AggieSTEM"]

# Setup tables within the db.
db["user"].drop()         
db["security"].drop() 
db["user_library_access"].drop()  
db["library"].drop()  
db["content"].drop()  

user_table                  = db["user"]
security_table              = db["security"]         
user_library_access_table   = db["user_library_access"]
library_table               = db["library"]
content_table               = db["content"]  

#----------------------------------------------------------------
#----------------------------------------------------------------

# Quickly sets up a local MongoDB database.
def Setup():
    # Create dummy content
    user        = User( user_id=0, 
                        username='admin#1510', 
                        access_level=3,
                        email='chingy1510@tamu.edu',
                        phone='254-555-0123', 
                        position='Admin',
                        security_questions=['What does a duck do?', 'How does a fox quack?'] )

    security    = Security( user_id=0,
                            password='pw1234',
                            security_answers=['quack', 'bark'] )

    access      = UserLibraryAccess(user_id=0, 
                                    library_ids=[0], 
                                    library_access=[3] )
    
    library     = Library(  library_id=0, 
                            owner_id=0,
                            min_permission=0,
                            content_ids=[0,1] )
    
    
    content     = Content(  content_id=0, 
                            data='HasContent' )


    # Create the tables by injecting the dummy data
    user_table.insert_one(                  json.loads(user.to_json())      )
    user_library_access_table.insert_one(   json.loads(access.to_json())    )
    security_table.insert_one(              json.loads(security.to_json())  )
    library_table.insert_one(               json.loads(library.to_json())   )
    content_table.insert_one(               json.loads(content.to_json())   )
    

    # Create indicies
    user_table.create_index([('user_id', pymongo.TEXT)], name='user_search', default_language='english')

    security_table.create_index([('user_id', pymongo.TEXT)], name='security_search', default_language='english')

    user_library_access_table.create_index([('user_id', pymongo.TEXT)], name='user_search', default_language='english')
    #user_library_access_table.create_index([('library_ids', pymongo.TEXT)], name='user_lib_search', default_language='english')

    library_table.create_index([('library_id', pymongo.TEXT)], name='lib_search', default_language='english')
    #library_table.create_index([('owner_id', pymongo.TEXT)], name='owner_lib_search', default_language='english')
    
    content_table.create_index([('content_id', pymongo.TEXT)], name='content_search', default_language='english')

    # Show that this name is successfully there
    dblist = client.list_database_names()
    print(dblist)

#----------------------------------------------------------------
#----------------------------------------------------------------

# Quickly sets up a local MongoDB database.
def Import(data_file = None):
    if data_file is None:
        print('Unable to open file.')
    else:
        # Parse the json data file
        with open(data_file, 'r') as f:
            data = json.load(f)

        # Create dummy content
        #user        = User( user_id=0, 
        #                    username='admin#1510', 
        #                    access_level=3,
        #                    email='chingy1510@tamu.edu',
        #                    phone='254-555-0123', 
        #                    position='Admin',
        #                    security_questions=['What does a duck do?', 'How does a fox quack?'] )
        #
        #security    = Security( user_id=0,
        #                        password='pw1234',
        #                        security_answers=['quack', 'bark'] )
        #
        #access      = UserLibraryAccess(user_id=0, 
        #                                library_ids=[0], 
        #                                library_access=[3] )
        #
        #library     = Library(  library_id=0, 
        #                        owner_id=0,
        #                        min_permission=0,
        #                        content_ids=[0,1] )
        #
        #content     = Content(  content_id=0, 
        #                        data='HasContent' )

        user_table.insert_many(data['user'])
        security_table.insert_many(data['security'])
        user_library_access_table.insert_many(data['access'])
        library_table.insert_many(data['library'])
        content_table.insert_many(data['content'])

        # Create indicies
        #user_table.create_index([('user_id', pymongo.TEXT)], default_language='english')
        #user_table.create_index([('username', pymongo.TEXT)], default_language='english')

        #security_table.create_index([('user_id', pymongo.TEXT)], name='security_search', default_language='english')

        #user_library_access_table.create_index([('user_id', pymongo.TEXT)], name='user_library_search', default_language='english')
        #user_library_access_table.create_index([('library_ids', pymongo.TEXT)], name='user_lib_search', default_language='english')

        #library_table.create_index([('library_id', pymongo.TEXT)], name='library_search', default_language='english')
        #library_table.create_index([('owner_id', pymongo.TEXT)], name='owner_lib_search', default_language='english')
        
        #content_table.create_index([('content_id', pymongo.TEXT)], name='content_search', default_language='english')

        # Show that this name is successfully there
        dblist = client.list_database_names()
        print(dblist)


    
args = sys.argv

if len(args) is 1:
    Setup()
else:
    Import(args[1])


#Create a master user
db['user'].find_one_and_update({'user_id':0}, {'$set':{'username': 'Andy', 'email':'andy@tamu.edu', 'access_level':3, 'position':'Admin'}})
db['security'].find_one_and_update({'user_id':0}, {'$set':{'password': 'Andy1234'}})

user = 'Andy'
pw = 'Andy1234'
email = 'Andy@tamu.edu'

#u_info = db['user'].find_one({'username':user})
#u_pw = db['security'].find_one({'user_id':u_info['user_id']})
#print(str(u_pw['password'] == pw))

# data = []
# for i in db['user'].find(): 
#     data.append(i) 

# pprint(data)

#for index in db['user'].find({'user_id': 0}):  
#    print(index) 
