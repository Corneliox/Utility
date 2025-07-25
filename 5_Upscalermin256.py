import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image

# --- Configuration ---
# You can change this value. Any image with a width or height
# smaller than this will be flagged for upscaling. 256 is a safe minimum.
MIN_DIMENSION = 256

def check_images():
    """
    Main function to orchestrate the image validation and upscaling process.
    """
    # --- Step 1: Check if Pillow is installed ---
    try:
        from PIL import Image
    except ImportError:
        messagebox.showerror("Dependency Missing", "Pillow library is not installed.\nPlease run: pip install Pillow")
        return

    # --- Step 2: Get Folder from User ---
    # Create the main application window but keep it hidden
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Image Validator & Upscaler", "Please select the folder containing your image dataset.")
    target_dir = filedialog.askdirectory(title="Select Folder to Scan for Images")
    
    if not target_dir:
        print("No folder selected. Aborting.")
        root.destroy()
        return

    print(f"Scanning folder: {target_dir}")
    print(f"Flagging images smaller than {MIN_DIMENSION}x{MIN_DIMENSION} pixels for upscaling.")
    print("-" * 30)

    # --- Step 3: Scan all images for issues ---
    damaged_files = []
    undersized_files = []
    total_checked = 0
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.webp'}

    for dirpath, _, filenames in os.walk(target_dir):
        for filename in filenames:
            _, extension = os.path.splitext(filename)
            if extension.lower() not in image_extensions:
                continue

            total_checked += 1
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, target_dir)
            
            try:
                with Image.open(file_path) as img:
                    img.verify()
                
                with Image.open(file_path) as img:
                    img.load()
                    
                    if img.width < MIN_DIMENSION or img.height < MIN_DIMENSION:
                        print(f"🟡 UNDERSIZED: {relative_path} ({img.width}x{img.height})")
                        undersized_files.append(file_path)
                    else:
                        print(f"✅ OK: {relative_path}")

            except (IOError, SyntaxError, Exception) as e:
                print(f"🔴 CORRUPTED: {relative_path} | Reason: {e}")
                damaged_files.append(file_path)

    # --- Step 4: Show the Final Report ---
    print("\n--- Scan Complete ---")
    # We pass the root window to the results function to manage the app's lifecycle
    show_results_window(root, target_dir, damaged_files, undersized_files, total_checked)

    # Start the Tkinter event loop. The script will pause here until the root window is destroyed.
    root.mainloop()


def show_results_window(root_window, target_dir, damaged_list, undersized_list, total_checked):
    """
    Creates a new Tkinter window to display the list of problematic files
    and offers to quarantine or upscale them.
    """
    results_window = tk.Toplevel(root_window)
    results_window.title("Image Scan Results")
    results_window.geometry("800x600")

    # This function will be called when the user closes the window with the 'X' button
    def on_closing():
        root_window.destroy()

    results_window.protocol("WM_DELETE_WINDOW", on_closing)

    main_frame = tk.Frame(results_window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    summary_text = f"Scan complete. Checked {total_checked} images."
    summary_label = tk.Label(main_frame, text=summary_text, font=("Helvetica", 12))
    summary_label.pack(anchor='w', pady=(0, 10))

    if not damaged_list and not undersized_list:
        message = "🎉 No issues found! 🎉\n\nAll images are valid and meet the minimum size requirement."
        label = tk.Label(main_frame, text=message, justify=tk.CENTER, font=("Helvetica", 14), fg="green")
        label.pack(pady=20, fill=tk.BOTH, expand=True)
        return

    # --- Display Damaged Files ---
    if damaged_list:
        label_text = f"Found {len(damaged_list)} damaged or unreadable image(s):"
        label = tk.Label(main_frame, text=label_text, justify=tk.LEFT, fg="red", font=("Helvetica", 10, "bold"))
        label.pack(anchor='w', pady=(10, 2))
        text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=8)
        text_area.pack(fill=tk.BOTH, expand=True)
        result_string = "\n".join([os.path.relpath(p, target_dir) for p in sorted(damaged_list)])
        text_area.insert(tk.INSERT, result_string)
        text_area.config(state=tk.DISABLED)
        
        quarantine_button = tk.Button(main_frame, text="Quarantine Damaged Files", command=lambda: quarantine_files(target_dir, damaged_list, root_window))
        quarantine_button.pack(pady=(5, 10))

    # --- Display Undersized Files ---
    if undersized_list:
        label_text = f"Found {len(undersized_list)} images smaller than {MIN_DIMENSION}x{MIN_DIMENSION} to upscale:"
        label = tk.Label(main_frame, text=label_text, justify=tk.LEFT, fg="orange", font=("Helvetica", 10, "bold"))
        label.pack(anchor='w', pady=(10, 2))
        text_area_undersized = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=8)
        text_area_undersized.pack(fill=tk.BOTH, expand=True)
        result_string_undersized = "\n".join([os.path.relpath(p, target_dir) for p in sorted(undersized_list)])
        text_area_undersized.insert(tk.INSERT, result_string_undersized)
        text_area_undersized.config(state=tk.DISABLED)

        upscale_button = tk.Button(main_frame, text="Upscale Undersized Images", command=lambda: upscale_images(undersized_list, root_window))
        upscale_button.pack(pady=(5, 10))

def quarantine_files(target_dir, damaged_list, root_window):
    quarantine_dir = os.path.join(target_dir, "_quarantined_images")
    try:
        os.makedirs(quarantine_dir, exist_ok=True)
        moved_count = 0
        for file_path in damaged_list:
            if os.path.exists(file_path):
                shutil.move(file_path, quarantine_dir)
                moved_count += 1
        
        messagebox.showinfo("Success", f"Successfully moved {moved_count} damaged file(s) to:\n{quarantine_dir}")
        root_window.destroy() # Close the entire application

    except Exception as e:
        messagebox.showerror("Error", f"Could not move files.\nError: {e}")

def upscale_images(undersized_list, root_window):
    """
    Upscales a list of images to meet the MIN_DIMENSION while preserving aspect ratio.
    """
    print("\n--- Starting Upscale Process ---")
    upscaled_count = 0
    error_count = 0
    
    for file_path in undersized_list:
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                
                if width < MIN_DIMENSION or height < MIN_DIMENSION:
                    if width < height:
                        new_width = MIN_DIMENSION
                        new_height = int(height * (MIN_DIMENSION / width))
                    else:
                        new_height = MIN_DIMENSION
                        new_width = int(width * (MIN_DIMENSION / height))
                    
                    print(f"Upscaling '{os.path.basename(file_path)}' from {width}x{height} to {new_width}x{new_height}...")
                    
                    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    img_resized.save(file_path)
                    upscaled_count += 1
        
        except Exception as e:
            print(f"❌ ERROR: Could not upscale '{os.path.basename(file_path)}'. Reason: {e}")
            error_count += 1
            
    summary_message = f"Upscale process complete!\n\nSuccessfully upscaled: {upscaled_count} images."
    if error_count > 0:
        summary_message += f"\nFailed to upscale: {error_count} images (see console for details)."
        
    messagebox.showinfo("Upscale Complete", summary_message)
    root_window.destroy() # Close the entire application


# --- How to Run the Script ---
if __name__ == "__main__":
    check_images()
