import argparse
import sys
import os

from rich.console import Console
from rich.table import Table
from utils.storage import load_data, save_data
from model.user import User

# Add path to allow local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))




console = Console()


def list_users():
    users = load_data()
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return

    table = Table(title="System Users")
    table.add_column("Name", style="cyan")
    table.add_column("Email", style="magenta")

    for u in users:
        table.add_row(u["name"], u["email"])

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    parser_add = subparsers.add_parser("add-user", help="Add a new user")
    parser_add.add_argument("--name", required=True, help="User's name")
    parser_add.add_argument("--email", required=True, help="User's email")

    subparsers.add_parser("list-users", help="List all users")

    args = parser.parse_args()

    if args.command == "list-users":
        list_users()
    elif args.command == "add-user":
        users = load_data()
        existing = [u for u in users if u["email"] == args.email]
        if existing:
            console.print(f"[red]User with email {args.email} already exists![/red]")
        else:
            new_user = User(args.name, args.email)
            users.append(new_user.to_dict())
            save_data(users)
            console.print(f"[green]✓ User {args.name} added successfully![/green]")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
