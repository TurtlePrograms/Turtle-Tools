import os
import json
import requests
import shutil
from zipfile import ZipFile

PLUGINS_DIR = "plugins"
REGISTRY_URL = "https://raw.githubusercontent.com/TurtlePrograms/Turtle-Tools-Registry/main/plugins.json"

os.makedirs(PLUGINS_DIR, exist_ok=True)

def list_plugins():
    """Fetch available plugins from the registry."""
    try:
        plugins = requests.get(REGISTRY_URL).json()["plugins"]
        for name, details in plugins.items():
            print(f"{name}: {details['description']} (v{details['latest_version']})")
    except Exception as e:
        print("Error fetching plugin list:", e)

def install_plugin(plugin_name):
    """Install a plugin from the registry."""
    try:
        plugins = requests.get(REGISTRY_URL).json()["plugins"]
        if plugin_name not in plugins:
            print("Plugin not found!")
            return

        repo_url = plugins[plugin_name]["repo"] + "/archive/refs/heads/main.zip"
        zip_path = f"{plugin_name}.zip"

        with open(zip_path, "wb") as f:
            f.write(requests.get(repo_url).content)

        with ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(PLUGINS_DIR)
        
        os.remove(zip_path)
        print(f"Plugin {plugin_name} installed successfully!")
    except Exception as e:
        print("Error installing plugin:", e)

def remove_plugin(plugin_name):
    """Remove an installed plugin."""
    plugin_path = os.path.join(PLUGINS_DIR, plugin_name)
    if os.path.exists(plugin_path):
        shutil.rmtree(plugin_path)
        print(f"Plugin {plugin_name} removed successfully!")
    else:
        print("Plugin not found!")

def handle_plugins(args):
    """Handle plugin-related commands."""
    if not args:
        list_plugins()
    elif args[0] == "install":
        install_plugin(args[1])
    elif args[0] == "remove":
        remove_plugin(args[1])
    else:
        print("Unknown plugins command:", args[0])