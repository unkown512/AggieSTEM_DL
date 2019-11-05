import sys
import json
import random

# Get the number of elements to generate
args = sys.argv

num_users = int(args[1])
num_library = int(args[2])
num_content = int(args[3])

# Name of the save file for the data
#user_file = 'user_data_' + str(num_users) + '.json'
#library_file = 'library_data_' + str(num_library) + '.json'
#content_file = 'content_data_' + str(num_content) + '.json'

save_file = 'data-U' + str(num_users) + '-L' + str(num_library) + '-C' + str(num_content) + '.json'

WORDS = []  #https://github.com/dwyl/english-words

print('Reading words file...', end='')
with open('words_alpha.txt', 'r') as f:
    WORDS = f.readlines()
print('...Done')

EMAILS = ['@gmail.com', '@yahoo.com', '@live.com', '@icloud.com', '@tamu.edu', '@hotmail.com']
POSITIONS = ['Guest', 'Member', 'Manager', 'Admin']

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

user_data = []
library_data = []
content_data = []

data = {}
data['user'] = []
data['security'] = []
data['access'] = []
data['library'] = []
data['content'] = []

#----------------------------------------------------------------

print('Generating user data...', end='', flush=True)
# Generate Users
for i in range(0, num_users):
    user_id = i
    username = (random.choice(WORDS)).rstrip() + '#' + str(random.randrange(10000)).zfill(4)
    access_level = random.randint(0,3)
    email = username + random.choice(EMAILS)
    phone = str(random.randrange(212,1000)) + '-' + str(random.randrange(1000)).zfill(3) + '-' + str(random.randrange(10000)).zfill(4)
    position = POSITIONS[access_level]
    security_questions = ['What does a duck do?', 'How does a fox quack?']
    password = username
    security_answers = ['quack', 'bark']
  
    d = {}
    n = random.randrange(10)
    while len(d) < n:   #Create a unique list of library_ids
        d.update({random.randrange(num_library): random.randint(0,3)})

    library_ids = list(d.keys())
    library_access = list(d.values())

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

    data['access'].append({
        'user_id': user_id,
        'library_ids': library_ids,
        'library_access': library_access
    })
    #END_OF_FOR
print('...Done', flush=True)

#----------------------------------------------------------------

print('Generating library data...', end='', flush=True)
# Generate Libraries
for i in range(0, num_library):
    library_id = i 
    owner_id = random.randrange(num_users)
    min_permission = random.randint(0,3)
    
    d = {}
    #n = random.randrange(num_content)
    #while len(d) < n:   #Create a unique list of content_ids
    for j in range(0, random.randrange(num_content)):   #Create a unique list of content_ids
        d.update({random.randrange(num_content): 0})

    content_ids = list(d.keys())

    # Create the data JSON
    data['library'].append({
        'library_id': library_id,
        'owner_id': owner_id,
        'min_permission': min_permission,
        'content_ids': content_ids
    })
    #END_OF_FOR
print('...Done', flush=True)

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
print('...Done', flush=True)

#----------------------------------------------------------------
#----------------------------------------------------------------

print('Exporting data...', end='', flush=True)
with open(save_file, 'w+') as f:
    json.dump(data, f)
print('...Done', flush=True)

#----------------------------------------------------------------
#----------------------------------------------------------------






#print('Exporting user data...', end='', flush=True)
#with open(user_file, 'w+') as f:
#    json.dump(user_data, f)
#print('...Done', flush=True)
#
#print('Exporting library data...', end='', flush=True)
#with open(library_file, 'w+') as f:
#    json.dump(library_data, f)
#print('...Done', flush=True)
#
#print('Exporting content data...', end='', flush=True)
#with open(content_file, 'w+') as f:
#    json.dump(content_data, f)
#print('...Done', flush=True)