"""Module for managing user data."""


class User:
    """Represents a system user."""

    def __init__(self, name, email):
        """Initialize a new user with a name and email."""
        self._name = name
        self._email = email
        self._projects = []

    @property
    def name(self):
        """Get the user's name."""
        return self._name

    @property
    def email(self):
        """Get the user's email."""
        return self._email
    @property
    def projects(self):
        """Get the user's projects."""
        return self._projects

    def to_dict(self):
        """Convert user instance to a dictionary for JSON storage."""
        return {
            "name": self._name,
            "email": self._email,
            "projects": self._projects
        }
