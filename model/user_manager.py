"""User manager manages user login and registration on databases."""
from werkzeug.security import generate_password_hash, check_password_hash


def unique_key():
    return 'SUPPOSETOBEASECRET'


def validate_user(db, username, pw):
    """Check if a user's credential is correct."""
    print('\n\nVALIDATING USER\n\n')
    user = db['user'].find_one({'username': username})

    # Check if user exists
    if user is None:
        return False

    user_id = user['user_id']

    # Check user's password against what is stored in the database
    pw = db['security'].find_one({'user_id': user_id})

    # Check if the password for the user exists
    if pw is None:
        return False

    # For backwards compatibility, treat password as unhashed first
    if pw['password'] == pw:
        return True

    # Check for hashed password
    if check_password_hash(pw['password'], pw):
        return True

    return False


def add_user(db, username, password, email, position, phone):
    """Add a user to the database.

    user_data: [username, password, email, position, phone]
    """
    # Set the new user id
    users = db['user'].find()
    next_id = max(u['user_id'] for u in users) + 1

    # Set Access Level. 1 will be for a user that has some content to view.
    # Default level is 0
    access_level_map = {'D': 3, 'S': 2}
    access_level = access_level_map.get(position, 0)

    # Create the data JSON
    db['user'].insert_one(dict(
        user_id=next_id,
        username=username,
        access_level=access_level,
        email=email,
        position=position,
        phone=phone,
        security_questions=[]))

    db['security'].insert_one(dict(
        user_id=next_id,
        password=generate_password_hash(password),
        security_answers=[]))

    # Insert user into DB
    return True


def get_user_profile(db, user):
    """Return one user profile."""
    return db['user'].find_one({'username': user})


def get_all_users(db):
    """Return all users in database."""
    return list(db['user'].find())


def update_user(db, user_data):
    # TODO
    return True


def delete_user(db, user):
    # TODO
    return True


def get_last_login(db, user):
    # TODO: RETURN LAST LOGIN TIME
    return 0

