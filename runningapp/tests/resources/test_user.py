import json
import unittest
from flask_jwt_extended import get_raw_jwt
from werkzeug.security import check_password_hash
from runningapp import create_app
from runningapp.db import db
from runningapp.models.user import UserModel, UserProfileModel
from runningapp.schemas.user import UserSchema, UserProfileSchema
from runningapp.tests.functions import (
    sample_user,
    get_access_token,
    sample_training,
    set_up_test_app,
    set_up_client,
    set_up_test_db,
)
from runningapp.blacklist import BLACKLIST


user_list_schema = UserSchema(many=True)


class UserTests(unittest.TestCase):
    def setUp(self):
        """Set up a test app, test client and test database"""
        set_up_test_app(obj=self, create_app=create_app)
        self.client = set_up_client(self)
        set_up_test_db(db)
        self.user = sample_user()
        self.access_token = get_access_token(client=self.client)

    def test_get_user_status_code_ok(self):
        """Test if the status code is 200 if the user is found"""
        response = self.client.get(
            path=f"users/{self.user.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_get_user_status_code_not_found(self):
        """Test if the status code is 404 if the user is not found"""
        response = self.client.get(
            path=f"users/10",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_get_user_data(self):
        """Test if the correct data is returned if the user is found"""
        response = self.client.get(
            path=f"users/{self.user.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.json["username"], self.user.username)
        self.assertEqual(response.json["id"], self.user.id)

    def test_delete_user_status_code_ok(self):
        """Test if the status code is 200 if the user is found and deleted"""
        response = self.client.delete(
            path=f"users/{self.user.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_user_status_code_not_found(self):
        """Test if the status code is 404 if the user is not found"""
        response = self.client.delete(
            path=f"users/10",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_user_status_code_forbidden(self):
        """Test if the status code is 403 if the user doesn't have permission to delete the user"""
        sample_user(username="user2")
        access_token2 = get_access_token(client=self.client, username="user2")
        response = self.client.delete(
            path=f"users/{self.user.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token2}",
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_method_deletes_user_from_db(self):
        """Test if delete method deletes the user from the database"""
        self.client.delete(
            path=f"users/{self.user.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        training = UserModel.find_by_id(self.user.id)

        self.assertIsNone(training)


class UserListTests(unittest.TestCase):
    def setUp(self):
        """Set up a test app, test client and test database"""
        set_up_test_app(obj=self, create_app=create_app)
        self.client = set_up_client(self)
        set_up_test_db(db)
        self.user1 = sample_user()
        self.user2 = sample_user(username="user2")
        self.access_token = get_access_token(client=self.client)

    def test_get_users_status_code_ok(self):
        """Test if the status code is 200"""
        response = self.client.get(
            path=f"users/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_get_users_data(self):
        """Test if the correct data is returned"""
        response = self.client.get(
            path=f"users/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )
        trainings_data = user_list_schema.dump(UserModel.find_all())

        self.assertEqual(len(response.json["users"]), 2)
        self.assertEqual(response.json["users"], trainings_data)


class UserProfileTests(unittest.TestCase):
    def setUp(self):
        """Set up a test app, test client and test database"""
        set_up_test_app(obj=self, create_app=create_app)
        self.client = set_up_client(self)
        set_up_test_db(db)
        self.user1 = sample_user()
        self.user2 = sample_user(username="user2")
        self.user_profile1 = UserProfileModel.find_by_user_id(self.user1.id)
        self.user_profile2 = UserProfileModel.find_by_user_id(self.user2.id)
        self.access_token = get_access_token(client=self.client)

    def test_update_user_profile_status_code_ok(self):
        """Test if the status code is 200 if the user profile is found and updated"""
        data = {
            "gender": self.user_profile1.gender,
            "age": self.user_profile1.age,
            "height": self.user_profile1.height,
            "weight": 55,
        }
        response = self.client.put(
            path=f"userprofiles/{self.user_profile1.id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_update_user_profile_status_code_not_found(self):
        """Test if the status code is 404 if the user profile is not found"""
        data = {
            "gender": self.user_profile1.gender,
            "age": self.user_profile1.age,
            "height": self.user_profile1.height,
            "weight": 55,
        }
        response = self.client.put(
            path=f"userprofiles/10",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_update_user_profile_status_code_forbidden(self):
        """Test if the status code is 403 if the user doesn't have permission to update the training"""
        data = {
            "gender": self.user_profile2.gender,
            "age": self.user_profile2.age,
            "height": self.user_profile2.height,
            "weight": 55,
        }
        response = self.client.put(
            path=f"userprofiles/{self.user_profile2.id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_put_method_updates_user_profile_in_db(self):
        """Test if put method updates the user profile in the database"""
        data = {"gender": "Female", "age": 25, "height": 170, "weight": 60}
        self.client.put(
            path=f"userprofiles/{self.user_profile1.id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(self.user_profile1.gender, data["gender"])
        self.assertEqual(self.user_profile1.age, data["age"])
        self.assertEqual(self.user_profile1.height, data["height"])


class OtherUserTests(unittest.TestCase):
    def setUp(self):
        """Set up a test app, test client and test database"""
        set_up_test_app(obj=self, create_app=create_app)
        self.client = set_up_client(self)
        set_up_test_db(db)
        self.user = sample_user()

    def test_register_status_code_created(self):
        """Test if the status code is 201 if the user is registered successfully"""
        data = {"username": "user2", "password": "testpass"}
        response = self.client.post(
            path=f"register",
            data=json.dumps(data),
            headers={"Content-Type": "application/json",},
        )

        self.assertEqual(response.status_code, 201)

    def test_register_status_code_bad_request(self):
        """Test if the status code is 400 if the user with the given username already exists"""
        data = {"username": self.user.username, "password": "testpass"}
        response = self.client.post(
            path=f"register",
            data=json.dumps(data),
            headers={"Content-Type": "application/json",},
        )

        self.assertEqual(response.status_code, 400)

    def test_register_data_in_db(self):
        """Test if the user is saved in the database after signing up"""
        data = {"username": "user2", "password": "testpass"}
        self.client.post(
            path=f"register",
            data=json.dumps(data),
            headers={"Content-Type": "application/json",},
        )

        user = UserModel.find_by_username(data["username"])

        self.assertIsNotNone(user)

    def test_login_status_code_ok(self):
        """Test if the status code is 200 if the user logged in successfully"""
        data = {"username": self.user.username, "password": "testpass"}
        response = self.client.post(
            path=f"login",
            data=json.dumps(data),
            headers={"Content-Type": "application/json",},
        )

        self.assertEqual(response.status_code, 200)

    def test_login_status_code_unauthorized(self):
        """Test if the status code is 401 if the user enters invalid credentials"""
        data = {"username": self.user.username, "password": "wrongpass"}
        response = self.client.post(
            path=f"login",
            data=json.dumps(data),
            headers={"Content-Type": "application/json",},
        )

        self.assertEqual(response.status_code, 401)

    def test_login_get_access_token(self):
        """Test if the access token is returned after logging in"""
        data = {"username": self.user.username, "password": "testpass"}
        response = self.client.post(
            path=f"login",
            data=json.dumps(data),
            headers={"Content-Type": "application/json",},
        )

        self.assertIn("access_token", response.json)

    def test_logout_status_code_ok(self):
        """Test if the status code is 200 if the user logged out successfully"""
        response = self.client.post(
            path=f"logout",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {get_access_token(self.client)}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_logout_token_in_blacklist(self):
        """Test if the token is added to the blacklist after logging out"""
        access_token = get_access_token(self.client)
        self.client.post(
            path=f"logout",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        jti = get_raw_jwt()["jti"]

        self.assertIn(jti, BLACKLIST)

    def test_change_password_status_code_created(self):
        """Test if the status code is 201 if the user changed password successfully"""
        data = {"old_password": "testpass", "new_password": "brandnewpass"}
        response = self.client.post(
            path=f"change-password",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {get_access_token(self.client)}",
            },
        )

        self.assertEqual(response.status_code, 201)

    def test_change_password_status_code_unauthorized(self):
        """Test if the status code is 401 if the user enters an invalid old password"""
        data = {"old_password": "wrongpass", "new_password": "brandnewpass"}
        response = self.client.post(
            path=f"change-password",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {get_access_token(self.client)}",
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_change_password_updates_data_in_db(self):
        """Check if the new password is saved in the database after changing it"""
        data = {"old_password": "testpass", "new_password": "brandnewpass"}
        self.client.post(
            path=f"change-password",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {get_access_token(self.client)}",
            },
        )
        is_password_changed = check_password_hash(
            self.user.password, data["new_password"]
        )

        self.assertTrue(is_password_changed)


if __name__ == "__main__":
    unittest.main()

