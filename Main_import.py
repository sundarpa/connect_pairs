import importlib

# Specify the module name (without the '.py' extension)
module_name = "dynamic_link"

# Dynamically import the module
try:
    imported_module = importlib.import_module(module_name)
    print(f"Module '{module_name}' imported successfully.")
except ImportError:
    print(f"Failed to import module '{module_name}'.")

# Use a function from the imported module
if hasattr(imported_module, "greet") and callable(imported_module.greet):
    result = imported_module.greet("Alice")
    print(result)
else:
    print(f"Module '{module_name}' does not have a 'greet' function.")
