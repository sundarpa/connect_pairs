import sys
import re
import glob

def openquery(myargs):
    if 'query' in myargs:
        query_file = myargs['query']
        with open(query_file, 'r') as fp:
            data = fp.read()

        required_params = set(re.findall(r'"([^"]*)"', data))
        missing_args = required_params - set(myargs.keys())

        if "help" in myargs or "h" in myargs:
            print(f"tquery {' '.join([f'--{arg} <{arg}>' for arg in required_params])} --query {query_file}")
        else:
            if missing_args:
                print("Missing arguments:", missing_args)
                raise SystemExit
            for param in required_params:
                print(f"{param} : {myargs[param]}")

        for k, v in myargs.items():
            data = data.replace(f'"{k}"', f'"{v}"')

        return data

    elif "help" in myargs or "h" in myargs:
        print("Provide --query <queryName.query> from the supported list:")
        dir_path = '/released_path/*.query'
        for queries in glob.glob(dir_path, recursive=True):
            print(queries)

def parse_argv(argv):
    opts = {}
    config_path = None  # Initialize the config_path variable

    while argv:
        if argv[0].startswith("--") or argv[0].startswith("-"):
            option = argv[0][2:]
            if len(argv) > 1 and not argv[1].startswith("--") and not argv[1].startswith("-"):
                if option == 'config':
                    config_path = argv[1]  # Set the config_path if --config is provided
                else:
                    opts[option] = argv[1]  # Assign the value if available
                argv = argv[2:]
            else:
                opts[option] = None  # Assign None if no value is provided
                argv = argv[1:]
        else:
            print("Error: Invalid argument", argv[0])
            return opts, config_path
    return opts, config_path
