#!/bin/sh

# Navigate to the project directory
cd "$(dirname "$0")/../.." || exit 1

# debug, sending notif with current directory
# pwd | terminal-notifier -message

# Activate the virtual environment
source .venv/bin/activate

# Generate the requirements.txt file
pip freeze > src/api/requirements.txt || exit 0

# add requirements.txt to commit
git add src/api/requirements.txt || exit 1

# Deactivate the virtual environment
deactivate

# notify the user that the pre-commit script has successfully been run.
if command -v terminal-notifier > /dev/null 2>&1; then
    terminal-notifier -message "pre commit: updated requirements.txt" 
else
    echo "terminal-notifier is not installed."
fi