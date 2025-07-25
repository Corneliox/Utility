import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def merge_dataset_files():
    """
    Scans a selected source directory recursively, finds all .png and .txt files,
    and copies them into a single selected destination directory.
    """
    # --- Step 1: Get Source and Destination Folders from User ---
    
    # Hide the root tkinter window
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Dataset Merger", "First, please select the SOURCE folder that contains your dataset (e.g., 'Images/').")
    source_dir = filedialog.askdirectory(title="Select the Source Dataset Folder")
    
    if not source_dir:
        print("No source folder selected. Aborting.")
        return

    messagebox.showinfo("Dataset Merger", "Next, please select the DESTINATION folder where you want to save the merged files.")
    dest_dir = filedialog.askdirectory(title="Select the Destination Folder for Merged Files")

    if not dest_dir:
        print("No destination folder selected. Aborting.")
        return
        
    print(f"Source Folder: {source_dir}")
    print(f"Destination Folder: {dest_dir}")
    print("-" * 30)

    # --- Step 2: Scan and Copy Files ---
    
    copied_files_count = 0
    skipped_files_count = 0

    try:
        # os.walk recursively goes through all directories and subdirectories
        for dirpath, _, filenames in os.walk(source_dir):
            for filename in filenames:
                # Check if the file is a .png or .txt file
                if filename.lower().endswith(('.png', '.txt')):
                    
                    # Construct the full path of the source file
                    source_path = os.path.join(dirpath, filename)
                    
                    # Construct the destination path
                    dest_path = os.path.join(dest_dir, filename)

                    # To avoid overwriting files with the same name from different folders,
                    # we can add a check or rename them. For this simple case, we'll just copy.
                    # Be aware that if 'image.png' exists in two subfolders, one will be overwritten.
                    
                    print(f"Copying '{filename}'...")
                    shutil.copy2(source_path, dest_path) # copy2 preserves metadata
                    copied_files_count += 1
                else:
                    skipped_files_count += 1
                    
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred during the process: {e}")
        return

    # --- Step 3: Show Final Report ---
    
    summary_message = (
        f"Process Complete!\n\n"
        f"Files copied: {copied_files_count}\n"
        f"Files skipped (not .png or .txt): {skipped_files_count}\n\n"
        f"All files have been merged into:\n{dest_dir}"
    )
    
    print("-" * 30)
    print("Process Complete!")
    print(f"Total files copied: {copied_files_count}")
    print(f"Total files skipped: {skipped_files_count}")
    
    messagebox.showinfo("Success", summary_message)


# --- How to Run the Script ---
if __name__ == "__main__":
    # This will start the process when you run the Python file.
    merge_dataset_files()
