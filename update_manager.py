import json
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
    install_dependencies()
    print("Update applied successfully!")

def install_dependencies():
    """Install the required dependencies for Turtles Tools."""
    print("Installing Turtles Tools...")
    os.makedirs("plugins", exist_ok=True)
    dependencies = ["requests"]
    for plugin_name in os.listdir("plugins"):
        config_path = os.path.join("plugins", plugin_name, "plugin.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                plugin_config = json.load(f)
                for dep in plugin_config.get("dependencies", []):
                    dependencies.append(dep)
    os.system("pip install " + " ".join(dependencies))
    print("Turtles Tools installed successfully!")