import json
import unittest
from runningapp import create_app
from runningapp.db import db
from runningapp.models.training import TrainingModel
from runningapp.schemas.training import TrainingSchema
from runningapp.tests.base_classes import BaseApp, BaseDb, BaseUser, BaseTraining


training_list_schema = TrainingSchema(many=True)


# TODO REFACTOR ALL THE TESTS
class TrainingTests(unittest.TestCase, BaseApp, BaseDb, BaseUser, BaseTraining):
    def setUp(self):
        """Set up a test app, test client and test database"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)
        self.user = self._create_sample_user()
        self.access_token = self._get_access_token(self.client)
        self.training = self._create_sample_training(self.user)

    def test_get_training_status_code_ok(self):
        """Test if the status code is 200 if the training is found"""
        response = self.client.get(
            path=f"trainings/{self.training.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_get_training_status_code_not_found(self):
        """Test if the status code is 404 if the training is not found"""
        response = self.client.get(
            path=f"trainings/100",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_get_training_data(self):
        """Test if the correct data is returned"""
        response = self.client.get(
            path=f"trainings/{self.training.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.json["name"], self.training.name)
        self.assertEqual(response.json["user_id"], self.training.user_id)
        self.assertEqual(response.json["distance"], self.training.distance)
        self.assertEqual(response.json["avg_tempo"], self.training.avg_tempo)
        self.assertEqual(
            response.json["time_in_seconds"], self.training.time_in_seconds
        )

    def test_delete_training_status_code_ok(self):
        """Test if the status code is 200 if the training is found and deleted"""
        response = self.client.delete(
            path=f"trainings/{self.training.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_training_status_code_not_found(self):
        """Test if the status code is 404 if the training is not found"""
        response = self.client.delete(
            path=f"trainings/10",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_training_status_code_forbidden(self):
        """Test if the status code is 403 if the user doesn't have permission to delete the training"""
        self._create_sample_user(username="user2")
        access_token2 = self._get_access_token(client=self.client, username="user2")
        response = self.client.delete(
            path=f"trainings/{self.training.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token2}",
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_method_deletes_training_from_db(self):
        """Test if delete method deletes the training from the database"""
        self.client.delete(
            path=f"trainings/{self.training.id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        training = TrainingModel.find_by_id(self.training.id)

        self.assertIsNone(training)

    def test_update_training_status_code_ok(self):
        """Test if the status code is 200 if the training is found and updated"""
        data = {
            "name": self.training.name,
            "distance": self.training.distance,
            "time_in_seconds": 3700,
        }
        response = self.client.put(
            path=f"trainings/{self.training.id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_update_training_status_code_not_found(self):
        """Test if the status code is 404 if the training is not found"""
        data = {
            "name": self.training.name,
            "distance": self.training.distance,
            "time_in_seconds": 3700,
        }
        response = self.client.put(
            path=f"trainings/10",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_update_training_status_code_forbidden(self):
        """Test if the status code is 403 if the user doesn't have permission to update the training"""
        self._create_sample_user(username="user2")
        access_token2 = self._get_access_token(client=self.client, username="user2")
        data = {
            "name": self.training.name,
            "distance": self.training.distance,
            "time_in_seconds": 3700,
        }
        response = self.client.put(
            path=f"trainings/{self.training.id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token2}",
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_update_training_status_code_bad_request(self):
        """Test if the status code is 400 if the user enters a name which already exists
         among their trainings"""
        training2 = self._create_sample_training(user=self.user, name="test2")
        data = {
            "name": self.training.name,
            "distance": training2.distance,
            "time_in_seconds": training2.time_in_seconds,
        }
        response = self.client.put(
            path=f"trainings/{training2.id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_put_method_updates_training_in_db(self):
        """Test if put method updates the training in the database"""
        data = {
            "name": self.training.name,
            "distance": 7,
            "time_in_seconds": 3700,
        }
        self.client.put(
            path=f"trainings/{self.training.id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        training = TrainingModel.find_by_id(self.training.id)

        expected_avg_tempo = 6.8

        self.assertEqual(training.distance, data["distance"])
        self.assertEqual(training.time_in_seconds, data["time_in_seconds"])
        self.assertEqual(training.avg_tempo, expected_avg_tempo)


class TrainingListTests(unittest.TestCase, BaseApp, BaseDb, BaseUser, BaseTraining):
    def setUp(self):
        """Set up a test app, test client and test database"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)
        self.user = self._create_sample_user()
        self.access_token = self._get_access_token(self.client)
        self.training1 = self._create_sample_training(self.user)
        self.training2 = self._create_sample_training(self.user, "test2")

    def test_get_trainings_status_code_ok(self):
        """Test if the status code is 200"""
        response = self.client.get(
            path=f"trainings/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_get_trainings_data(self):
        """Test if the correct data is returned"""
        response = self.client.get(
            path=f"trainings/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )
        trainings_data = training_list_schema.dump(
            TrainingModel.find_all_by_user_id(self.user.id)
        )

        expected_trainings_num = 2

        self.assertEqual(len(response.json["trainings"]), expected_trainings_num)
        self.assertEqual(response.json["trainings"], trainings_data)

    def test_post_training_status_code_created(self):
        """Test if the status code is 201 if the training is created"""
        data = {
            "name": "test3",
            "distance": 10,
            "time_in_seconds": 3600,
        }
        response = self.client.post(
            path=f"trainings/",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 201)

    def test_post_training_status_code_bad_request(self):
        """Test if the status code is 400 if the user enters a name
        which already exists among their trainings"""
        data = {
            "name": "test2",
            "distance": 10,
            "time_in_seconds": 3600,
        }
        response = self.client.post(
            path=f"trainings/",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_post_training_data_in_db(self):
        """Test if the correct data is saved in the database"""
        data = {
            "name": "test3",
            "distance": 10,
            "time_in_seconds": 3600,
        }
        self.client.post(
            path=f"trainings/",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        training = TrainingModel.find_by_name(data["name"])

        self.assertEqual(training.name, data["name"])
        self.assertEqual(training.distance, data["distance"])
        self.assertEqual(training.time_in_seconds, data["time_in_seconds"])


if __name__ == "__main__":
    unittest.main()
