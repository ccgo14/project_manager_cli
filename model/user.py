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
    def add_project(self, project):
        """Adds a project to the user."""
        if project not in self._projects:
            self._projects.append(project)

    def to_dict(self):
        """Converts to dictionary for JSON. Converts objects to simple titles."""
        return {
            "name": self._name,
            "email": self._email,
            "projects": [p.title for p in self._projects]
        }
    @classmethod
    def from_dict(cls, data):
        """Creates a User instance from dictionary data."""
        return cls(data["name"], data["email"])
