# AggieSTEM MongoDB Database Setup

This is the directory for the AggieSTEM database, wherein backend development will take place.

To add a new user to DB user_information:
> user = User(_id='0', username='chingy1510', password='abcdefABCDEF', permission_level='admin', 
      phone='254-555-0123', security_questions=['What does a duck do?'], security_answers=['Quack'],
      email='chingy1510@tamu.edu')
>      
> user_information.insert_one(json.loads(user.to_json()))
  
  And this process can be generalized using the schema and Database_Setup.py to add documents to any of the given tables.
  
  # TODO:
  - Read the MongoDB tutorial : https://www.tutorialspoint.com/mongodb/index.htm
  - Host the MongoDB server online : https://www.tutorialspoint.com/mongodb/mongodb_deployment.htm
  - Generate dummy data : https://www.json-generator.com/
  - Identify better indices : https://www.simplilearn.com/indexing-and-aggregation-mongodb-tutorial-video
  - Play around with uploading all file types.
  
