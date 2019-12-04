'''
   Model team to fill in interations with library

'''

def create_library(db, owner_id, library_id, min_perm, content_ids):
  '''
    library.owner = userid of who can access this
    library.content_id_list = list of conten_ids
  '''
  # Check if the intended owner exists and has the appropriate access level
  owner = db["user"].find({"user_id": owner_id})
  if len(owner) == 0:
      print("Error! Intended owner account does not exist!")
      return False
  if owner["access_level"] < min_perm:
      print("Error! Cannot impose stricter permissions than your own access level!")
      return False
  
  # Next, build the library JSON dictionary.
  db['library'].insert_one({
    'library_id'    : library_id,
    'owner_id'      : owner_id,
    'min_permission': min_perm,
    'content_ids'   : [content_ids]
  })

  # Successful operation.
  return True

def add_content(db, user_id, library_id, content_name, data):
  '''
    Only the admin will do this which is checked in the controller.
    content.dir = path to data
  '''
  # Get the library to add the content id to.
  library = db["library"].find_one({"library_id": library_id})
  if len(library) == 0:
      print("Error! Adding to a nonextant library...")
      return False
  if user_id != library["owner_id"]:
      print("Error! Cannot delete from a library you do not own...")
      return False
  
  # Next, build the group JSON dictionary.
  _id = db['content'].insert_one({
    'data'         : data,
    'content_id'   : content_name
  })
    
  # Add the inserted record's ID to the library
  library["content_ids"] = set(library["content_ids"].append(_id))
    
  # Update the library w/ the new content id
  db['library'].update_one({'library_id': library_id}, {'$set': library})
  
  # Successful
  return True

# TODO: Add a delete flag for content 
def delete_content(db, content):
  '''
    content.id = content_id
  '''
  return True

# TODO: Add a delete flag for libraries
def delete_library(db, library):
  '''
    library.owner_id = user id for a library row
    library.id = library_id
  '''
  return True
