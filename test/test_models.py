import pytest
from model.user import User
from model.project import Project
from model.task import Task


def test_user_creation():
    user = User("Caleb", "caleb@test.com")
    assert user.name == "Caleb"
    assert user.email == "caleb@test.com"
    assert len(user.projects) == 0


def test_project_creation():
    project = Project("CLI Tool", "Build a CLI", "2026-06-13")
    assert project.title == "CLI Tool"
    assert project.description == "Build a CLI"
    assert project.due_date == "2026-06-13"
    assert project.tasks == []


def test_project_add_task():
    project = Project("CLI Tool", "Build a CLI", "2026-06-13")
    task = Task("Implement add-task", "Caleb")
    project.add_task(task)
    assert len(project.tasks) == 1
    assert project.tasks[0].title == "Implement add-task"


def test_project_to_dict():
    project = Project("CLI Tool", "Build a CLI", "2026-06-13")
    task = Task("Implement add-task", "Caleb")
    project.add_task(task)
    result = project.to_dict()
    assert result["title"] == "CLI Tool"
    assert len(result["tasks"]) == 1


def test_task_creation():
    task = Task("Write docs", "Caleb")
    assert task.title == "Write docs"
    assert task.assigned_to == "Caleb"
    assert task.status == "Pending"


def test_task_status_update():
    task = Task("Write docs", "Caleb")
    task.status = "Completed"
    assert task.status == "Completed"


def test_task_invalid_status():
    task = Task("Write docs", "Caleb")
    with pytest.raises(ValueError):
        task.status = "InProgress"


def test_task_to_dict():
    task = Task("Write docs", "Caleb")
    expected = {"title": "Write docs", "status": "Pending", "assigned_to": "Caleb"}
    assert task.to_dict() == expected