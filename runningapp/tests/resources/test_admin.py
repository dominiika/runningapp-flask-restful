import json
import unittest
from werkzeug.security import check_password_hash

from runningapp import create_app
from runningapp.db import db
from runningapp.models.user import UserModel
from runningapp.schemas.user import UserSchema
from runningapp.tests.base_classes import BaseApp, BaseDb, BaseUser, BaseAdmin

user_list_schema = UserSchema(many=True)


class AdminManageUserTests(unittest.TestCase, BaseApp, BaseDb, BaseUser, BaseAdmin):
    """Test admin interface"""

    def setUp(self) -> None:
        """Set up a test app, test client and test database"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)
        self.admin = self._create_sample_admin()
        self.admin_access_token = self._get_admin_access_token(self.client)
        self.user = self._create_sample_user()

    def test_get_user_status_scode_ok(self):
        """Test if the status code is 200 if the user is found
        and if the logged in user is the admin"""
        response = self.client.get(
            path=f"admin/users/{self.user.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_get_user_status_code_not_found(self):
        """Test if the status code is 404 if the user is not found"""
        response = self.client.get(
            path=f"admin/users/10",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_get_user_status_code_forbidden(self):
        """Test if the status code is 403 if the logged in user is not the admin"""
        user_token = self._get_access_token(
            client=self.client, username=self.user.username, password="testpass"
        )
        response = self.client.get(
            path=f"admin/users/{self.user.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer \
            {user_token}",
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_get_user_data(self):
        """Test if the correct data is returned if the user is found
         and the logged in user is the admin"""
        response = self.client.get(
            path=f"admin/users/{self.user.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
        )

        self.assertEqual(response.json["username"], self.user.username)
        self.assertEqual(response.json["id"], self.user.id)

    def test_delete_user_status_code_ok(self):
        """Test if the status code is 200 if the user is found and deleted"""
        response = self.client.delete(
            path=f"admin/users/{self.user.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_user_status_code_not_found(self):
        """Test if the status code is 404 if the user is not found"""
        response = self.client.delete(
            path=f"admin/users/10",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_user_status_code_forbidden(self):
        """Test if the status code is 403 if the logged in user is not the admin"""
        user_token = self._get_access_token(
            client=self.client, username=self.user.username, password="testpass"
        )
        response = self.client.delete(
            path=f"admin/users/{self.user.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {user_token}",
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_method_deletes_user_from_db(self):
        """Test if delete method deletes the user from the database"""
        self.client.delete(
            path=f"admin/users/{self.user.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
        )

        training = UserModel.find_by_id(self.user.id)

        self.assertIsNone(training)

    def test_update_user_status_code_ok(self):
        """Test if the status code is 200 if the user is found and updated
        and the logged in user is the admin"""
        data = {"username": "updated_username", "password": "updatedpass"}
        response = self.client.put(
            path=f"admin/users/{self.user.id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_update_user_status_code_not_found(self):
        """Test if the status code is 404 if the user is not found"""
        data = {"username": "updated_username", "password": "updatedpass"}
        response = self.client.put(
            path=f"admin/users/10",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_update_user_status_code_forbidden(self):
        """Test if the status code is 403 if the logged in user is not the admin"""
        user_token = self._get_access_token(
            client=self.client, username=self.user.username, password="testpass"
        )
        data = {"username": "updated_username", "password": "updatedpass"}
        response = self.client.put(
            path=f"admin/users/{self.user.id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {user_token}",
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_put_method_updates_user_in_db(self):
        """Test if put method updates the user in the database"""
        data = {"username": "updated_username", "password": "updatedpass"}
        self.client.put(
            path=f"admin/users/{self.user.id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
        )

        self.assertEqual(self.user.username, data["username"])
        self.assertTrue(check_password_hash(self.user.password, data["password"]))


class AdminManageUserListTests(unittest.TestCase, BaseApp, BaseDb, BaseAdmin, BaseUser):
    """Test admin interface"""

    def setUp(self):
        """Set up a test app, test client and test database"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)
        self.admin = self._create_sample_admin()
        self.admin_access_token = self._get_admin_access_token(self.client)

    def test_get_users_status_code_ok(self):
        """Test if the status code is 200 if the logged in user is the admin"""

        response = self.client.get(
            path=f"admin/users/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_get_users_data(self):
        """Test if the correct data is returned if the logged in user is the admin"""
        self._create_sample_user()

        response = self.client.get(
            path=f"admin/users/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
        )

        users_data = user_list_schema.dump(UserModel.find_all())

        self.assertEqual(len(response.json["users"]), 2)
        self.assertEqual(users_data, response.json["users"])

    def test_get_users_status_code_forbidden(self):
        """Test if the status code is 403 if the logged in user is not the admin"""
        user = self._create_sample_user()
        user_token = self._get_access_token(
            client=self.client, username=user.username, password="testpass"
        )

        response = self.client.get(
            path=f"admin/users/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {user_token}",
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_post_status_code_created(self):
        """Test if the status code is 201 if the user is registered successfully by the admin"""
        data = {"username": "user2", "password": "testpass"}

        response = self.client.post(
            path=f"admin/users/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
            data=json.dumps(data),
        )

        self.assertEqual(response.status_code, 201)

    def test_post_data_in_db(self):
        """Test if the user is saved in the database after signing them up by the admin"""
        data = {"username": "user2", "password": "testpass"}

        self.client.post(
            path=f"admin/users/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
            data=json.dumps(data),
        )

        user = UserModel.find_by_username(data["username"])

        self.assertIsNotNone(user)

    def test_register_status_code_bad_request(self):
        """Test if the status code is 400 if the user with the given username already exists"""
        self._create_sample_user(username="user1")
        data = {"username": "user1", "password": "testpass"}

        response = self.client.post(
            path=f"admin/users/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.admin_access_token}",
            },
            data=json.dumps(data),
        )

        self.assertEqual(response.status_code, 400)

    def test_post_users_status_code_forbidden(self):
        """Test if the status code is 403 if the logged in user is not the admin"""
        self._create_sample_user(username="user")
        token = self._get_access_token(
            client=self.client, username="user", password="testpass"
        )
        data = {"username": "user2", "password": "testpass"}

        response = self.client.post(
            path=f"admin/users/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            data=json.dumps(data),
        )

        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
