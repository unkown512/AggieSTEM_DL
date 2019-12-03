import unittest

import model.user_manager as user
import model.group_manager as group
import model.library_manager as library

import run_server

client = run_server.db_connection()
db = run_server.db_client()

from database.Database_Setup import init_database

class TestDatabase(unittest.TestCase):
  def setUp(self):
    client.drop_database('AggieSTEM')
    init_database()
    users = [
      ['cat', 'pass', 'email', '', '1231231234']
    ]
    for u in users:
      user.add_user(db, u)

class TestUserManager(TestDatabase):
  def test_add_user(self):
    u = user.get_user_profile(db, 'cat')
    self.assertEqual(u['username'], 'cat')
    self.assertEqual(u['email'], 'email')
    self.assertTrue(user.validate_user(db, 'cat', 'pass'))
  
  def test_get_all_users(self):
    users = user.get_all_users(db)
    self.assertEqual(len(users), 2)
  
  def test_get_access_level(self):
    u = user.get_access_level(db, 'cat')
    self.assertEqual(u, 0)

class TestGroupManager(TestDatabase):
  # def test_create_group(self):
  #   group.create_group(db, user_id, group_id, user_list, access_level)
  def setUp(self):
    super().setUp()
    group.create_group(db, 0, 0, [0], 3)
  
  def test_create_group(self):
    # Already a group
    self.assertFalse(group.create_group(db, 0, 0, [0], 3))
    
  def test_valid_access_level(self):
    self.assertTrue(group.valid_access_level(0))
    self.assertTrue(group.valid_access_level(1))
    self.assertTrue(group.valid_access_level(2))
    self.assertTrue(group.valid_access_level(3))
    self.assertTrue(group.valid_access_level(4))
    self.assertTrue(group.valid_access_level(5))
    self.assertFalse(group.valid_access_level(-1))
    self.assertFalse(group.valid_access_level(-2))
    self.assertFalse(group.valid_access_level(-3))
    self.assertFalse(group.valid_access_level(6))
    self.assertFalse(group.valid_access_level(7))
    self.assertFalse(group.valid_access_level(8))
    self.assertFalse(group.valid_access_level(9))
    self.assertFalse(group.valid_access_level(10))

unittest.main()