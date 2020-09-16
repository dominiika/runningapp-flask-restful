import json
import unittest
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
    sample_admin,
)


user_list_schema = UserSchema(many=True)


class AdminManageUserTests(unittest.TestCase):
    def setUp(self):
        """Set up a test app, test client and test database"""
        set_up_test_app(obj=self, create_app=create_app)
        self.client = set_up_client(self)
        set_up_test_db(db)
        self.admin = sample_admin()
        self.access_token = get_access_token(
            client=self.client, username="admin", password="testpass"
        )
        self.user = sample_user()

    def test_get_user_status_code_ok(self):
        """Test if the status code is 200 if the user is found
        and if the logged in user is the admin"""
        response = self.client.get(
            path=f"admin/users/{self.user.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_get_user_status_code_not_found(self):
        """Test if the status code is 404 if the user is not found"""
        response = self.client.get(
            path=f"admin/users/10",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_get_user_status_code_forbidden(self):
        """Test if the status code is 403 if the logged in user is not the admin"""
        user_token = get_access_token(
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
                "Authorization": f"Bearer {self.access_token}",
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
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_user_status_code_not_found(self):
        """Test if the status code is 404 if the user is not found"""
        response = self.client.delete(
            path=f"admin/users/10",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_user_status_code_forbidden(self):
        """Test if the status code is 403 if the logged in user is not the admin"""
        user_token = get_access_token(
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
                "Authorization": f"Bearer {self.access_token}",
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
                "Authorization": f"Bearer {self.access_token}",
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
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_update_user_status_code_forbidden(self):
        """Test if the status code is 403 if the logged in user is not the admin"""
        user_token = get_access_token(
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
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(self.user.username, data["username"])
        self.assertTrue(check_password_hash(self.user.password, data["password"]))


class AdminManageUserListTests(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
