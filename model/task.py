class Task:

    def __init__(self, title, assigned_to):
        self._title = title
        self._status = "Pending"
        self._assigned_to = assigned_to

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in ["Pending", "Completed"]:
            raise ValueError("Status must be 'Pending' or 'Completed'")
        self._status = value