import os
import tkinter as tk
from tkinter import filedialog, messagebox

def validate_dataset_pairs():
    """
    Scans a selected directory to ensure every image file has a corresponding
    .txt file with the same base name.
    """
    # --- Step 1: Get Target Folder from User ---
    
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Dataset Validator", "Please select the folder containing your final dataset (the merged images and text files).")
    target_dir = filedialog.askdirectory(title="Select Dataset Folder to Validate")
    
    if not target_dir:
        print("No folder selected. Aborting.")
        return

    print(f"Validating folder: {target_dir}")
    print("-" * 30)

    # --- Step 2: Scan Files and Separate by Type ---

    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.webp'}
    image_files = set()
    text_files = set()

    try:
        for filename in os.listdir(target_dir):
            # Get the filename without extension (the base name)
            base_name, extension = os.path.splitext(filename)
            extension = extension.lower()

            if extension in image_extensions:
                image_files.add(base_name)
            elif extension == '.txt':
                text_files.add(base_name)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while scanning the folder: {e}")
        return

    # --- Step 3: Compare Sets and Find Mismatches ---

    # Files that have both an image and a text file
    matching_pairs = image_files.intersection(text_files)
    
    # Images that are missing a .txt file
    images_missing_text = image_files.difference(text_files)
    
    # .txt files that are missing an image
    text_missing_images = text_files.difference(image_files)

    # --- Step 4: Generate and Display the Report ---

    report_lines = [
        "--- Validation Report ---",
        f"\nTotal Valid Pairs (Image + Text): {len(matching_pairs)}",
        f"Total Image Files: {len(image_files)}",
        f"Total Text Files: {len(text_files)}",
    ]

    print("\n--- Validation Report ---")
    print(f"Total Valid Pairs (Image + Text): {len(matching_pairs)}")
    print(f"Total Image Files: {len(image_files)}")
    print(f"Total Text Files: {len(text_files)}")


    if images_missing_text:
        report_lines.append(f"\n🔴 WARNING: {len(images_missing_text)} IMAGES MISSING .TXT FILES:")
        print(f"\n🔴 WARNING: {len(images_missing_text)} IMAGES MISSING .TXT FILES:")
        for base_name in sorted(list(images_missing_text)):
            report_lines.append(f"  - {base_name}")
            print(f"  - {base_name}")
    
    if text_missing_images:
        report_lines.append(f"\n🟡 WARNING: {len(text_missing_images)} .TXT FILES MISSING IMAGES:")
        print(f"\n🟡 WARNING: {len(text_missing_images)} .TXT FILES MISSING IMAGES:")
        for base_name in sorted(list(text_missing_images)):
            report_lines.append(f"  - {base_name}")
            print(f"  - {base_name}")

    if not images_missing_text and not text_missing_images:
        success_message = "✅ Success! All images have a corresponding .txt file."
        report_lines.append("\n" + success_message)
        print("\n" + success_message)

    final_report = "\n".join(report_lines)
    
    # Displaying the report in a message box. 
    # For very long reports, checking the console is better.
    messagebox.showinfo("Validation Complete", final_report)


# --- How to Run the Script ---
if __name__ == "__main__":
    validate_dataset_pairs()
