import sys
import json
import random
import timer

# Get the number of elements to generate
args = sys.argv

num_users = int(args[1])
num_library = int(args[2])
num_content = int(args[3])
num_user_library = 20

TOGGLE_SORTED_LISTS = True

#----------------------------------------------------------------

t = timer.Timer()
t.start()

#----------------------------------------------------------------

save_file = 'data-U' + str(num_users) + '-L' + str(num_library) + '-C' + str(num_content) + '.json'

#----------------------------------------------------------------

print('\n----------------------------------------------------------------')
print('Users: {0} \tLibraries: {1} \tContent: {2}'.format(num_users, num_library, num_content))
print('----------------------------------------------------------------')

#----------------------------------------------------------------

print('Reading words file...', end='')
WORDS = []  #https://github.com/dwyl/english-words
with open('words_alpha.txt', 'r') as f:
    WORDS = f.readlines()
print('...Done \t\t{0} ms'.format(t.lap_time(1000)), flush=True)

#----------------------------------------------------------------

EMAILS = ['@gmail.com', '@yahoo.com', '@live.com', '@icloud.com', '@tamu.edu', '@hotmail.com']
POSITIONS = ['Guest', 'Member', 'Manager', 'Admin']
ACCESS_LEVELS = [0, 1, 2, 3]

#----------------------------------------------------------------

print('Generating ID list(s)...', end='')
USER_IDS = []
LIBRARY_IDS = []
CONTENT_IDS = []

#Create a list of USER_IDS for use with generating unique groups
for i in range(0, num_users):   
    USER_IDS.append(i)
#Create a list of LIBRARY_IDS for use with generating unique users
for i in range(0, num_library):   
    LIBRARY_IDS.append(i)
#Create a list of CONTENT_IDS for use with generating unique libraries
for i in range(0, num_content):   
    CONTENT_IDS.append(i)
print('...Done \t{0} ms'.format(t.lap_time(1000)), flush=True)

#----------------------------------------------------------------

# Data Schema
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
#
#
#lib         = Library(  library_id=0, 
#                        owner_id=0,
#                        min_permission=0,
#                        content_ids=[0,1] )
#
#
#content     = Content(  content_id=0, 
#                        data='HasContent' )

#----------------------------------------------------------------

data = {}
data['user'] = []
data['security'] = []
data['group'] = []
data['access'] = []
data['library'] = []
data['content'] = []

#----------------------------------------------------------------

print('Generating user data...', end='', flush=True)
# Generate Users
for i in range(0, num_users):
    user_id = i
    username = (random.choice(WORDS)).rstrip() + '#' + str(random.randrange(10000)).zfill(4)
    access_level = random.choice(ACCESS_LEVELS)
    email = username + random.choice(EMAILS)
    phone = str(random.randrange(212,1000)) + '-' + str(random.randrange(1000)).zfill(3) + '-' + str(random.randrange(10000)).zfill(4)
    position = POSITIONS[access_level]
    
    group_name = (random.choice(WORDS)).rstrip()
    user_ids = random.sample(LIBRARY_IDS, k=random.randrange(num_users))
    
    security_questions = ['What does a duck do?', 'How does a fox quack?']
    password = username
    security_answers = ['quack', 'bark']

    n = random.randrange(num_user_library)
    library_access = random.choices(ACCESS_LEVELS, k=n)
    library_ids = random.sample(LIBRARY_IDS, k=n)           #Unique random elements from LIBRARY_IDS

    if TOGGLE_SORTED_LISTS:
        user_ids.sort()
        library_ids.sort()
    
    #d = dict(zip(library_ids, library_access))

    # Create the data JSON
    data['user'].append({
        'user_id': user_id,
        'username': username,
        'access_level': access_level,
        'email': email,
        'phone': phone,
        'position': position,
        'security_questions': security_questions
    })

    data['security'].append({
        'user_id': user_id,
        'password': password,
        'security_answers': security_answers
    })

    data['group'].append({
        'group_id': user_id,
        'owner_id': user_id,
        'group_name': group_name,
        'access_level': access_level,
        'user_ids': user_ids
    })

    data['access'].append({
        'user_id': user_id,
        'library_ids': library_ids,
        'library_access': library_access
    })

    #END_OF_FOR
print('...Done \t\t{0} ms'.format(t.lap_time(1000)), flush=True)

#----------------------------------------------------------------

print('Generating library data...', end='', flush=True)
# Generate Libraries
for i in range(0, num_library):
    library_id = i 
    owner_id = random.randrange(num_users)
    min_permission = random.choice(ACCESS_LEVELS)
    content_ids = random.sample(CONTENT_IDS, k=random.randrange(num_content))

    if TOGGLE_SORTED_LISTS:
        content_ids.sort()

    # Create the data JSON
    data['library'].append({
        'library_id': library_id,
        'owner_id': owner_id,
        'min_permission': min_permission,
        'content_ids': content_ids
    })
    #END_OF_FOR
print('...Done \t{0} ms'.format(t.lap_time(1000)), flush=True)

#----------------------------------------------------------------

print('Generating content data...', end='', flush=True)
# Generate Content
for i in range(0, num_content):
    content_id = i

    # Create the data JSON
    data['content'].append({
        'content_id': content_id,
        'data': 'Data for content_id: ' + str(content_id)
    })
    #END_OF_FOR
print('...Done \t{0} ms'.format(t.lap_time(1000)), flush=True)

#----------------------------------------------------------------
#----------------------------------------------------------------

print('Exporting data...', end='', flush=True)
with open(save_file, 'w+') as f:
    json.dump(data, f)
print('...Done \t\t{0} ms'.format(t.lap_time(1000)), flush=True)

#----------------------------------------------------------------
t.stop()
print('----------------------------------------------------------------')
print('Total elapsed {0} ms'.format(t.get_time(1000)))
print('----------------------------------------------------------------\n')
#----------------------------------------------------------------
