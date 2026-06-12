import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from utils.storage import load_data, save_data
from model.user import User
from model.project import Project
from model.task import Task

console = Console()


def list_users():
    """Display all users in a formatted table."""
    users = load_data()
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return

    table = Table(title="System Users")
    table.add_column("Name", style="cyan")
    table.add_column("Email", style="magenta")
    table.add_column("Projects", style="green")

    for u in users:
        project_count = len(u.get("projects", []))
        table.add_row(u["name"], u["email"], str(project_count))

    console.print(table)


def list_projects(user_email):
    """Display all projects for a specific user."""
    users = load_data()
    user = next((u for u in users if u["email"] == user_email), None)

    if not user:
        console.print(f"[red]User {user_email} not found![/red]")
        return

    projects = user.get("projects", [])
    if not projects:
        console.print(f"[yellow]No projects for {user_email}[/yellow]")
        return

    table = Table(title=f"Projects for {user['name']}")
    table.add_column("Title", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Due Date", style="yellow")
    table.add_column("Tasks", style="green")

    for p in projects:
        task_count = len(p.get("tasks", []))
        table.add_row(p["title"], p["description"], p.get("due_date", "N/A"), str(task_count))

    console.print(table)


def list_tasks(project_title):
    """Display all tasks for a specific project."""
    users = load_data()

    for user in users:
        for project in user.get("projects", []):
            if project["title"] == project_title:
                tasks = project.get("tasks", [])
                if not tasks:
                    console.print(f"[yellow]No tasks for project '{project_title}'[/yellow]")
                    return

                table = Table(title=f"Tasks for {project_title}")
                table.add_column("Title", style="cyan")
                table.add_column("Status", style="green")
                table.add_column("Assigned To", style="magenta")

                for t in tasks:
                    status_icon = "✅" if t["status"] == "Completed" else "🔄"
                    table.add_row(t["title"], f"{status_icon} {t['status']}", t["assigned_to"])

                console.print(table)
                return

    console.print(f"[red]Project '{project_title}' not found![/red]")


def main():
    """Main CLI execution logic."""
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # ============================================
    # USER COMMANDS
    # ============================================

    # Add-user command
    parser_add_user = subparsers.add_parser("add-user", help="Add a new user")
    parser_add_user.add_argument("--name", required=True, help="User's name")
    parser_add_user.add_argument("--email", required=True, help="User's email")

    # List-users command
    subparsers.add_parser("list-users", help="List all users")

    # ============================================
    # PROJECT COMMANDS
    # ============================================

    # Add-project command
    parser_add_project = subparsers.add_parser("add-project", help="Add project to user")
    parser_add_project.add_argument("--user", required=True, help="User email")
    parser_add_project.add_argument("--title", required=True, help="Project title")
    parser_add_project.add_argument("--description", default="", help="Project description")
    parser_add_project.add_argument("--due-date", default="", help="Due date (YYYY-MM-DD)")

    # List-projects command
    parser_list_projects = subparsers.add_parser("list-projects", help="List user's projects")
    parser_list_projects.add_argument("--user", required=True, help="User email")

    # ============================================
    # TASK COMMANDS
    # ============================================

    # Add-task command
    parser_add_task = subparsers.add_parser("add-task", help="Add task to project")
    parser_add_task.add_argument("--project", required=True, help="Project title")
    parser_add_task.add_argument("--title", required=True, help="Task title")
    parser_add_task.add_argument("--assigned-to", required=True, help="Assigned user email")

    # Complete-task command
    parser_complete_task = subparsers.add_parser("complete-task", help="Mark task as complete")
    parser_complete_task.add_argument("--project", required=True, help="Project title")
    parser_complete_task.add_argument("--task", required=True, help="Task title")

    # List-tasks command
    parser_list_tasks = subparsers.add_parser("list-tasks", help="List tasks in a project")
    parser_list_tasks.add_argument("--project", required=True, help="Project title")

    args = parser.parse_args()

    # ============================================
    # HANDLE COMMANDS
    # ============================================

    if args.command == "list-users":
        list_users()

    elif args.command == "add-user":
        users = load_data()
        existing = [u for u in users if u["email"] == args.email]
        if existing:
            console.print(f"[red]User with email {args.email} already exists![/red]")
        else:
            new_user = {"name": args.name, "email": args.email, "projects": []}
            users.append(new_user)
            save_data(users)
            console.print(f"[green]✓ User {args.name} added successfully![/green]")

    elif args.command == "add-project":
        users = load_data()
        user = next((u for u in users if u["email"] == args.user), None)

        if not user:
            console.print(f"[red]User {args.user} not found![/red]")
        else:
            if "projects" not in user:
                user["projects"] = []

            # Check if project already exists
            existing = [p for p in user["projects"] if p["title"] == args.title]
            if existing:
                console.print(f"[red]Project '{args.title}' already exists for this user![/red]")
            else:
                user["projects"].append({
                    "title": args.title,
                    "description": args.description,
                    "due_date": args.due_date,
                    "tasks": []
                })
                save_data(users)
                console.print(f"[green]✓ Project '{args.title}' added to {args.user}![/green]")

    elif args.command == "list-projects":
        list_projects(args.user)

    elif args.command == "add-task":
        users = load_data()
        task_added = False

        for user in users:
            for project in user.get("projects", []):
                if project["title"] == args.project:
                    if "tasks" not in project:
                        project["tasks"] = []

                    # Check if task already exists
                    existing = [t for t in project["tasks"] if t["title"] == args.title]
                    if existing:
                        console.print(f"[red]Task '{args.title}' already exists in this project![/red]")
                        task_added = True
                        break

                    project["tasks"].append({
                        "title": args.title,
                        "status": "Pending",
                        "assigned_to": args.assigned_to
                    })
                    save_data(users)
                    console.print(f"[green]✓ Task '{args.title}' added to project '{args.project}'![/green]")
                    task_added = True
                    break
            if task_added:
                break

        if not task_added:
            console.print(f"[red]Project '{args.project}' not found![/red]")

    elif args.command == "complete-task":
        users = load_data()
        task_completed = False

        for user in users:
            for project in user.get("projects", []):
                if project["title"] == args.project:
                    for task in project.get("tasks", []):
                        if task["title"] == args.task:
                            task["status"] = "Completed"
                            save_data(users)
                            console.print(f"[green]✓ Task '{args.task}' marked as complete![/green]")
                            task_completed = True
                            break
                    if task_completed:
                        break
            if task_completed:
                break

        if not task_completed:
            console.print(f"[red]Task '{args.task}' not found in project '{args.project}'![/red]")

    elif args.command == "list-tasks":
        list_tasks(args.project)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()