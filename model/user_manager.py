"""User manager manages user login and registration on databases."""
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

import datetime
import random

def unique_key():
  return str(uuid4())

def get_access_level(db, username):
  # Return true if user access level is high enough
  user = db['user'].find_one({'username': username})
  return user['access_level']


def validate_user(db, username, pw):
  """Check if a user's credential is correct."""
  print('\n\nVALIDATING USER\n\n')
  user = db['user'].find_one({'username': username})

  update_timestamp = {}
  update_timestamp['login_timestamp'] = str(datetime.datetime.utcnow())

  # Check if user exists
  if user is None:
    print(username + " does not exist!")
    return False

  user_id = str(user['_id'])
  print("User ID: " + user_id)

  # Check user's password against what is stored in the database
  db_pw = db['security'].find_one({'user_id': user_id})

  # Check if the password for the user exists
  if db_pw is None:
    print("User password does not exist!")
    return False

  # For backwards compatibility, treat password as unhashed first
  if db_pw['password'] == pw:
    db['user'].update_one({'_id': user_id}, {'$set': update_timestamp})
    print("Valid user!")
    return True

  # Check for hashed password
  if check_password_hash(db_pw['password'], pw):
    db['user'].update_one({'_id': user_id}, {'$set': update_timestamp})
    print("Valid user!")
    return True

  print("Invalid user!")
  return False


def check_security_answers(db, username, answers, minimum_correct=0):
  """Check if a user's security answers are correct.

  Args:
    db (pymongo.MongoClient): mongodb client instance.
    username (str): username of the user.
    answers (List[str]): user provided answer.
    minimum_correct (int): minimum number of questions to answer
      correctly in order to pass the test.

  """
  user = get_username_profile(db, username)
  if user is None:
    return False

  security = db['security'].find_one({'_id': str(user['_id'])})
  if security is None:
    return False
  correct_answers = security['security_answers']

  # Count the number of correct answers
  correct_count = 0
  for answer, correct in zip(answers, correct_answers):
    if answer == correct:
      correct_count += 1
    elif check_password_hash(correct, answer):
      correct_count += 1

  # Check if satisfy minimum correct count
  if minimum_correct > 0:
    return correct_count >= minimum_correct
  else:  # Otherwise, pass if all correct
    return correct_count == len(correct_answers)


def add_user(db, user_data):
  """Add a user to the database.

  user_data: [username, password, email, position, phone]
  """
  username, password, email, position, phone = user_data[:5]

  # Set the new user id
  #users = db['user'].find()
  #next_id = max(u['_id'] for u in users) + 1

  # Set Access Level. 1 will be for a user that has some content to view.
  # Default level is 0
  access_level_map = {'D': 3, 'S': 2}
  access_level = access_level_map.get(position, 0)

  security_questions = []
  security_answers = []

  security_answers_hash = [generate_password_hash(ans)
                           for ans in security_answers]

  password_hash = generate_password_hash(password)


  # Create the data JSON
  new_user = db['user'].insert_one({
    'username': username,
    'access_level': access_level,
    'email': email,
    'position': position,
    'phone': phone,
    'security_questions': security_questions,
    'login_timestamp':str(datetime.datetime.utcnow()),
    'deleted': False
  })

  db['security'].insert_one({
    'user_id': str(new_user.inserted_id),
    'password': password_hash,
    'security_answers': security_answers_hash
  })

  # Insert user into DB
  return True


def hash_all_password(db):
  """Hash all passwords that's stored in plaintext previously."""
  passwords = []
  # Filter all users that needs update
  for security in db['security'].find():
    update = {}
    # Check if password is hashed
    if not security['password'].startswith('pbkdf2:'):
      update['password'] = generate_password_hash(security['password'])

    # Check if security answers are hashed
    if any(not ans.startswith('pbkdf2:') for ans in security['security_answers']):
      update['security_answers'] = [generate_password_hash(ans)
                                    for ans in security['security_answers']]

    if update:
      passwords.append((str(security['_id']), update))
  print("Will update these users: ", passwords)

  # Update these users
  for _id, update in passwords:
    db['security'].update_one({'_id': _id}, {'$set': update})


def get_username_profile(db, username):
  """Return one user profile."""
  return db['user'].find_one({'username': username})

def get_userid_profile(db, user_id):
  """Return one user profile."""
  return db['user'].find_one({'_id': user_id})


def get_all_users(db):
  """Return all users in database."""
  return list(db['user'].find())

# TODO: Make sure this works correctly
def update_user(db, user, user_data):
  db['user'].update_one({'_id': str(user['_id'])}, {'$set': user_data})
  return True


def delete_user(db, user):
  users = db['user'].find({'username': user})
  update = {}
  update['deleted'] = True

  # Return False if more than one user was found
  if(len(users) > 1):
    return False

  db['user'].update_one({'_id': str(user['_id'])}, {'$set': update})
  return True


def get_last_login(db, user):
  u = db['user'].find_one({'username': user})
  return u['login_timestamp']

