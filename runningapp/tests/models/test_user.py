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


class UserProfileModelCalculatorsTests(unittest.TestCase, BaseApp, BaseDb, BaseUser):
    def setUp(self):
        """Set up a test app, test client and test database"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)
        self.user = self._create_sample_user(
            age=25, gender="Female", height=165, weight=58
        )
        self.user_profile = UserProfileModel.find_by_user_id(self.user.id)

    def test_calculate_bmi_success(self):
        """Test if BMI is calculated correctly."""
        self.user_profile.calculate_bmi()
        expected_bmi = 21.3

        self.assertEqual(self.user_profile.bmi, expected_bmi)

    def test_calculate_bmi_failure(self):
        """Test if BMI is calculated incorrectly."""
        self.user_profile.calculate_bmi()
        wrong_bmi = 21

        self.assertNotEqual(self.user_profile.bmi, wrong_bmi)

    def test_calculate_activity_factor_success(self):
        """Test if the activity factor is calculated correctly."""
        trainings_per_week = 5

        activity_factor = self.user_profile._calculate_activity_factor(
            trainings_per_week
        )
        expected_activity_factor = 1.8

        self.assertEqual(activity_factor, expected_activity_factor)

    def test_calculate_activity_factor_failure(self):
        """Test if the activity factor is calculated incorrectly."""
        trainings_per_week = 5

        activity_factor = self.user_profile._calculate_activity_factor(
            trainings_per_week
        )
        wrong_activity_factor = 2

        self.assertNotEqual(activity_factor, wrong_activity_factor)

    def test_calculate_daily_caloric_needs_success(self):
        """Test if the daily caloric needs is calculated correctly."""
        trainings_per_week = 5

        self.user_profile.calculate_daily_caloric_needs(trainings_per_week)
        expected_daily_cal = 2504

        self.assertEqual(self.user_profile.daily_cal, expected_daily_cal)

    def test_calculate_daily_caloric_needs_failure(self):
        """Test if the daily caloric needs is calculated incorrectly."""
        trainings_per_week = 5

        self.user_profile.calculate_daily_caloric_needs(trainings_per_week)
        wrong_daily_cal = 2000

        self.assertNotEqual(self.user_profile.daily_cal, wrong_daily_cal)
