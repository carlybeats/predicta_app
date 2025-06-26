import pytest
import os
from pydantic import ValidationError

from api import get_predictions, get_user, create_user, write_predictions, NewUser, Prediction

os.environ["TESTING"] = "True"

class TestCreateUser:

    def test_create_user_success(self):
        valid_user = NewUser(first_name='valid', last_name='user')
        result = create_user(valid_user)
        assert result == {"success": "new user created"}
        
    def test_invalid_user_creation(self):
        with pytest.raises(ValidationError):
            invalid_user = NewUser(first_name='invalid', last_name=7)
        with pytest.raises(ValidationError):
            invalid_user = NewUser()

class TestRetrieveUser:

    def test_retrieve_user_success(self):
       user = get_user(1)
       assert user == {'user_id': 1, 'first_name': 'valid', 'last_name': 'user'}

    def test_user_doesnt_exist(self):
        user = get_user(100000000)
        assert user == {"error": "user not found"}

class TestCreatePredictions:

    def test_valid_predictions(self):
        predictions = [
        Prediction(prediction="Valid"),
        Prediction(prediction="Valid", friend_name="Friend", friend_prediction="Valid2"),
        Prediction(prediction="Valid", friend_name="Friend", friend_prediction="Valid2", stake=5)]

        for prediction in predictions:
            assert write_predictions(prediction, user_id=1) == {"success": "prediction made"}

    def test_invalid_predictions(self):
        with pytest.raises(ValidationError):
            Prediction(prediction=7)

        with pytest.raises(ValidationError):
            Prediction(prediction="valid", friend_name=7)


class TestGetPredictions:

    def test_predictions_exist(self):
        predictions = get_predictions(1)
        assert predictions[0]['user_id'] == 1
        assert predictions[0]['prediction'] == 'Valid'

    def test_predictions_dont_exist(self):
        predictions = get_predictions(2)
        assert predictions == []