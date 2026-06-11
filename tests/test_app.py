from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant():
    test_email = "test.student@mergington.edu"
    response = client.post("/activities/Chess%20Club/signup", params={"email": test_email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {test_email} for Chess Club"

    response = client.get("/activities")
    assert test_email in response.json()["Chess Club"]["participants"]


def test_remove_participant_from_activity():
    test_email = "remove.student@mergington.edu"
    client.post("/activities/Chess%20Club/signup", params={"email": test_email})

    response = client.delete("/activities/Chess%20Club/participants", params={"email": test_email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {test_email} from Chess Club"

    response = client.get("/activities")
    assert test_email not in response.json()["Chess Club"]["participants"]
