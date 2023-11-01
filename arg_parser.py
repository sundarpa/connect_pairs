def parse_argv(argv):
    opts = {}
    config_path = None
    csv_module_name = None
    excel_filename = None  # Initialize the excel_filename variable

    while argv:
        if argv[0].startswith("--"):
            option = argv[0][2:]
            if len(argv) > 1 and not argv[1].startswith("--") and not argv[1].startswith("-"):
                if option == 'config':
                    config_path = argv[1]
                elif option == 'csvfile':
                    opts[option] = argv[1]
                elif option == 'excelfile':
                    opts[option] = argv[1]  # Set the excel_filename if --excelfile is provided
                else:
                    opts[option] = None
                argv = argv[2:]
            else:
                opts[option] = None
                argv = argv[1:]
        elif argv[0].startswith("-"):
            print("Warning: Single character options not supported:", argv[0])
            argv = argv[1:]
        else:
            print("Error: Invalid argument", argv[0])
            return opts, config_path, csv_module_name, excel_filename

    return opts, config_path, csv_module_name, excel_filename

