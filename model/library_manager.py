'''
   Model team to fill in interations with library

'''

def create_library(db, library):
  # TODO: Insert a new library
  '''
    library.owner = userid of who can access this
    library.content_id_list = list of conten_ids
  '''
  return True

def add_content(db, content):
  # TODO: Insert a new content
  '''
    Only the admin will do this which is checked in the controller.

    content.dir = path to data
  '''

def delete_content(db, content):
  # TODO: Delete content and update all library rows
  '''
    content.id = content_id
  '''
  return True

def delete_library(db, library):
  #TODO: Delete a libray row
  '''
    library.owner_id = user id for a library row
    library.id = library_id
  '''
  return True
