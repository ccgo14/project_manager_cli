import pytest
from model.user import User


def test_user_creation():
    user = User("Caleb", "caleb@test.com")
    assert user.name == "Caleb"
    assert user.email == "caleb@test.com"
    assert len(user.projects) == 0
