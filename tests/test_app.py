import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original = {
        name: {
            "description": data["description"],
            "schedule": data["schedule"],
            "max_participants": data["max_participants"],
            "participants": list(data["participants"]),
        }
        for name, data in activities.items()
    }
    yield
    activities.clear()
    activities.update(original)


def test_unregister_participant_removes_email():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert delete_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
