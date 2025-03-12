import os
import json
import requests
import shutil
from zipfile import ZipFile

import update_manager

PLUGINS_DIR = "plugins"
REGISTRY_URL = "https://raw.githubusercontent.com/TurtlePrograms/Turtle-Tools-Registry/main/plugins.json"

os.makedirs(PLUGINS_DIR, exist_ok=True)

def list_all_plugins():
    """Fetch available plugins from the registry."""
    try:
        plugins = requests.get(REGISTRY_URL).json()["plugins"]
        for name, details in plugins.items():
            print(f"{name}: {details['description']} (v{details['latest_version']})")
    except Exception as e:
        print("Error fetching plugin list:", e)

def list_installed_plugins():
    """List all installed plugins."""
    for plugin_name in os.listdir(PLUGINS_DIR):
        config_path = os.path.join(PLUGINS_DIR, plugin_name, "plugin.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                plugin_config = json.load(f)
            print(f"{plugin_name}: {plugin_config['description']} (v{plugin_config['version']})")

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
        update_manager.install_dependencies()
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
        list_all_plugins()
    elif args[0] == "list":
        list_installed_plugins()
    elif args[0] == "install":
        install_plugin(args[1])
    elif args[0] == "remove":
        remove_plugin(args[1])
    else:
        print("Unknown plugins command:", args[0])