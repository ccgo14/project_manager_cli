class Project:
    def __init__(self, title, description, due_date):
        self._title = title
        self._description = description
        self._due_date = due_date
        self.tasks = []

    @property
    def title(self):
        return self._title