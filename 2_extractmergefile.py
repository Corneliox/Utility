import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def merge_dataset_files():
    """
    Scans a selected source directory recursively, finds all .png and .txt files,
    and copies them into a single selected destination directory. It also reports
    on any files that were skipped during the process.
    """
    # --- Step 1: Get Source and Destination Folders from User ---
    
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
    skipped_files_details = [] # List to store details of skipped files

    try:
        # os.walk recursively goes through all directories and subdirectories
        for dirpath, _, filenames in os.walk(source_dir):
            for filename in filenames:
                source_path = os.path.join(dirpath, filename)
                
                # Check if the file is a .png or .txt file
                if filename.lower().endswith(('.png', '.txt')):
                    
                    dest_path = os.path.join(dest_dir, filename)
                    
                    print(f"Copying '{filename}'...")
                    shutil.copy2(source_path, dest_path) # copy2 preserves metadata
                    copied_files_count += 1
                else:
                    # This file is not a .png or .txt, so we record it as skipped
                    relative_path = os.path.relpath(source_path, source_dir)
                    skipped_files_details.append(relative_path)
                    
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred during the process: {e}")
        return

    # --- Step 3: Show Final Report ---
    
    print("-" * 30)
    print("Process Complete!")
    print(f"Total files copied: {copied_files_count}")
    print(f"Total files skipped: {len(skipped_files_details)}")

    summary_lines = [
        f"Process Complete!\n",
        f"Files copied: {copied_files_count}",
        f"Files skipped: {len(skipped_files_details)}"
    ]

    # If any files were skipped, list them in the report
    if skipped_files_details:
        print("\n--- Skipped Files (not .png or .txt) ---")
        summary_lines.append("\n\nSkipped Files:")
        
        # Add skipped files to console output and the final message box
        for i, file_path in enumerate(sorted(skipped_files_details)):
            print(f"  - {file_path}")
            # Limit lines in the messagebox to avoid making it too big
            if i < 15: 
                summary_lines.append(f"  - {file_path}")
        
        if len(skipped_files_details) > 15:
            summary_lines.append("  - ... (and more, see console for full list)")

    final_summary = "\n".join(summary_lines)
    messagebox.showinfo("Merge Complete", final_summary)


# --- How to Run the Script ---
if __name__ == "__main__":
    # This will start the process when you run the Python file.
    merge_dataset_files()
