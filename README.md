# Project Management CLI Tool

A command-line tool for managing users, projects, and tasks.

## Setup

```bash
# Clone the repository
git clone https://github.com/ccgo14/project_manager_cli.git
cd project_manager_cli

# Install dependencies
pip install -r requirements.txt

# Add a user
python cli/main.py add-user --name "Alex" --email "alex@test.com"

# List all users
python cli/main.py list-users
# Add a project to a user
python cli/main.py add-project --user "alex@test.com" --title "CLI Tool" --description "Build a CLI" --due-date "2026-12-31"

# List user's projects
python cli/main.py list-projects --user "alex@test.com"
# Add a task to a project
python cli/main.py add-task --project "CLI Tool" --title "Implement add-user" --assigned-to "alex@test.com"

# Mark task as complete
python cli/main.py complete-task --project "CLI Tool" --task "Implement add-user"

# List tasks in a project
python cli/main.py list-tasks --project "CLI Tool"
Requirements
Python 3.10+

rich

Author
Caleb Mwaniki
