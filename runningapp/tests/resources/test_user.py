import json
import unittest
from flask_jwt_extended import get_raw_jwt
from werkzeug.security import check_password_hash
from runningapp import create_app
from runningapp.db import db
from runningapp.models.user import UserModel, UserProfileModel
from runningapp.schemas.user import UserSchema
from runningapp.tests.base_classes import BaseApp, BaseDb, BaseUser
from runningapp.blacklist import BLACKLIST


user_list_schema = UserSchema(many=True)


# TODO REFACTOR ALL THE TESTS
class UserTest(unittest.TestCase, BaseApp, BaseDb, BaseUser):
    def setUp(self):
        """Set up a test app, test client and test database"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)

    def test_gets_user_data(self):
        self.__given_test_user_is_created()

        self.__when_get_request_is_sent(self.user.id)

        self.__then_status_code_is_200_ok()
        self.__then_correct_user_data_is_returned()

    def __given_test_user_is_created(self):
        self.user = self._create_sample_user()
        self.access_token = self._get_access_token(self.client)

    def __when_get_request_is_sent(self, user_id):
        self.response = self.client.get(
            path=f"users/{user_id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

    def __then_status_code_is_200_ok(self):
        self.assertEqual(self.response.status_code, 200)

    def __then_correct_user_data_is_returned(self):
        self.assertEqual(self.response.json["username"], self.user.username)
        self.assertEqual(self.response.json["id"], self.user.id)

    def test_does_not_return_user_data_if_not_found(self):
        non_existing_user_id = 10

        self.__given_test_user_is_created()

        self.__when_get_request_is_sent(non_existing_user_id)

        self.__then_status_code_is_404_not_found()
        self.__then_no_user_data_is_returned()

    def __then_status_code_is_404_not_found(self):
        self.assertEqual(self.response.status_code, 404)

    def __then_no_user_data_is_returned(self):
        self.assertNotIn("user", self.response.json)

    def test_deletes_user(self):

        self.__given_test_user_is_created()

        self.__when_delete_request_is_sent(self.user.id)

        self.__then_status_code_is_200_ok()
        self.__then_user_object_is_deleted()

    def __when_delete_request_is_sent(self, user_id):
        self.response = self.client.delete(
            path=f"users/{user_id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

    def __then_user_object_is_deleted(self):
        user = UserModel.find_by_id(self.user.id)

        self.assertIsNone(user)

    def test_does_not_delete_user_if_not_found(self):
        non_existing_user_id = 10

        self.__given_test_user_is_created()

        self.__when_delete_request_is_sent(non_existing_user_id)

        self.__then_status_code_is_404_not_found()

    def test_does_not_delete_user_if_no_permission(self):
        self.__given_test_user_is_created()
        self.__given_other_user_is_created()

        self.__when_delete_request_is_sent(self.user2.id)

        self.__then_status_code_is_403_forbidden()
        self.__then_user_object_is_not_deleted()

    def __then_status_code_is_403_forbidden(self):
        self.assertEqual(self.response.status_code, 403)

    def __given_other_user_is_created(self):
        self.user2 = self._create_sample_user(username="testuser2")
        self.user_profile2 = UserProfileModel.find_by_user_id(self.user2.id)

    def __then_user_object_is_not_deleted(self):
        user = UserModel.find_by_id(self.user2.id)

        self.assertIsNotNone(user)


class UserListTest(unittest.TestCase, BaseApp, BaseDb, BaseUser):
    def setUp(self):
        """Set up a test app, test client and test database"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)

    def test_gets_user_list_data(self):

        self.__given_users_are_created()

        self.__when_get_request_is_sent()

        self.__then_status_code_is_200_ok()
        self.__then_correct_user_list_data_is_returned()

    def __given_users_are_created(self):
        self._create_sample_user()
        self._create_sample_user(username="user2")
        self.access_token = self._get_access_token(self.client)

    def __when_get_request_is_sent(self):
        self.response = self.client.get(
            path=f"users/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

    def __then_status_code_is_200_ok(self):
        self.assertEqual(self.response.status_code, 200)

    def __then_correct_user_list_data_is_returned(self):
        trainings_data = user_list_schema.dump(UserModel.find_all())

        self.assertEqual(len(self.response.json["users"]), 2)
        self.assertEqual(self.response.json["users"], trainings_data)


class UserProfileTest(unittest.TestCase, BaseApp, BaseDb, BaseUser):
    def setUp(self):
        """Set up a test app, test client and test database"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)

    def __given_test_user_is_created(self):
        self.user1 = self._create_sample_user()
        self.user_profile1 = UserProfileModel.find_by_user_id(self.user1.id)
        self.access_token = self._get_access_token(self.client)

    def __given_other_user_is_created(self):
        self.user2 = self._create_sample_user(username="testuser2")
        self.user_profile2 = UserProfileModel.find_by_user_id(self.user2.id)

    def test_updates_properties_correctly(self):

        self.__given_test_user_is_created()
        self.__given_test_user_profile_data_is_prepared()

        self.__when_update_user_profile_is_sent_on_put_request(self.user_profile1.id)

        self.__then_status_code_is_200_ok()
        self.__then_user_profile_object_is_updated_correctly()

    def __then_status_code_is_200_ok(self):
        self.assertEqual(self.response.status_code, 200)

    def __when_update_user_profile_is_sent_on_put_request(self, user_profile_id):
        self.response = self.client.put(
            path=f"userprofiles/{user_profile_id}",
            data=json.dumps(self.user_profile_data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

    def __given_test_user_profile_data_is_prepared(self):
        self.user_profile_data = {
            "gender": "Female",
            "age": 24,
            "height": 165,
            "weight": 55,
        }

    def __then_user_profile_object_is_updated_correctly(self):
        self.assertEqual(self.user_profile1.gender, self.user_profile_data["gender"])
        self.assertEqual(self.user_profile1.age, self.user_profile_data["age"])
        self.assertEqual(self.user_profile1.height, self.user_profile_data["height"])
        self.assertEqual(self.user_profile1.weight, self.user_profile_data["weight"])

    def test_does_not_update_if_user_profile_not_found(self):

        non_existing_id = 10
        self.__given_test_user_is_created()
        self.__given_user_profile_is_none(non_existing_id)
        self.__given_test_user_profile_data_is_prepared()

        self.__when_update_user_profile_is_sent_on_put_request(non_existing_id)

        self.__then_status_code_is_404_not_found()

    def __then_status_code_is_404_not_found(self):
        self.assertEqual(self.response.status_code, 404)

    def __given_user_profile_is_none(self, user_profile_id):
        user_profile = UserProfileModel.find_by_id(user_profile_id)

        self.assertIsNone(user_profile)

    def test_does_not_update_if_no_permission(self):

        self.__given_test_user_is_created()
        self.__given_other_user_is_created()
        self.__given_test_user_profile_data_is_prepared()

        self.__when_update_user_profile_is_sent_on_put_request(self.user_profile2.id)

        self.__then_status_code_is_403_forbidden()
        self.__then_user_profile_is_not_updated()

    def __then_status_code_is_403_forbidden(self):
        self.assertEqual(self.response.status_code, 403)

    def __then_user_profile_is_not_updated(self):
        self.assertNotEqual(self.user_profile2.gender, self.user_profile_data["gender"])
        self.assertNotEqual(self.user_profile2.age, self.user_profile_data["age"])
        self.assertNotEqual(self.user_profile2.height, self.user_profile_data["height"])
        self.assertNotEqual(self.user_profile2.weight, self.user_profile_data["weight"])

    def test_updates_daily_caloric_needs_correctly(self):
        """Test if correct daily caloric needs are returned"""

        self.__given_test_user_is_created()
        self.__given_test_daily_cal_is_prepared()

        self.__when_update_daily_needs_is_sent_on_post_request()

        self.__then_status_code_is_201_created()
        self.__then_correct_daily_cal_is_returned()
        self.__then_user_profile_object_is_updated_with_correct_daily_cal()

    def __given_test_daily_cal_is_prepared(self):
        self.data = {"daily_cal": 2500}

    def __when_update_daily_needs_is_sent_on_post_request(self):
        self.response = self.client.post(
            path=f"update-daily-needs",
            data=json.dumps(self.data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._get_access_token(self.client)}",
            },
        )

    def __then_status_code_is_201_created(self):
        self.assertEqual(self.response.status_code, 201)

    def __then_correct_daily_cal_is_returned(self):
        expected_data = self.data["daily_cal"]
        self.assertEqual(self.response.json["daily_cal"], expected_data)

    def __then_user_profile_object_is_updated_with_correct_daily_cal(self):
        expected_daily_cal = self.data["daily_cal"]
        self.assertEqual(self.user_profile1.daily_cal, expected_daily_cal)


class OtherUserTests(unittest.TestCase, BaseApp, BaseDb, BaseUser):
    def setUp(self):
        """Set up a test app, test client and test database"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)

    def test_registers_user(self):
        self.__given_register_user_data_is_prepared()

        self.__when_post_request_is_sent("register", self.register_data)

        self.__then_status_code_is_201_created()
        self.__then_user_object_is_saved_in_db()
        self.__then_correct_register_user_data_is_returned()

    def __then_user_object_is_saved_in_db(self):
        user = UserModel.find_all()[-1]
        is_password_correct = check_password_hash(user.password, self.register_data['password'])

        self.assertEqual(user.username, self.register_data['username'])
        self.assertTrue(is_password_correct)

    def __then_correct_register_user_data_is_returned(self):
        user = UserModel.find_by_username(self.register_data['username'])

        self.assertEqual(self.response.json['username'], user.username)
        self.assertEqual(self.response.json['user'], user.id)
        self.assertIn('access_token', self.response.json)

    def __then_status_code_is_201_created(self):
        self.assertEqual(self.response.status_code, 201)

    def __when_post_request_is_sent(self, path, data):
        self.response = self.client.post(
            path=path,
            data=json.dumps(data),
            headers={"Content-Type": "application/json", },
        )

    def __given_register_user_data_is_prepared(self):
        self.register_data = {"username": "user2", "password": "testpass"}

    def __given_test_user_is_created(self):
        self.user1 = self._create_sample_user(username="testuser")
        self.user_profile1 = UserProfileModel.find_by_user_id(self.user1.id)
        self.access_token = self._get_access_token(self.client)

    def test_does_not_register_user_if_already_exists(self):
        users_number = len(UserModel.find_all())

        self.__given_test_user_is_created()
        self.__given_already_existing_data_is_prepared()

        self.__when_post_request_is_sent("register", self.existing_data)

        self.__then_status_code_is_400_bad_request()
        self.__then_no_new_user_is_registered(users_number)

    def __then_no_new_user_is_registered(self, previous_number):
        new_users_number = len(UserModel.find_all())

        self.assertNotEqual(new_users_number, previous_number)

    def __then_status_code_is_400_bad_request(self):
        self.assertEqual(self.response.status_code, 400)

    def __given_already_existing_data_is_prepared(self):
        self.existing_data = {
            "username": "testuser",
            "password": "testpass"
        }

    #
    #
    # def test_login_status_code_ok(self):
    #     """Test if the status code is 200 if the user logged in successfully"""
    #     data = {"username": self.user.username, "password": "testpass"}
    #     response = self.client.post(
    #         path=f"login",
    #         data=json.dumps(data),
    #         headers={"Content-Type": "application/json",},
    #     )
    #
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_login_status_code_unauthorized(self):
    #     """Test if the status code is 401 if the user enters invalid credentials"""
    #     data = {"username": self.user.username, "password": "wrongpass"}
    #     response = self.client.post(
    #         path=f"login",
    #         data=json.dumps(data),
    #         headers={"Content-Type": "application/json",},
    #     )
    #
    #     self.assertEqual(response.status_code, 401)
    #
    # def test_login_get_access_token(self):
    #     """Test if the access token is returned after logging in"""
    #     data = {"username": self.user.username, "password": "testpass"}
    #     response = self.client.post(
    #         path=f"login",
    #         data=json.dumps(data),
    #         headers={"Content-Type": "application/json",},
    #     )
    #
    #     self.assertIn("access_token", response.json)
    #
    # def test_logout_status_code_ok(self):
    #     """Test if the status code is 200 if the user logged out successfully"""
    #     response = self.client.post(
    #         path=f"logout",
    #         headers={
    #             "Content-Type": "application/json",
    #             "Authorization": f"Bearer {self._get_access_token(self.client)}",
    #         },
    #     )
    #
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_logout_token_in_blacklist(self):
    #     """Test if the token is added to the blacklist after logging out"""
    #     access_token = self._get_access_token(self.client)
    #     self.client.post(
    #         path=f"logout",
    #         headers={
    #             "Content-Type": "application/json",
    #             "Authorization": f"Bearer {access_token}",
    #         },
    #     )
    #
    #     jti = get_raw_jwt()["jti"]
    #
    #     self.assertIn(jti, BLACKLIST)
    #
    # def test_change_password_status_code_created(self):
    #     """Test if the status code is 201 if the user changed password successfully"""
    #     data = {"old_password": "testpass", "new_password": "brandnewpass"}
    #     response = self.client.post(
    #         path=f"change-password",
    #         data=json.dumps(data),
    #         headers={
    #             "Content-Type": "application/json",
    #             "Authorization": f"Bearer {self._get_access_token(self.client)}",
    #         },
    #     )
    #
    #     self.assertEqual(response.status_code, 201)
    #
    # def test_change_password_status_code_unauthorized(self):
    #     """Test if the status code is 401 if the user enters an invalid old password"""
    #     data = {"old_password": "wrongpass", "new_password": "brandnewpass"}
    #     response = self.client.post(
    #         path=f"change-password",
    #         data=json.dumps(data),
    #         headers={
    #             "Content-Type": "application/json",
    #             "Authorization": f"Bearer {self._get_access_token(self.client)}",
    #         },
    #     )
    #
    #     self.assertEqual(response.status_code, 401)
    #
    # def test_change_password_updates_data_in_db(self):
    #     """Check if the new password is saved in the database after changing it"""
    #     data = {"old_password": "testpass", "new_password": "brandnewpass"}
    #     self.client.post(
    #         path=f"change-password",
    #         data=json.dumps(data),
    #         headers={
    #             "Content-Type": "application/json",
    #             "Authorization": f"Bearer {self._get_access_token(self.client)}",
    #         },
    #     )
    #     is_password_changed = check_password_hash(
    #         self.user.password, data["new_password"]
    #     )
    #
    #     self.assertTrue(is_password_changed)


if __name__ == "__main__":
    unittest.main()
