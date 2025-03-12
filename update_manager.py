import requests
import os
from zipfile import ZipFile

VERSION = "1.0.0"
REPO_RELEASES = "https://api.github.com/TurtlePrograms/Turtle-Tools/releases/latest"

def check_for_updates():
    """Check GitHub for the latest release and update if needed."""
    try:
        response = requests.get(REPO_RELEASES).json()
        latest_version = response["tag_name"]

        if latest_version > VERSION:
            print(f"New version available: {latest_version}. Updating...")
            download_url = response["assets"][0]["browser_download_url"]
            update_tool(download_url)
        else:
            print("Turtles Tools is up to date!")
    except Exception as e:
        print("Error checking for updates:", e)

def update_tool(download_url):
    """Download and apply the latest version."""
    zip_path = "update.zip"
    with open(zip_path, "wb") as f:
        f.write(requests.get(download_url).content)

    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(".")
    
    os.remove(zip_path)
    print("Update applied successfully!")
