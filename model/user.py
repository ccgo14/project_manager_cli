"""Module for managing user data."""


class USser:
    """Represents a system user."""

    def __init__(self, name, email):
        """Initialize a new user with a name and email."""
        self._name = name
        self._email = email
        self._project = []

    @property
    def name(self):
        """Get the user's name."""
        return self._name

    @property
    def email(self):
        """Get the user's email."""
        return self._email
