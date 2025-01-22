import os
from dotenv import load_dotenv
from github import Github

load_dotenv()

def increment_number_in_file(file_path: str) -> str:
    """
    Increments the number in the given file. If the file does not exist, it creates it with the number 1.

    Args:
        file_path (str): The path to the file
    
    Returns:
        str: The new content of the file
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            number = int(file.read().strip())
        number += 1
    else:
        number = 1

    with open(file_path, 'w') as file:
        file.write(str(number))
    
    return str(number)

def commit_to_github(token: str, repo_name: str, file_path: str, branch: str = "main", commit_message: str = "automated commit") -> None:
    """
    Commits the given file to a GitHub repository.

    Args:
        token (str): The GitHub token
        repo_name (str): The name of the repository
        file_path (str): The path to the file to commit
        branch (str): The branch to commit to
        commit_message (str): The commit message
    
    Returns:
        None
    """
    # Authenticate with GitHub
    g = Github(token)
    repo = g.get_repo(repo_name)

    with open(file_path, 'r') as file:
        content_string = file.read()

    try:
        # Check if the file already exists
        file = repo.get_contents(file_path, ref=branch)

        # Update the existing file
        repo.update_file(
            path=file.path,
            message=commit_message,
            content=content_string,
            sha=file.sha,
            branch=branch
        )
        print(f"Updated file at {file_path}")
    except:
        print(f"path not found: {file_path}")
        # Create a new file
        repo.create_file(
            path=file_path,
            message=commit_message,
            content=content_string,
            branch=branch
        )
        print(f"Created new file at {file_path}")

# GitHub Upload variables
GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN")
REPO_NAME: str = "Lars-Ostervold/i-like-green-trees"
FILE_PATH: str = "increment.txt"
BRANCH: str = "main"
COMMIT_MESSAGE: str = "Automated commit: Incremented number"

# Increment the number in the file
increment_number_in_file(FILE_PATH)

# Commit the file to GitHub
commit_to_github(GITHUB_TOKEN, REPO_NAME, FILE_PATH, BRANCH, COMMIT_MESSAGE)