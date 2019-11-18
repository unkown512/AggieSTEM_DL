# Model for user group interaction
import mongoengine
import pymongo
import datetime
import json
import sys

# TODO: -Add redirect to a page to be able to request access to a 
#        group from its administrator via the message app.
#       -Test functionality.

# Checks if the access level being set is appropriate for the DB
# 0 : all access, 1 : tier 1 access, 2 : tier 2 access, ..., 5 : admin access.
def valid_access_level(access_level):
  if access_level >= 0 and access_level <= 5:
    print("Proper access level!")
    return True
  else:
    print("Improper access level! Please enter [0, 5].")
    return False

# Create a new group
def create_group(db, user_id, group_id, user_list, access_level):
  # First, check and make sure this group doesn't already exist.
  if is_group(db, group_id):
    print("Error! Already a group!")
    return False
  
  # Check if the access_level is valid.
  if not valid_access_level(access_level):
    print("Invalid access level requested!")
    return False
    
  # Check if a member is being included with this group.
  if len(user_list) == 0:
    print("Critical error! Must have at least one member!")
    return False
  
  # Next, build the group JSON dictionary.
  db['group_table'].insert_one({
    'owner_id'     : user_id,
    'group_id'     : group_id,
    'user_list'    : user_list,
    'access_level' : access_level,
    'user_ids'     : [user_id]
  })
  
  # Check if this insert was successful
  if is_group(db, group_id):
    print("Successful insertion of group!")
    return True
  else:
    print("Error inserting to database! Retry or debug!")
    return False
  
# Attempts to delete group: group_id as user: user_id.
def delete_group(db, user_id, group_id):
  # Fetch the requested user and group for the interaction.
  user  = db.user_table.find({"user_id" : user_id})
  group = db.group_table.find({"group_id" : group_id})
  
  # Check if the user_id was valid and returned a record.
  if len(user) == 0:
    print("NO USER FOUND. CANNOT DELETE.")
    return False
    
  # Check if the group_id was valid and returned a record.
  if len(group) == 0:
    print("NO GROUP FOUND. CANNOT DELETE.")
    return False
    
  # Check if this user has appropriate permissions to delete.
  if user['access_level'] < group['access_level']:
    print("Invalid permissions! Cannot delete group! Contact an admin...")
    return False
    
  # At this point, all data retrieved from the db has been verified, and the
  # delete transaction can take place.
  db.group_table.delete_one({"group_id" : group_id})
  
  # Check if the group was successfully deleted.
  if not is_group(db, group_id):
    print("Successful deletion!")
    return True
  # In this case, the group is still queryable and active.
  else:
    print("Unsuccessful deletion interaction with the database!")
    return False

# Get users for a specifc group.
def get_users(db, group_id):
  # Check if this group exists.
  if not is_group(db, group_id):
    print("Invalid group! Cannot return users!")
    return False
    
  # Query the groups array for values equivalent to group_id.
  group    = db.group_table.find({"group_id" : group_id})
  users    = db.user_table.find({"user_id" : group['user_ids']})
  
  # Check if the group has users to return.
  # Base user should be the admin - this is a critical error if hit.
  if len(users) == 0:
    print("Critical error! No users in this group!")
    return False
  
  # Check if user(s) have the correct group.
  for user in users:
    if group_id not in user['group_ids']:
      print("Error fetching " + group_id + " members from database.")
      return False
      
  # Extract user id(s). This may be slow?
  #user_ids = []
  #for user in users:
  #  user_ids.append(user['user_id'])
    
  # Return the fetched user JSON values.
  return users
   
# Valid group check.
# https://stackoverflow.com/questions/25163658/mongodb-return-true-if-document-exists
def is_group(db, group_id):
  # Query to see if a single library with this id exists.
  if db.library_table.count_documents({"library_id" : group_id}, limit = 1) != 0:
    print("Valid group!")
    return True
  # If the query returned 0, the group/library doesn't exist.
  else:
    print("Invalid group!")
    return False
  
# Add a user to a group.
def add_user(db, admin_id, group_id, user_id):
  # First, check if the group exists.
  if not is_group(db, group_id):
    print("Attempting to add user to invalid group! Error!")
    return False
    
  # Check if the user being entered exists
  user = db.user_table.find_one({"user_id" : user_id})
  if len(user) == 0:
    print("Invalid user_id! Cannot add to group!")
    return False
    
  # Fetch the admin and group records, and validate.
  admin = db.user_table.find_one({"user_id"  : admin_id})
  group = db.group_table.find_one({"group_id": group_id})
  
  # Check if the admin has correct credentials.
  if len(admin) == 0 or admin['access_level'] < group['access_level']:
    print("Invalid credentials to add user to group!")
    return False
  # If so, add this user to the group.
  else:
    print("Valid credentials! Adding...")
    group['user_ids'].append(user_id)
    db.group_table.update(group)
    return True
  
# Remove a user from a group
def remove_user(db, admin_id, group_id, user_id):
 # First, check if the group exists.
  if not is_group(db, group_id):
    print("Attempting to add user to invalid group! Error!")
    return False
    
  # Check if the user being entered exists
  user = db.user_table.find_one({"user_id" : user_id})
  if len(user) == 0:
    print("Invalid user_id! Cannot add to group!")
    return False
    
  # Fetch the admin and group records, and validate.
  admin = db.user_table.find_one({"user_id"  : admin_id})
  group = db.group_table.find_one({"group_id": group_id})
  
  # Check if the admin has correct credentials.
  if len(admin) != 0 or admin['access_level'] >= group['access_level']:
    print("Valid credentials! Adding...")
    group['user_ids'].remove(user_id)
    db.group_table.update(group)
    return True
  # Otherwise, do not delete.
  else:
    print("Invalid credentials to add user to group!")
    return False
  
# Checks if the user has the appropriate permissions, and if so, adds the group to their document.
def join_group(db, user_id, group_id):
  # First, check if the group exists.
  if not is_group(db, group_id):
    print("Attempting to add user to invalid group! Error!")
    return False
    
  # Check if the user being entered exists
  user = db.user_table.find_one({"user_id" : user_id})
  if len(user) == 0:
    print("Invalid user_id! Cannot add to group!")
    return False
  
  # Fetch the group.
  group = db.group_table.find_one({"group_id": group_id})
  
  # Check if the user has the appropriate access level
  if user['access_level'] >= group['access_level']:
    print("Valid credentials! Adding...")
    group['user_ids'].append(user_id)
    db.group_table.update(group)
  # Otherwise, do not add.
  else:
    print("Invalid permissions to join group! Unsuccessful!")
    return False
