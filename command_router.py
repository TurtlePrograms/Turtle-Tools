import os
import importlib.util
import json

PLUGINS_DIR = "plugins"

def route_command(command, args):
    """Check if a command belongs to a plugin and execute it."""
    for plugin_name in os.listdir(PLUGINS_DIR):
        plugin_path = os.path.join(PLUGINS_DIR, plugin_name)
        config_path = os.path.join(plugin_path, "plugin.json")

        if os.path.isdir(plugin_path) and os.path.exists(config_path):
            with open(config_path, "r") as f:
                plugin_config = json.load(f)

            # If the command matches a plugin command, execute it
            if command in plugin_config.get("commands", []):
                execute_plugin(plugin_path, plugin_config["entry_point"], command, args)
                return

    print(f"Unknown command: {command}")

def execute_plugin(plugin_path, entry_point, command, args):
    """Dynamically import and run the plugin's entry point."""
    module_path = os.path.join(plugin_path, entry_point)
    module_name = f"plugins.{os.path.basename(plugin_path)}"

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, "main"):
        module.main(command, args)
    else:
        print(f"Error: Plugin {module_name} does not have a 'main' function.")
