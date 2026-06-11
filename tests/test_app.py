from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)

ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities_state():
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))


def test_get_activities_returns_activities():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity in data
    assert isinstance(data[expected_activity]["participants"], list)


def test_signup_for_activity_adds_participant():
    # Arrange
    test_email = "test.student@mergington.edu"
    activity_path = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(activity_path, params={"email": test_email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {test_email} for Chess Club"

    activities_response = client.get("/activities")
    assert test_email in activities_response.json()["Chess Club"]["participants"]


def test_remove_participant_from_activity():
    # Arrange
    test_email = "remove.student@mergington.edu"
    signup_path = "/activities/Chess%20Club/signup"
    remove_path = "/activities/Chess%20Club/participants"
    client.post(signup_path, params={"email": test_email})

    # Act
    response = client.delete(remove_path, params={"email": test_email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {test_email} from Chess Club"

    activities_response = client.get("/activities")
    assert test_email not in activities_response.json()["Chess Club"]["participants"]
