import argparse
import update_manager
import plugin_manager
import command_router

def main():
    parser = argparse.ArgumentParser(description="Turtles Tools CLI")
    parser.add_argument("command", help="Command to run")
    parser.add_argument("args", nargs="*", help="Arguments for the command")
    args = parser.parse_args()

    if args.command == "update":
        update_manager.check_for_updates()
    elif args.command == "plugins":
        plugin_manager.handle_plugins(args.args)
    else:
        command_router.route_command(args.command, args.args)

if __name__ == "__main__":
    main()
