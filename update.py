# THIS IS NOT THE MAIN CODE. THIS SCRIPT ONLY UPDATES THINGS. MAIN CODE IS LOCATED AT commitify.py

import requests

def download_script(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {filename}")
    
def check_for_updates(version):
    # GitHub API URL for the latest release of the specified repository
    url = "https://api.github.com/repos/kokofixcomputers/commitify/releases/latest"
    
    try:
        # Make a GET request to the GitHub API
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Extract version and other details from the response
            latest_version = data['tag_name']
            release_notes = data['body']
            print(f"Latest Release: {latest_version}")
            return latest_version == version
        else:
            print(f"Failed to fetch updates: {response.status_code} - {response.text}")
            return "Failed to fetch updates"
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
def update_script():
    download_script("https://raw.githubusercontent.com/kokofixcomputers/Commitify/refs/heads/main/commitify.py", "commitify.py")
    print("Commitify script updated successfully!")
    print("Please restart the script.")





