class project:
    def __init__(self,title,description,due_date):
        self._title = title
        self._description = description
        self._due_date = due_date
        self._tasks = []
    @property
    def title(self):
        return self._title

    def add_task(self, task):
        self._tasks.append(task)