import unittest
from runningapp import create_app
from runningapp.db import db
from runningapp.tests.base_classes import BaseApp, BaseDb, BaseUser, BaseTraining
from runningapp.models.training import TrainingModel


class TrainingModelTests(unittest.TestCase, BaseApp, BaseDb, BaseUser, BaseTraining):
    def setUp(self):
        """Set up a test app, test client and test database"""
        self.app = self._set_up_test_app(create_app)
        self.client = self._set_up_client(self.app)
        self._set_up_test_db(db)
        self.user = self._create_sample_user()

    def test_training_is_saved_in_db(self):
        """Test if the training has been successfully saved in the database"""
        training = TrainingModel(
            name="test training",
            user_id=self.user.id,
            distance=10,
            time_in_seconds=3600,
        )
        training.save_to_db()
        found_training = TrainingModel.find_by_name("test training")

        self.assertIsNotNone(found_training)

    def test_training_is_deleted_from_db(self):
        """Test if the training has been successfully deleted from the database"""
        training = self._create_sample_training(self.user)
        training.delete_from_db()
        found_training = TrainingModel.find_by_name("test training")

        self.assertIsNone(found_training)

    def test_find_by_name(self):
        """Test if the training is found"""
        training = self._create_sample_training(user=self.user, name="test training")
        found_training = TrainingModel.find_by_name("test training")

        self.assertEqual(found_training, training)

    def test_find_by_name_no_training(self):
        """Test if None is returned if the training with the given name doesn't exist"""
        found_training = TrainingModel.find_by_name("test training")

        self.assertIsNone(found_training)

    def test_find_by_name_and_user_id(self):
        """Test if the training is found"""
        training = self._create_sample_training(user=self.user, name="test training")
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
        training = self._create_sample_training(self.user)
        found_training = TrainingModel.find_by_id(1)

        self.assertEqual(training, found_training)

    def test_find_by_id_no_training(self):
        """Test if None is returned if the training with the given id doesn't exist"""
        found_training = TrainingModel.find_by_id(1)

        self.assertIsNone(found_training)

    def test_find_all_by_user_id(self):
        """Test if all the user's trainings are found"""
        self._create_sample_training(self.user, "test training1")
        self._create_sample_training(self.user, "test training2")
        found_trainings = TrainingModel.find_all_by_user_id(user_id=self.user.id)

        self.assertEqual(len(found_trainings), 2)

    def test_find_all_by_user_id_current_user_only(self):
        """Test if only trainings which belong to the given user are returned"""
        training1 = self._create_sample_training(self.user, "test training1")
        training2 = self._create_sample_training(self.user, "test training2")
        user2 = self._create_sample_user("user2")
        training3 = self._create_sample_training(user2, "test training3")
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
        training1 = self._create_sample_training(self.user, "test training1")
        training2 = self._create_sample_training(self.user, "test training2")
        user2 = self._create_sample_user("user2")
        training3 = self._create_sample_training(user2, "test training3")
        found_trainings = TrainingModel.find_all()

        self.assertIn(training1, found_trainings)
        self.assertIn(training2, found_trainings)
        self.assertIn(training3, found_trainings)

    def test_find_all_no_trainings(self):
        """Test if an empty list is returned if there are no trainings in the database"""
        found_trainings = TrainingModel.find_all()

        self.assertEqual(found_trainings, [])

    def test_get_total_kilometers(self):
        """Test if correct total kilometers number is returned"""
        self._create_sample_training(user=self.user, name="test training1", distance=10)
        self._create_sample_training(user=self.user, name="test training2", distance=7)
        kilometers_number = TrainingModel.get_total_kilometers()

        expected_number = 17

        self.assertEqual(kilometers_number, expected_number)

    def test_calculate_total_calories(self):
        """Test if correct total calories number is returned"""
        training1 = self._create_sample_training(
            user=self.user, name="test training1", distance=10
        )
        training2 = self._create_sample_training(
            user=self.user, name="test training2", distance=7
        )
        training1.calculate_calories_burnt()
        training2.calculate_calories_burnt()

        expected_number = training1.calories + training2.calories
        total_calories = TrainingModel.calculate_total_calories()

        self.assertEqual(total_calories, expected_number)

    def test_calculate_met_value_success(self):
        """Test if the met value is calculated correctly"""
        training = self._create_sample_training(
            user=self.user, name="test training1", distance=15, time_in_seconds=3600
        )
        training.calculate_average_tempo()

        expected_met = 13
        met = training._calculate_met_value()

        self.assertEqual(met, expected_met)

    def test_calculate_met_value_failure(self):
        """Test if the met value is calculated incorrectly"""
        training = self._create_sample_training(
            user=self.user, name="test training1", distance=15, time_in_seconds=3600
        )
        training.calculate_average_tempo()

        met = training._calculate_met_value()
        wrong_met = 12
        self.assertNotEqual(met, wrong_met)

    def test_calculate_calories_burnt_success(self):
        """Test if calories burnt during 1 training are calculated correctly"""
        training = self._create_sample_training(
            user=self.user, name="test training1", distance=15, time_in_seconds=3600
        )
        training.calculate_average_tempo()
        training.calculate_calories_burnt()

        expected_calories_burnt = 955

        self.assertEqual(training.calories, expected_calories_burnt)

    def test_calculate_calories_burnt_failure(self):
        """Test if calories burnt during 1 training are calculated incorrectly"""
        training = self._create_sample_training(
            user=self.user, name="test training1", distance=15, time_in_seconds=3600
        )
        training.calculate_average_tempo()
        training.calculate_calories_burnt()

        wrong_calories_burnt = 400

        self.assertNotEqual(training.calories, wrong_calories_burnt)

    def test_calculate_average_tempo_success(self):
        """Test if the average tempo during a training is calculated correctly."""
        training = self._create_sample_training(
            user=self.user, name="test training1", distance=7, time_in_seconds=1800
        )

        training.calculate_average_tempo()
        expected_tempo = 14

        self.assertEqual(training.avg_tempo, expected_tempo)

    def test_calculate_average_tempo_failure(self):
        """Test if the average tempo during a training is calculated incorrectly."""
        training = self._create_sample_training(
            user=self.user, name="test training1", distance=7, time_in_seconds=1800
        )

        training.calculate_average_tempo()
        wrong_tempo = 28

        self.assertNotEqual(training.avg_tempo, wrong_tempo)
