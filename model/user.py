class User:
    def __init__(self, name, email):
        self._name = name
        self._email = email
        self._projects = []

    @property
    def name(self): return self._name

    @property
    def email(self): return self._email

    @property
    def projects(self): return self._projects

    def add_project(self, project):
        if project not in self._projects:
            self._projects.append(project)

    def to_dict(self):

        return {
            "name": self._name,
            "email": self._email,
            "projects": [p.title for p in self._projects]
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["email"])