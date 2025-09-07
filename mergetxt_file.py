import os
import tkinter as tk
from tkinter import filedialog, messagebox

def merge_txt_files():
    # Select folder with .txt files
    source_folder = filedialog.askdirectory(title="Select Folder with .txt files")
    if not source_folder:
        return
    
    # Select output folder
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        return
    
    folder_name = os.path.basename(source_folder.rstrip("/\\"))
    output_file = os.path.join(output_folder, f"merge{folder_name}.txt")
    
    # Get all .txt files in source folder
    txt_files = [f for f in os.listdir(source_folder) if f.lower().endswith(".txt")]
    if not txt_files:
        messagebox.showerror("Error", "No .txt files found in the selected folder.")
        return
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        for txt_file in txt_files:
            file_path = os.path.join(source_folder, txt_file)
            outfile.write(f"---- {txt_file} ----\n")
            with open(file_path, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
            outfile.write("\n\n")  # Add space between files
    
    messagebox.showinfo("Success", f"Merged file created:\n{output_file}")

# Setup basic UI
root = tk.Tk()
root.title("Merge TXT Files")
root.geometry("300x100")

tk.Label(root, text="Click the button to merge TXT files").pack(pady=10)
tk.Button(root, text="Merge TXT Files", command=merge_txt_files).pack()

root.mainloop()
