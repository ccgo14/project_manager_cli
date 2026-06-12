import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
from rich.console import Console
from rich.table import Table
from utils.storage import load_data, save_data
from model.user import User
from model.project import Project
from model.task import Task

console = Console()


def find_user(users, name):
    """Find a user dict by name."""
    for u in users:
        if u["name"] == name:
            return u
    return None


def find_project(user, title):
    """Find a project dict within a user's projects by title."""
    for p in user.get("projects", []):
        if p["title"] == title:
            return p
    return None


def find_task(project, title):
    """Find a task dict within a project's tasks by title."""
    for t in project.get("tasks", []):
        if t["title"] == title:
            return t
    return None


def list_users():
    users = load_data()
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return
    table = Table(title="System Users")
    table.add_column("Name", style="cyan")
    table.add_column("Email", style="magenta")
    table.add_column("Projects", style="green")
    for u in users:
        table.add_row(u["name"], u["email"], str(len(u.get("projects", []))))
    console.print(table)


def add_user(args):
    users = load_data()
    if find_user(users, args.name):
        console.print(f"[red]User '{args.name}' already exists![/red]")
        return
    new_user = User(args.name, args.email)
    users.append(new_user.to_dict())
    save_data(users)
    console.print(f"[green]✓ User {args.name} added successfully![/green]")


def add_project(args):
    users = load_data()
    user = find_user(users, args.user)
    if not user:
        console.print(f"[red]User '{args.user}' not found![/red]")
        return
    if find_project(user, args.title):
        console.print(f"[red]Project '{args.title}' already exists for {args.user}![/red]")
        return
    new_project = Project(args.title, args.description, args.due_date)
    user.setdefault("projects", []).append(new_project.to_dict())
    save_data(users)
    console.print(f"[green]✓ Project '{args.title}' added to {args.user}![/green]")


def add_task(args):
    users = load_data()
    for user in users:
        project = find_project(user, args.project)
        if project:
            if find_task(project, args.title):
                console.print(f"[red]Task '{args.title}' already exists in '{args.project}'![/red]")
                return
            new_task = Task(args.title, args.assigned_to)
            project.setdefault("tasks", []).append(new_task.to_dict())
            save_data(users)
            console.print(f"[green]✓ Task '{args.title}' added to '{args.project}'![/green]")
            return
    console.print(f"[red]Project '{args.project}' not found![/red]")


def list_projects(args):
    users = load_data()
    table = Table(title="Projects")
    table.add_column("Owner", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Description", style="white")
    table.add_column("Due Date", style="yellow")
    table.add_column("Tasks", style="green")

    found = False
    for user in users:
        if args.user and user["name"] != args.user:
            continue
        for p in user.get("projects", []):
            table.add_row(user["name"], p["title"], p["description"], p["due_date"], str(len(p.get("tasks", []))))
            found = True

    if not found:
        console.print("[yellow]No projects found.[/yellow]")
        return
    console.print(table)


def complete_task(args):
    users = load_data()
    for user in users:
        project = find_project(user, args.project)
        if project:
            task = find_task(project, args.title)
            if not task:
                console.print(f"[red]Task '{args.title}' not found in '{args.project}'![/red]")
                return
            task["status"] = "Completed"
            save_data(users)
            console.print(f"[green]✓ Task '{args.title}' marked as Completed![/green]")
            return
    console.print(f"[red]Project '{args.project}' not found![/red]")


def main():
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    p_add_user = subparsers.add_parser("add-user", help="Add a new user")
    p_add_user.add_argument("--name", required=True, help="User's name")
    p_add_user.add_argument("--email", required=True, help="User's email")

    subparsers.add_parser("list-users", help="List all users")

    p_add_project = subparsers.add_parser("add-project", help="Add a project to a user")
    p_add_project.add_argument("--user", required=True, help="Owner's name")
    p_add_project.add_argument("--title", required=True, help="Project title")
    p_add_project.add_argument("--description", default="", help="Project description")
    p_add_project.add_argument("--due-date", dest="due_date", default="", help="Due date (YYYY-MM-DD)")

    p_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    p_add_task.add_argument("--project", required=True, help="Project title")
    p_add_task.add_argument("--title", required=True, help="Task title")
    p_add_task.add_argument("--assigned-to", dest="assigned_to", required=True, help="Assignee name")

    p_list_projects = subparsers.add_parser("list-projects", help="List all projects")
    p_list_projects.add_argument("--user", default=None, help="Filter by user name")

    p_complete_task = subparsers.add_parser("complete-task", help="Mark a task as completed")
    p_complete_task.add_argument("--project", required=True, help="Project title")
    p_complete_task.add_argument("--title", required=True, help="Task title")

    args = parser.parse_args()

    if args.command == "list-users":
        list_users()
    elif args.command == "add-user":
        add_user(args)
    elif args.command == "add-project":
        add_project(args)
    elif args.command == "add-task":
        add_task(args)
    elif args.command == "list-projects":
        list_projects(args)
    elif args.command == "complete-task":
        complete_task(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()