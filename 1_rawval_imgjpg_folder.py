import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

def validate_directory_pairs():
    """
    Main function to orchestrate the validation process. It browses for a root
    directory, recursively finds all subdirectories containing dataset files,
    validates them, and saves a detailed report to a .txt file.
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
    validation_issues = {} # Dictionary to store {directory: [list_of_error_messages]}
    valid_dirs = []      # List to store valid directory paths
    
    for dirpath, _, filenames in os.walk(root_dir):
        has_dataset_files = any(f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp', '.txt')) for f in filenames)

        if has_dataset_files:
            relative_path = os.path.relpath(dirpath, root_dir)
            print(f"Checking: {relative_path}...")
            
            error_messages = check_pairs_in_subdirectory(dirpath)
            if error_messages:
                # If the list of errors is not empty, the directory is invalid
                validation_issues[relative_path] = error_messages
                print(f"🔴 Invalid: Directory '{relative_path}' has issues.")
            else:
                valid_dirs.append(relative_path)
                print(f"✅ Valid: Directory '{relative_path}' is OK.")

    # --- Step 3: Generate the Report and Save to a File ---
    print("\n--- Validation Scan Complete ---")
    generate_report_file(root_dir, validation_issues, valid_dirs)

def check_pairs_in_subdirectory(subdir_path):
    """
    Validates a single subdirectory based on strict pairing rules.

    Args:
        subdir_path (str): The full path to the subdirectory to check.

    Returns:
        list: A list of strings describing validation errors. 
              Returns an empty list if the directory is valid.
    """
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.webp'}
    image_bases = set()
    text_file_names = set()
    error_messages = []

    try:
        for filename in os.listdir(subdir_path):
            base_name, extension = os.path.splitext(filename)
            ext_lower = extension.lower()

            if ext_lower in image_extensions:
                image_bases.add(base_name)
            elif ext_lower == '.txt':
                text_file_names.add(base_name)
        
        # --- NEW VALIDATION LOGIC ---
        
        # Case 1: Only images, no text files at all.
        if image_bases and not text_file_names:
            error_messages.append("Contains image files but is missing all .txt files.")
            return error_messages

        # Case 2: Only text files, no images at all.
        if text_file_names and not image_bases:
            error_messages.append("Contains .txt files but is missing all image files.")
            return error_messages

        # Case 3: No images to validate (e.g., folder with only other file types)
        if not image_bases:
            return [] # Valid

        # Case 4: Mismatched pairs (both types exist, but some images lack a caption)
        for img_base in image_bases:
            found_match = False
            for txt_name in text_file_names:
                if img_base.lower() in txt_name.lower():
                    found_match = True
                    break
            
            if not found_match:
                error_messages.append(f"  - Missing pair for image: {img_base}")
        
        return error_messages

    except Exception as e:
        print(f"Error processing subdirectory '{subdir_path}': {e}")
        return [f"ERROR reading directory: {e}"]

def generate_report_file(root_dir, validation_issues, valid_dirs):
    """
    Builds the report string and saves it to a user-specified .txt file.
    """
    report_lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Build the Report String ---
    report_lines.append("--- Dataset Validation Report ---")
    report_lines.append(f"Generated on: {timestamp}")
    report_lines.append(f"Root Directory: {os.path.normpath(root_dir)}")
    report_lines.append("\n" + "="*40)
    report_lines.append("🔴 INVALID DIRECTORIES (Issues Found)")
    report_lines.append("="*40)

    if not validation_issues:
        report_lines.append("\n🎉 No invalid directories found! All pairs are valid.\n")
    else:
        for directory, error_list in sorted(validation_issues.items()):
            report_lines.append(f"\nDirectory: {os.path.normpath(directory)}")
            for error in sorted(error_list):
                report_lines.append(f"  - {error}")
    
    report_lines.append("\n" + "="*40)
    report_lines.append("✅ VALID DIRECTORIES")
    report_lines.append("="*40 + "\n")

    if not valid_dirs:
        report_lines.append("No valid directories found.")
    else:
        for directory in sorted(valid_dirs):
            report_lines.append(f"- {os.path.normpath(directory)}")

    final_report = "\n".join(report_lines)

    # --- Ask User Where to Save the File ---
    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Save Validation Report As",
        initialfile="validation_report.txt"
    )

    if not save_path:
        print("\nSave cancelled by user. Report not saved.")
        messagebox.showinfo("Report Not Saved", "You cancelled saving the report file. The results are available in the console.")
        return

    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(final_report)
        print(f"\nReport successfully saved to: {save_path}")
        messagebox.showinfo("Success", f"Report successfully saved to:\n{save_path}")
    except Exception as e:
        print(f"\nError saving report file: {e}")
        messagebox.showerror("Save Error", f"Could not save the report file.\nError: {e}")


# --- How to Run the Script ---
if __name__ == "__main__":
    validate_directory_pairs()
