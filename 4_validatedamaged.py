import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image

def check_for_damaged_images():
    """
    Main function to orchestrate the image validation process.
    """
    # --- Step 1: Check if Pillow is installed ---
    try:
        from PIL import Image
    except ImportError:
        messagebox.showerror("Dependency Missing", "Pillow library is not installed.\nPlease run: pip install Pillow")
        return

    # --- Step 2: Get Folder from User ---
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Damaged Image Checker", "Please select the folder containing your image dataset.")
    target_dir = filedialog.askdirectory(title="Select Folder to Scan for Damaged Images")
    
    if not target_dir:
        print("No folder selected. Aborting.")
        return

    print(f"Scanning folder: {target_dir}")
    print("-" * 30)

    # --- Step 3: Scan all images and check for corruption ---
    damaged_files = []
    total_checked = 0
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.webp'}

    for dirpath, _, filenames in os.walk(target_dir):
        for filename in filenames:
            _, extension = os.path.splitext(filename)
            if extension.lower() not in image_extensions:
                continue

            total_checked += 1
            file_path = os.path.join(dirpath, filename)
            try:
                # Open the image file
                with Image.open(file_path) as img:
                    # The .verify() method checks for file integrity.
                    img.verify()
                
                # Re-open after verify and try to load the pixel data.
                # This is a more thorough check.
                with Image.open(file_path) as img:
                    img.load()

                print(f"✅ OK: {os.path.relpath(file_path, target_dir)}")

            except (IOError, SyntaxError, Exception) as e:
                # If any error occurs during open, verify, or load, it's likely corrupt.
                print(f"🔴 CORRUPTED: {os.path.relpath(file_path, target_dir)} | Reason: {e}")
                damaged_files.append(file_path)

    # --- Step 4: Show the Final Report ---
    print("\n--- Scan Complete ---")
    show_results_window(target_dir, damaged_files, total_checked)


def show_results_window(target_dir, damaged_list, total_checked):
    """
    Creates a new Tkinter window to display the list of damaged files
    and offers to quarantine them.
    """
    results_window = tk.Toplevel()
    results_window.title("Image Scan Results")
    results_window.geometry("800x600")

    main_frame = tk.Frame(results_window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    summary_text = f"Scan complete. Checked {total_checked} images."
    summary_label = tk.Label(main_frame, text=summary_text, font=("Helvetica", 12))
    summary_label.pack(anchor='w', pady=(0, 10))

    if not damaged_list:
        message = "🎉 No damaged images found! 🎉"
        label = tk.Label(main_frame, text=message, justify=tk.CENTER, font=("Helvetica", 14), fg="green")
        label.pack(pady=20, fill=tk.BOTH, expand=True)
        return

    label_text = f"Found {len(damaged_list)} damaged or unreadable image(s):"
    label = tk.Label(main_frame, text=label_text, justify=tk.LEFT, fg="red")
    label.pack(anchor='w', pady=(0, 5))

    text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=15, width=60)
    text_area.pack(fill=tk.BOTH, expand=True)
    
    result_string = "\n".join([os.path.relpath(p, target_dir) for p in sorted(damaged_list)])
    text_area.insert(tk.INSERT, result_string)
    text_area.config(state=tk.DISABLED)

    def quarantine_files():
        quarantine_dir = os.path.join(target_dir, "_quarantined_images")
        try:
            os.makedirs(quarantine_dir, exist_ok=True)
            moved_count = 0
            for file_path in damaged_list:
                # Move file to the quarantine directory
                shutil.move(file_path, quarantine_dir)
                moved_count += 1
            
            messagebox.showinfo("Success", f"Successfully moved {moved_count} damaged file(s) to:\n{quarantine_dir}", parent=results_window)
            results_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Could not move files.\nError: {e}", parent=results_window)

    quarantine_button = tk.Button(main_frame, text="Move Damaged Files to Quarantine Folder", command=quarantine_files)
    quarantine_button.pack(pady=10)


# --- How to Run the Script ---
if __name__ == "__main__":
    check_for_damaged_images()
