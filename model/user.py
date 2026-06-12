


class Person:


    def __init__(self, name, email):
        self._name = name
        self._email = email

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email


class User(Person):


    def __init__(self, name, email):
        super().__init__(name, email)
        self._projects = []

    @property
    def projects(self):
        return self._projects

    def add_project(self, project):

        self._projects.append(project)

    def to_dict(self):
        
        return {
            "name": self._name,
            "email": self._email,
            "projects": [p.to_dict() if hasattr(p, "to_dict") else p for p in self._projects]
        }

    def __repr__(self):
        return f"User(name='{self._name}', projects={len(self._projects)})"