import unittest
from runningapp import create_app
from runningapp.db import db
from runningapp.tests.functions import (
    set_up_test_app,
    set_up_client,
    set_up_test_db,
    sample_user,
    sample_training,
)
from runningapp.models.training import TrainingModel


class TrainingModelTests(unittest.TestCase):
    def setUp(self):
        """Set up a test app, test client and test database"""
        set_up_test_app(obj=self, create_app=create_app)
        self.client = set_up_client(self)
        set_up_test_db(db)
        self.user = sample_user()

    def test_training_is_saved_in_db(self):
        """Test if the training has been successfully saved in the database"""
        training = TrainingModel(
            name="test training",
            user_id=self.user.id,
            distance=10,
            avg_tempo=8,
            time_in_seconds=3600,
        )
        training.save_to_db()
        found_training = TrainingModel.find_by_name("test training")

        self.assertIsNotNone(found_training)

    def test_training_is_deleted_from_db(self):
        """Test if the training has been successfully deleted from the database"""
        training = sample_training(self.user)
        training.delete_from_db()
        found_training = TrainingModel.find_by_name("test training")

        self.assertIsNone(found_training)

    def test_find_by_name(self):
        """Test if the training is found"""
        training = sample_training(user=self.user, name="test training")
        found_training = TrainingModel.find_by_name("test training")

        self.assertEqual(found_training, training)

    def test_find_by_name_no_training(self):
        """Test if None is returned if the training with the given name doesn't exist"""
        found_training = TrainingModel.find_by_name("test training")

        self.assertIsNone(found_training)

    def test_find_by_name_and_user_id(self):
        """Test if the training is found"""
        training = sample_training(user=self.user, name="test training")
        found_training = TrainingModel.find_by_name_and_user_id(
            "test training", self.user.id
        )

        self.assertEqual(found_training.name, training.name)
        self.assertEqual(found_training.user_id, self.user.id)

    def test_find_by_name_and_user_id_no_training(self):
        """Test if None is returned if the training with the given name doesn't exist
        among the given user's trainings"""
        found_training = TrainingModel.find_by_name_and_user_id(
            "test training", self.user.id
        )

        self.assertIsNone(found_training)

    def test_find_by_id(self):
        """Test if the training is found"""
        training = sample_training(self.user)
        found_training = TrainingModel.find_by_id(1)

        self.assertEqual(training, found_training)

    def test_find_by_id_no_training(self):
        """Test if None is returned if the training with the given id doesn't exist"""
        found_training = TrainingModel.find_by_id(1)

        self.assertIsNone(found_training)

    def test_find_all_by_user_id(self):
        """Test if all the user's trainings are found"""
        sample_training(self.user, "test training1")
        sample_training(self.user, "test training2")
        found_trainings = TrainingModel.find_all_by_user_id(user_id=self.user.id)

        self.assertEqual(len(found_trainings), 2)

    def test_find_all_by_user_id_current_user_only(self):
        """Test if only trainings which belong to the given user are returned"""
        training1 = sample_training(self.user, "test training1")
        training2 = sample_training(self.user, "test training2")
        user2 = sample_user("user2")
        training3 = sample_training(user2, "test training3")
        found_trainings = TrainingModel.find_all_by_user_id(self.user.id)

        self.assertIn(training1, found_trainings)
        self.assertIn(training2, found_trainings)
        self.assertNotIn(training3, found_trainings)

    def test_find_all_by_user_id_no_trainings(self):
        """Test if an empty list is returned if the user has no trainings"""
        found_trainings = TrainingModel.find_all_by_user_id(self.user.id)

        self.assertEqual(found_trainings, [])

    def test_find_all(self):
        """Test if all trainings which exist in the database are returned"""
        training1 = sample_training(self.user, "test training1")
        training2 = sample_training(self.user, "test training2")
        user2 = sample_user("user2")
        training3 = sample_training(user2, "test training3")
        found_trainings = TrainingModel.find_all()

        self.assertIn(training1, found_trainings)
        self.assertIn(training2, found_trainings)
        self.assertIn(training3, found_trainings)

    def test_find_all_no_trainings(self):
        """Test if an empty list is returned if there are no trainings in the database"""
        found_trainings = TrainingModel.find_all()

        self.assertEqual(found_trainings, [])
