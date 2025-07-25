import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def validate_directory_pairs():
    """
    Main function to orchestrate the validation process. It browses for a root
    directory, recursively finds all subdirectories containing dataset files,
    validates them, and reports any issues including the specific missing files.
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
    validation_issues = {} # Dictionary to store {directory: [list_of_missing_files]}
    
    for dirpath, _, filenames in os.walk(root_dir):
        has_dataset_files = any(f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp', '.txt')) for f in filenames)

        if has_dataset_files:
            relative_path = os.path.relpath(dirpath, root_dir)
            print(f"Checking: {relative_path}...")
            
            missing_files = check_pairs_in_subdirectory(dirpath)
            if missing_files:
                # If the list of missing files is not empty, the directory is invalid
                validation_issues[relative_path] = missing_files
                print(f"🔴 Invalid: Directory '{relative_path}' has {len(missing_files)} missing pair(s).")
            else:
                print(f"✅ Valid: Directory '{relative_path}' is OK.")

    # --- Step 3: Show the Final Report ---
    print("\n--- Validation Scan Complete ---")
    show_results_window(root, validation_issues)

def check_pairs_in_subdirectory(subdir_path):
    """
    Validates a single subdirectory.

    Args:
        subdir_path (str): The full path to the subdirectory to check.

    Returns:
        list: A list of image base names that are missing a text pair. 
              Returns an empty list if the directory is valid.
    """
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.webp'}
    image_bases = set()
    text_file_names = set()
    images_missing_pairs = []

    try:
        for filename in os.listdir(subdir_path):
            base_name, extension = os.path.splitext(filename)
            ext_lower = extension.lower()

            if ext_lower in image_extensions:
                image_bases.add(base_name)
            elif ext_lower == '.txt':
                text_file_names.add(base_name)
    
        if not image_bases:
            return [] # No images to validate, so it's valid.

        for img_base in image_bases:
            found_match = False
            for txt_name in text_file_names:
                if img_base.lower() in txt_name.lower():
                    found_match = True
                    break
            
            if not found_match:
                images_missing_pairs.append(img_base)
        
        return images_missing_pairs

    except Exception as e:
        print(f"Error processing subdirectory '{subdir_path}': {e}")
        return ["ERROR_READING_DIRECTORY"]

def show_results_window(parent_window, validation_issues):
    """
    Creates a new Tkinter window to display the invalid directories and the
    specific files that are missing pairs.
    """
    # Ensure the parent window's state is up to date before creating a child
    parent_window.update_idletasks()

    results_window = tk.Toplevel(parent_window)
    results_window.title("Validation Results")
    
    # Set a smaller initial size and maximum size
    results_window.geometry("700x550")
    results_window.maxsize(1200, 800)
    results_window.resizable(True, True)

    main_frame = tk.Frame(results_window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    if not validation_issues:
        message = "🎉 All subdirectories are valid! 🎉\n\nEvery image file in every relevant folder has a corresponding text file."
        label = tk.Label(main_frame, text=message, justify=tk.CENTER, font=("Helvetica", 12))
        label.pack(pady=20, fill=tk.BOTH, expand=True)
        results_window.resizable(False, False)
        # We still need to wait for this simple message window to be closed
        results_window.transient(parent_window)
        results_window.grab_set()
        parent_window.wait_window(results_window)
        return

    label_text = "The following directories have missing image-text pairs:"
    label = tk.Label(main_frame, text=label_text, justify=tk.LEFT)
    label.pack(anchor='w', pady=(0, 5))

    text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=15, width=60)
    text_area.pack(fill=tk.BOTH, expand=True)
    
    # Build the detailed report string
    report_lines = []
    for directory, missing_files in sorted(validation_issues.items()):
        report_lines.append(f"Directory: {os.path.normpath(directory)}")
        for file_base in sorted(missing_files):
            report_lines.append(f"  - Missing pair for: {file_base}")
        report_lines.append("") # Add a blank line for spacing

    result_string = "\n".join(report_lines)
    text_area.insert(tk.INSERT, result_string)
    text_area.config(state=tk.DISABLED)

    def copy_to_clipboard():
        results_window.clipboard_clear()
        results_window.clipboard_append(result_string)
        messagebox.showinfo("Copied!", "The detailed report has been copied to your clipboard.", parent=results_window)

    copy_button = tk.Button(main_frame, text="Copy Report to Clipboard", command=copy_to_clipboard)
    copy_button.pack(pady=10)

    # --- FIX: Make the window modal and wait for it to be closed ---
    # This ensures the window stays on top and the script doesn't exit prematurely.
    results_window.transient(parent_window)
    results_window.grab_set()
    parent_window.wait_window(results_window)


# --- How to Run the Script ---
if __name__ == "__main__":
    validate_directory_pairs()
