import unittest
from runningapp import create_app
from runningapp.db import db
from runningapp.tests.base_classes import BaseApp, BaseDb, BaseUser
from runningapp.models.user import UserModel, UserProfileModel


class UserModelTests(unittest.TestCase, BaseApp, BaseDb, BaseUser):
    def setUp(self):
        """Set up a test app, test client and test database"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)

    def test_user_is_saved_in_db(self):
        """Test if the user has been successfully saved in the database"""
        user = UserModel(username="test", password="testpass")
        user.save_to_db()
        found_user = UserModel.find_by_username("test")

        self.assertIsNotNone(found_user)

    def test_user_is_deleted_from_db(self):
        """Test if the user has been successfully deleted from the database"""
        user = self._create_sample_user("test")
        user.delete_from_db()
        found_user = UserModel.find_by_username("test")

        self.assertIsNone(found_user)

    def test_find_by_username(self):
        """Test if the user is found"""
        user = self._create_sample_user("test")
        found_user = UserModel.find_by_username("test")

        self.assertEqual(found_user, user)

    def test_find_by_username_no_user(self):
        """Test if None is returned if the user with the given username doesn't exist"""
        found_user = UserModel.find_by_username("test")

        self.assertIsNone(found_user)

    def test_find_by_id(self):
        """Test if the user is found"""
        user = self._create_sample_user("test")
        found_user = UserModel.find_by_id(user.id)

        self.assertEqual(user, found_user)

    def test_find_by_id_no_user(self):
        """Test if None is returned if the user with the given id doesn't exist"""
        found_user = UserModel.find_by_id(1)

        self.assertIsNone(found_user)

    def test_find_all(self):
        """Test if all the users which exist in the database are returned"""
        user1 = self._create_sample_user("test1")
        user2 = self._create_sample_user("user2")
        found_users = UserModel.find_all()

        self.assertIn(user1, found_users)
        self.assertIn(user2, found_users)

    def test_find_all_no_users(self):
        """Test if an empty list is returned if there are no users in the database"""
        found_users = UserModel.find_all()

        self.assertEqual(found_users, [])


class UserProfileModelTests(unittest.TestCase, BaseApp, BaseDb, BaseUser):
    def setUp(self):
        """Set up a test app, test client and test database"""
        # set_up_test_app(obj=self, create_app=create_app)
        # self.client = set_up_client(self)
        # set_up_test_db(db)
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)

    def test_userprofile_is_saved_in_db(self):
        """Test if the user profile has been successfully saved in the database
        after creating a new user"""
        user = UserModel(username="test", password="testpass")
        user.save_to_db()
        userprofile = UserProfileModel(user_id=user.id)
        userprofile.save_to_db()
        found_userprofile = UserProfileModel.find_by_username(user.username)

        self.assertIsNotNone(found_userprofile)

    def test_userprofile_is_deleted_from_db(self):
        """Test if the user profile has been successfully deleted from the database"""
        user = self._create_sample_user("test")
        userprofile = UserProfileModel.find_by_user_id(user.id)
        userprofile.delete_from_db()
        found_userprofile = UserProfileModel.find_by_user_id(user.id)

        self.assertIsNone(found_userprofile)

    def test_find_by_username(self):
        """Test if the user profile is found"""
        user = self._create_sample_user("test")
        found_userprofile = UserProfileModel.find_by_username("test")

        self.assertEqual(found_userprofile.user_id, user.id)

    def test_find_by_username_no_user(self):
        """Test if None is returned if the user with the given username doesn't exist"""
        found_userprofile = UserProfileModel.find_by_username("test")

        self.assertIsNone(found_userprofile)

    def test_find_by_id(self):
        """Test if the user profile is found"""
        self._create_sample_user("test")
        found_userprofile = UserProfileModel.find_by_id(1)

        self.assertIsNotNone(found_userprofile)

    def test_find_by_id_no_user(self):
        """Test if None is returned if the user profile with the given id doesn't exist"""
        found_userprofile = UserProfileModel.find_by_id(1)

        self.assertIsNone(found_userprofile)

    def test_find_all(self):
        """Test if all the user profiles which exist in the database are returned"""
        self._create_sample_user("test1")
        self._create_sample_user("user2")
        found_userprofiles = UserProfileModel.find_all()

        self.assertEqual(len(found_userprofiles), 2)

    def test_find_all_no_users(self):
        """Test if an empty list is returned if there are no trainings in the database"""
        found_userprofiles = UserProfileModel.find_all()

        self.assertEqual(found_userprofiles, [])
