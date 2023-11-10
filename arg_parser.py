import sys

def parse_argv(argv):
    options = {}
    config_path = None
    csv_module_name = None
    excel_filename = None
    query = None

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg.startswith("--"):
            option_name = arg[2:]
            i += 1
            if i < len(argv):
                option_value = argv[i]
                options[option_name] = option_value
            else:
                options[option_name] = None
        i += 1

    return options, config_path, csv_module_name, excel_filename, query, None  # Add None as the sixth value

# Usage example:

command_line_arguments = sys.argv[1:]  # Get the command line arguments passed to the script
result = parse_argv(command_line_arguments)

# Access the options and their values dynamically
options = result[0]
for option, value in options.items():
    print(f"{option}: {value}")
