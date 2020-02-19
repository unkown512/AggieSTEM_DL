'''
   Model team to fill in interations with library
'''
def create_library(db, owner_id, library_name, min_perm, content_ids):
  '''
    library.owner = userid of who can access this
    library.content_id_list = list of conten_ids
  '''
  # Check if the intended owner exists and has the appropriate access level
  owner = db["user"].find_one({"_id": owner_id})
  if len(owner) == 0:
      print("Error! Intended owner account does not exist!")
      return False
  if owner["access_level"] < min_perm:
      print("Error! Cannot impose stricter permissions than your own access level!")
      return False
  
  # Next, build the library JSON dictionary.
  new_library_id = db['library'].insert_one({
    'name'          : library_name,
    'owner_id'      : owner_id,
    'min_permission': min_perm,
    'content_ids'   : [content_ids],
    'deleted'       : False
  })

  # Update user's access table to include the new library
  user_access = db['access'].find_one({'user_id': owner_id})
  user_access['library_ids'] = list(user_access['library_ids'].append(str(new_library_id.inserted_id)))

  # It is assumed that the owner should have admin rights over their library
  user_access['library_access'] = list(user_access['library_access'].append(3))
  #user_access['library_access'] = set(user_access['library_access'].append(owner["access_level"]))

  # TODO: Add test for if it was created successfully and the owner has access
  # Successful operation.
  return True

def add_content(db, user_id, library_id, content_name, data):
  '''
    Only the admin will do this which is checked in the controller.
    content.dir = path to data
  '''
  # Get the library to add the content id to.
  library = db["library"].find_one({"_id": library_id})
  if len(library) == 0:
      print("Error! Adding to a nonextant library...")
      return False
  if user_id != library["owner_id"]:
      print("Error! Cannot delete from a library you do not own...")
      return False
  
  # Next, build the group JSON dictionary.
  new_content_id = db['content'].insert_one({
    'name'         : content_name,
    'data'         : data,
    'deleted'      : False
  })
    
  # Add the inserted record's ID to the library
  library["content_ids"].append(str(new_content_id.inserted_id))
    
  # Update the library w/ the new content id
  db['library'].update_one({'_id': library_id}, {'$set': library})
  
  # TODO: Add test for if it was successful
  # Successful
  return True

# Sets the deletion flag for content 
def delete_content(db, content_id):
  '''
    content.id = content_id
  '''
  # Retrieve the content record from the DB.
  content = db["content"].find_one({"_id": content_id})
  if content is None or content['deleted'] == True:
      print("Error! Deletion of nonextant content...")
      return False
  
  # Set the deletion flag, signifying not to retrieve this content from DB.
  content['deleted'] = True
  
  # Update the library's record in the DB.
  db['content'].update_one({'_id': content_id}, {'$set': content})
  return True

# Sets the deletion flag for a library.
def delete_library(db, library_id):
  '''
    library.owner_id = user id for a library row
    library.id = library_id
  '''
  # Retrieve the library record from the DB.
  library = db["library"].find_one({"_id": library_id})
  if library is None:
      print("Error! Deletion of a nonextant library...")
      return False
  
  # Set the deletion flag, signifying not to retrieve this content from DB.
  library['deleted'] = True
  
  # Update the library's record in the DB.
  db['library'].update_one({'_id': library_id}, {'$set': library})
  return True

# Takes a list of content_ids and retrieves their JSON records.
# Can be a single ID.
def get_content(db, content_ids):
  '''
    content.id = content_id
  '''
  # Grab non-deleted content.
  content = db["content"].find({"_id": content_ids, "deleted": False})
  
  # Check if anything was retuned.
  if content is None:
      print("Error! Could not retrieve requested content!")
      return False
  
  # Serve the content
  return content

# Takes a list of library_ids and retrieves their JSON records.
# Can be a single ID.
def get_libraries(db, library_ids):
  '''
    library.owner_id = user id for a library row
    library.id = library_id
  '''
  # Grab non-deleted content.
  libraries = db["library"].find({"_id": library_ids, "deleted": False})
  
  # Check if anything was retuned.
  if libraries is None:
      print("Error! Could not retrieve requested libraries!")
      return False
  
  # Serve the libraries
  return libraries
