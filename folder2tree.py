import os

def generate_file_tree(root_dir, ignore_list=None):
    """
    Generates and prints a file tree structure for a given directory.

    Args:
        root_dir (str): The absolute or relative path to the root directory.
        ignore_list (list, optional): A list of directory or file names to ignore. 
                                      Defaults to a common list of virtual environments
                                      and cache directories.
    """
    if ignore_list is None:
        # Common directories to ignore to keep the tree clean
        ignore_list = ['__pycache__', '.git', '.vscode', 'node_modules', 'venv', '.env']

    if not os.path.isdir(root_dir):
        print(f"Error: Directory '{root_dir}' not found.")
        return

    print(f"📁 {os.path.basename(os.path.abspath(root_dir))}")
    _walk_directory(root_dir, "", ignore_list)

def _walk_directory(directory, prefix, ignore_list):
    """
    A recursive helper function to walk through the directory and print its contents.
    
    Args:
        directory (str): The current directory path to walk through.
        prefix (str): The prefix string for printing, to create the tree structure.
        ignore_list (list): A list of directory or file names to ignore.
    """
    # Get all items in the directory and filter out ignored ones
    try:
        items = [item for item in os.listdir(directory) if item not in ignore_list]
    except PermissionError:
        print(f"{prefix}└── [Access Denied]")
        return
        
    # Separate directories and files to print directories first
    dirs = [item for item in items if os.path.isdir(os.path.join(directory, item))]
    files = [item for item in items if os.path.isfile(os.path.join(directory, item))]
    
    # Combine lists, directories first
    all_items = dirs + files
    
    for i, item_name in enumerate(all_items):
        is_last = (i == len(all_items) - 1)
        connector = "└── " if is_last else "├── "
        
        full_path = os.path.join(directory, item_name)
        
        if os.path.isdir(full_path):
            # It's a directory, print its name and recurse
            print(f"{prefix}{connector}📂 {item_name}")
            new_prefix = prefix + ("    " if is_last else "│   ")
            _walk_directory(full_path, new_prefix, ignore_list)
        else:
            # It's a file, just print its name
            print(f"{prefix}{connector}📄 {item_name}")


# --- HOW TO USE THE SCRIPT ---
if __name__ == "__main__":
    # Get the directory of the script itself to run an example
    # You should change this to the path you want to inspect.
    # For example: target_directory = "C:/Users/YourUser/Documents/MyProject"
    # Or use "." to represent the current directory.
    target_directory = "." 

    print("--- Generating File Tree ---")
    generate_file_tree(target_directory)
    print("\n--- End of File Tree ---")

    # Example with a custom ignore list:
    # print("\n--- Generating with Custom Ignore List ---")
    # custom_ignore = ['.git', 'node_modules']
    # generate_file_tree(target_directory, ignore_list=custom_ignore)

