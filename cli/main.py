"""Entry point for the Project Management CLI tool."""

import argparse
from utils.storage import load_data, save_data


def main():
    """Main CLI execution logic."""
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Command: add-user
    parser_user = subparsers.add_parser("add-user", help="Add a new user")
    parser_user.add_argument("--name", required=True, help="User's name")
    parser_user.add_argument("--email", required=True, help="User's email")

    args = parser.parse_args()

    if args.command == "add-user":
        # Logic to handle adding user
        data = load_data()
        new_user = {"name": args.name, "email": args.email}
        data.append(new_user)
        save_data(data)
        print(f"User {args.name} added successfully!")


if __name__ == "__main__":
    main()
