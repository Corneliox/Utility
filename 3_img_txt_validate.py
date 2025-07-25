import os
import tkinter as tk
from tkinter import filedialog, messagebox

def validate_and_fix_dataset_pairs():
    """
    Scans a directory to find image-text pairs where the image name is contained
    within the text file name. Offers to rename the text files for a perfect match.
    """
    # --- Step 1: Get Target Folder from User ---
    
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Dataset Validator & Fixer", "Please select the folder containing your dataset.")
    target_dir = filedialog.askdirectory(title="Select Dataset Folder to Validate and Fix")
    
    if not target_dir:
        print("No folder selected. Aborting.")
        return

    print(f"Processing folder: {target_dir}")
    print("-" * 30)

    # --- Step 2: Scan Files and Separate by Type ---

    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.webp'}
    image_files = {}  # dict: {base_name: extension}
    text_files = {}   # dict: {base_name: extension}

    try:
        for filename in os.listdir(target_dir):
            base_name, extension = os.path.splitext(filename)
            ext_lower = extension.lower()
            if ext_lower in image_extensions:
                image_files[base_name] = extension
            elif ext_lower == '.txt':
                text_files[base_name] = extension
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while scanning the folder: {e}")
        return

    # --- Step 3: Find Correlated Pairs ---

    matches_to_rename = [] # List of tuples: (image_base, text_base)
    perfect_matches = set()
    unmatched_images = list(image_files.keys())
    unmatched_texts = list(text_files.keys())

    for img_base in list(unmatched_images):
        # Check for perfect match first
        if img_base in unmatched_texts:
            perfect_matches.add(img_base)
            unmatched_images.remove(img_base)
            unmatched_texts.remove(img_base)
            continue

        # Check for loose match (image name contained in text name)
        found_loose_match = False
        for txt_base in list(unmatched_texts):
            if img_base.lower() in txt_base.lower():
                matches_to_rename.append((img_base, txt_base))
                unmatched_images.remove(img_base)
                unmatched_texts.remove(txt_base)
                found_loose_match = True
                break # Move to next image once a match is found
    
    # --- Step 4: Generate and Display the Report ---

    report_lines = ["--- Validation Report ---"]
    report_lines.append(f"\n✅ Found {len(perfect_matches)} perfect pairs (e.g., Image1.jpg & Image1.txt).")
    
    if matches_to_rename:
        report_lines.append(f"\n✨ Found {len(matches_to_rename)} correlated pairs to fix:")
        for img, txt in matches_to_rename:
            report_lines.append(f"  - Image: '{img}'  ->  Text: '{txt}.txt'")
    
    if unmatched_images:
        report_lines.append(f"\n🔴 WARNING: {len(unmatched_images)} IMAGES MISSING ANY TEXT FILE:")
        for base_name in sorted(unmatched_images):
            report_lines.append(f"  - {base_name}")
    
    if unmatched_texts:
        report_lines.append(f"\n🟡 WARNING: {len(unmatched_texts)} TEXT FILES MISSING ANY IMAGE:")
        for base_name in sorted(unmatched_texts):
            report_lines.append(f"  - {base_name}")

    final_report = "\n".join(report_lines)
    print(final_report)
    messagebox.showinfo("Validation Complete", final_report)

    # --- Step 5: Ask User to Perform Renaming ---

    if not matches_to_rename:
        print("\nNo files to rename. All pairs are perfect or have issues.")
        return

    proceed_with_rename = messagebox.askyesno(
        "Fix Filenames?",
        f"Do you want to automatically rename the {len(matches_to_rename)} correlated text files to match their images?"
    )

    if not proceed_with_rename:
        print("\nUser chose not to rename files. Exiting.")
        return

    # --- Step 6: Perform Renaming ---
    
    renamed_count = 0
    rename_errors = []
    print("\n--- Renaming Files ---")

    for img_base, txt_base in matches_to_rename:
        try:
            old_txt_ext = text_files[txt_base]
            old_path = os.path.join(target_dir, f"{txt_base}{old_txt_ext}")
            
            # New name will be based on the image's base name
            new_path = os.path.join(target_dir, f"{img_base}{old_txt_ext}")

            if os.path.exists(new_path):
                error_msg = f"Skipped: '{old_path}' because '{new_path}' already exists."
                rename_errors.append(error_msg)
                print(f"⚠️  {error_msg}")
                continue

            os.rename(old_path, new_path)
            print(f"✅ Renamed '{txt_base}{old_txt_ext}' -> '{img_base}{old_txt_ext}'")
            renamed_count += 1
        except Exception as e:
            error_msg = f"Failed to rename '{txt_base}': {e}"
            rename_errors.append(error_msg)
            print(f"❌ {error_msg}")

    # --- Step 7: Final Renaming Summary ---
    
    summary_message = f"Renaming Complete!\n\nSuccessfully renamed: {renamed_count} files."
    if rename_errors:
        summary_message += f"\n\nErrors encountered: {len(rename_errors)}\n(See console for details)"
    
    messagebox.showinfo("Rename Summary", summary_message)
    print("\n--- Renaming Process Finished ---")


# --- How to Run the Script ---
if __name__ == "__main__":
    validate_and_fix_dataset_pairs()
