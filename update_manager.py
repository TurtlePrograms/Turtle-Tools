import json
import subprocess
import requests
import os
from zipfile import ZipFile

VERSION = "1.0.0"

def check_for_updates():
    """Check GitHub for the latest release and update if needed."""
    try:
        #use gh cli to get the latest release
        response = subprocess.run(["gh", "release", "list","--exclude-drafts","--exclude-pre-releases","--json","isLatest,name,tagName"], capture_output=True).stdout.decode("utf-8")
        response = json.loads(response)[0]
        print(response)
        latest_version = response["tagName"]
        if latest_version > VERSION:
            print(f"New version available: {latest_version}. Updating...")
            # Get the download URL for the latest release
            download_url = f"https://github.com/TurtlePrograms/Turtle-Tools/archive/refs/tags/{latest_version}.zip"
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