# Model for user group interaction
#import mongoengine
#import pymongo
#import datetime
#import json
#import sys

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
def create_group(db, owner_id, user_ids, access_level, group_name=None):
  # Check if the access_level is valid.
  if not valid_access_level(access_level):
    print("Invalid access level requested!")
    return False

  # Check if a member is being included with this group.
  if user_ids is None:
    print("Critical error! Must have at least one member!")
    return False

  # Check for a group_name, otherwise set it to the default
  if group_name is None:
    group_name = 'New Group'

  # Next, build the group JSON dictionary.
  new_group_id = db['group'].insert_one({
    'name'         : group_name,
    'owner_id'     : owner_id,
    'access_level' : access_level,
    'user_ids'     : user_ids,
    'deleted'      : False
  })

  # Check if this insert was successful
  if is_group(db, str(new_group_id.inserted_id)):
    print("Successful insertion of group!")
    return True
  else:
    print("Error inserting to database! Retry or debug!")
    return False

# Attempts to delete group: group_id as user: user_id.
def delete_group(db, user_id, group_id):
  # Fetch the requested user and group for the interaction.
  user  = db['user'].find({"_id" : user_id})
  group = db['group'].find({"_id" : group_id})

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
  #db['group'].delete_one({"_id" : group_id})

  # Don't actually delete the group, but set the deleted flag for the group
  group['deleted'] = True
  db['group'].update_one({"_id" : group_id}, {'$set': group})

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
  group    = db['group'].find({'_id' : group_id})
  users    = db['user'].find({'_id'  : group['user_ids']})

  # Check if the group has users to return.
  # Base user should be the admin - this is a critical error if hit.
  if users is None:
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
  # Query to see if a single group with this id exists and the deleted flag has not been set.
  if db['group'].count_documents({"_id" : group_id}, limit = 1) != 0:
    is_deleted = db['group'].find_one({"_id" : group_id})
    if is_deleted['deleted'] == False:
      print("Valid group!")
      return True
    else:
      print('Group has been deleted!')
      return False
  # If the query returned 0, the group/library doesn't exist.
  else:
    print("Invalid group!")
    return False

# Add an existing user to a group.
def add_user(db, admin_id, group_id, user_id):
  # First, check if the group exists.
  if not is_group(db, group_id):
    print("Attempting to add user to invalid group! Error!")
    return False

  # Check if the user being entered exists
  user = db['user'].find_one({"_id" : user_id})
  if user is None:
    print("Invalid user_id! Cannot add to group!")
    return False

  # Fetch the admin and group records, and validate.
  admin = db['user'].find_one({"_id"  : admin_id})
  group = db['group'].find_one({"_id": group_id})

  # Check if the admin has correct credentials or is the owner.
  if admin is None or admin['access_level'] < group['access_level'] or str(admin['_id']) != group['owner_id']:
    print("Invalid credentials to add user to group!")
    return False
  # If so, add this user to the group.
  else:
    print("Valid credentials! Adding...")
    group['user_ids'].append(user_id)
    db['group'].update(group)
    return True

# Remove a user from a group
def remove_user(db, admin_id, group_id, user_id):
 # First, check if the group exists.
  if not is_group(db, group_id):
    print("Attempting to add user to invalid group! Error!")
    return False

  # Check if the user being entered exists
  user = db['user'].find_one({"_id" : user_id})
  if user is None:
    print("Invalid user_id! Cannot add to group!")
    return False

  # Fetch the admin and group records, and validate.
  admin = db['user'].find_one({"_id"  : admin_id})
  group = db['group'].find_one({"_id": group_id})

  # Check if the admin has correct credentials or is the owner.
  if admin is None or admin['access_level'] >= group['access_level'] or str(admin['_id']) != group['owner_id']:
    print("Valid credentials! Adding...")
    group['user_ids'].remove(user_id)
    db['group'].update(group)
    return True
  # Otherwise, do not delete.
  else:
    print("Invalid credentials to remove user from group!")
    return False

# Checks if the user has the appropriate permissions, and if so, adds the group to their document.
def join_group(db, user_id, group_id):
  # First, check if the group exists.
  if not is_group(db, group_id):
    print("Attempting to add user to invalid group! Error!")
    return False

  # Check if the user being entered exists
  user = db['user'].find_one({"_id" : user_id})
  if user is None:
    print("Invalid user_id! Cannot add to group!")
    return False

  # Fetch the group.
  group = db['group'].find_one({"_id": group_id})

  # Check if the user has the appropriate access level
  if user['access_level'] >= group['access_level']:
    print("Valid credentials! Adding...")
    group['user_ids'].append(user_id)
    db['group'].update(group)
  # Otherwise, do not add.
  else:
    print("Invalid permissions to join group! Unsuccessful!")
    return False

# Grabs all groups that this user is a part of.
def get_all_groups(db, user_id):
  # Grab this user to check availability
  user = db['user'].find_one({'_id': str(user_id)})
  print(user)
  if user is None:
    print("Error! Invalid user_id given! Cannot retrieve groups!")
    return False
  
  user_groups = db['group'].find({'user_ids': user_id})

  if user_groups is None:
    print('User is not in a group!')
    return False
  return user_groups


  '''
  # Grab the groups and check for correctness.
  user_access = db['user_library_access'].find_one({"user_id": user_id})
  if len(user_access) == 0:
      print("Error! Could not retrieve user_library_access!")
      return False
  
  #Return all the groups the user is apart of
  return user_access["library_ids"]
  '''
