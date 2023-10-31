import sys

def parse_argv(argv):
    opts = {}
    config_path = None
    csv_module_name = None  # Initialize the csv_module_name variable

    while argv:
        if argv[0].startswith("--"):
            option = argv[0][2:]
            if len(argv) > 1 and not argv[1].startswith("--") and not argv[1].startswith("-"):
                if option == 'config':
                    config_path = argv[1]  # Set the config_path if --config is provided
                elif option == 'csvfile':
                    opts[option] = argv[1]  # Assign the value if available
                else:
                    opts[option] = None  # Assign None if no value is provided
                argv = argv[2:]
            else:
                opts[option] = None  # Assign None if no value is provided
                argv = argv[1:]
        elif argv[0].startswith("-"):
            # Handle single character options if needed
            print("Warning: Single character options not supported:", argv[0])
            argv = argv[1:]
        else:
            print("Error: Invalid argument", argv[0])
            return opts, config_path, csv_module_name

    return opts, config_path, csv_module_name
