class Project:
    def __init__(self, title, description, due_date):
        self._title = title
        self._description = description
        self._due_date = due_date
        self.tasks = []

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def due_date(self):
        return self._due_date

    def add_task(self, task):
        self.tasks.append(task)

    def to_dict(self):
        return {
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    def __repr__(self):
        return f"Project(title='{self._title}', tasks={len(self.tasks)})"