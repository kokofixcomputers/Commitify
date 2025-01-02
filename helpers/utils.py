import platform
import os
import subprocess

def fetch_platform():
    # Get the OS name
    os_name = platform.system()
    return os_name

def is_git_directory():
    # Get the current working directory
    current_dir = os.getcwd()
    
    # Check if the .git directory exists
    git_dir = os.path.join(current_dir, '.git')
    
    if os.path.isdir(git_dir):
        try:
            subprocess.run(["git", "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    else:
        return False

def get_git_remotes():
    # Check if the current directory is a Git repository
    if not os.path.isdir('.git'):
        print("This directory is not a Git repository.")
        return []

    try:
        # Run the git remote -v command to get the list of remotes
        result = subprocess.run(
            ["git", "remote", "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        
        # Split the output into lines
        remote_lines = result.stdout.splitlines()
        
        # Use a set to track unique URLs
        seen_urls = set()
        remotes = []
        
        for line in remote_lines:
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                url = parts[1]
                
                # Only add the URL if it hasn't been seen before
                if url not in seen_urls:
                    seen_urls.add(url)
                    remotes.append((name, url))  # Store as a tuple (name, url)
        
        return remotes
    
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving remotes: {e.stderr}")
        return []

def get_git_branches():
    # Check if the current directory is a Git repository
    if not os.path.isdir('.git'):
        print("This directory is not a Git repository.")
        return []

    try:
        # Run the git branch command to get the list of branches
        result = subprocess.run(
            ["git", "branch"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        
        # Split the output into lines and strip whitespace
        branches = [branch.strip() for branch in result.stdout.splitlines()]
        
        # Remove leading asterisks and spaces from the current branch indicator
        branches = [branch.lstrip('* ').strip() for branch in branches]
        
        return branches
    
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving branches: {e.stderr}")
        return []