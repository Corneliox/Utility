import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def validate_directory_pairs():
    """
    Main function to orchestrate the validation process. It browses for a root
    directory, recursively finds all subdirectories containing dataset files,
    validates them, and reports any issues.
    """
    # --- Step 1: Get Root Folder from User ---
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Directory Pair Validator", "Please select the root folder containing your dataset.")
    root_dir = filedialog.askdirectory(title="Select Root Dataset Folder")
    
    if not root_dir:
        print("No folder selected. Aborting.")
        return

    print(f"Validating root folder: {root_dir}")
    print("Searching for dataset files in all subdirectories...")
    print("-" * 30)

    # --- Step 2: Recursively Find and Validate Subdirectories ---
    invalid_subdirs = []
    
    # Use os.walk to go through all directories and subdirectories
    for dirpath, _, filenames in os.walk(root_dir):
        # Check if the current directory contains any relevant dataset files
        has_dataset_files = any(f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp', '.txt')) for f in filenames)

        if has_dataset_files:
            # This is a folder we need to validate
            print(f"Checking: {os.path.relpath(dirpath, root_dir)}...")
            is_valid = check_pairs_in_subdirectory(dirpath)
            if not is_valid:
                # Get the path relative to the root folder for clear reporting
                relative_path = os.path.relpath(dirpath, root_dir)
                invalid_subdirs.append(relative_path)
                print(f"🔴 Invalid: Directory '{relative_path}' has missing pairs.")
            else:
                print(f"✅ Valid: Directory '{os.path.relpath(dirpath, root_dir)}' is OK.")

    # --- Step 3: Show the Final Report ---
    print("\n--- Validation Scan Complete ---")
    show_results_window(invalid_subdirs)

def check_pairs_in_subdirectory(subdir_path):
    """
    Validates a single subdirectory to ensure each image has a corresponding
    text file where the image's base name is contained within the text file's name.

    Args:
        subdir_path (str): The full path to the subdirectory to check.

    Returns:
        bool: True if all image files have a valid text pair, False otherwise.
    """
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.webp'}
    image_bases = set()
    text_file_names = set()

    try:
        for filename in os.listdir(subdir_path):
            base_name, extension = os.path.splitext(filename)
            ext_lower = extension.lower()

            if ext_lower in image_extensions:
                image_bases.add(base_name)
            elif ext_lower == '.txt':
                text_file_names.add(base_name)
    
        if not image_bases:
            return True # No images to validate, so it's considered valid.

        # For every image, check if a corresponding text file exists
        for img_base in image_bases:
            found_match = False
            for txt_name in text_file_names:
                if img_base.lower() in txt_name.lower():
                    found_match = True
                    break # Found a match, no need to check other text files
            
            if not found_match:
                # An image is missing its text pair, this directory is invalid
                return False

        # If we get here, all images had a match
        return True

    except Exception as e:
        print(f"Error processing subdirectory '{subdir_path}': {e}")
        return False # Treat directories with errors as invalid

def show_results_window(invalid_list):
    """
    Creates a new Tkinter window to display the list of invalid directories
    and provide a copy-to-clipboard button.
    """
    results_window = tk.Toplevel()
    results_window.title("Validation Results")
    results_window.geometry("500x400")

    main_frame = tk.Frame(results_window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    if not invalid_list:
        message = "🎉 All subdirectories are valid! 🎉\n\nEvery image file in every relevant folder has a corresponding text file."
        label = tk.Label(main_frame, text=message, justify=tk.CENTER, font=("Helvetica", 12))
        label.pack(pady=20, fill=tk.BOTH, expand=True)
        return

    label_text = "The following directories have missing image-text pairs:"
    label = tk.Label(main_frame, text=label_text, justify=tk.LEFT)
    label.pack(anchor='w', pady=(0, 5))

    text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=15, width=60)
    text_area.pack(fill=tk.BOTH, expand=True)
    
    # Use os.path.normpath to clean up paths for consistent display (e.g. \ vs /)
    result_string = "\n".join(sorted([os.path.normpath(p) for p in invalid_list]))
    text_area.insert(tk.INSERT, result_string)
    text_area.config(state=tk.DISABLED) # Make it read-only

    def copy_to_clipboard():
        results_window.clipboard_clear()
        results_window.clipboard_append(result_string)
        messagebox.showinfo("Copied!", "The list of invalid directories has been copied to your clipboard.", parent=results_window)

    copy_button = tk.Button(main_frame, text="Copy List to Clipboard", command=copy_to_clipboard)
    copy_button.pack(pady=10)

# --- How to Run the Script ---
if __name__ == "__main__":
    validate_directory_pairs()
