import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading

# ==============================================================================
# === CONFIGURATION: Your custom translation dictionary ===
# ==============================================================================
# You can add or change any terms here. The script will find the Indonesian
# word and replace it with the English word.
translation_dict = {
    "Putih": "white",
    "Biru": "blue",
    "Merah": "red",
    "Kuning": "yellow",
    "Hijau": "green",
    "Hitam": "black",
    "Timbre": "tone",
    "Dekoratif": "decorative",
    "Tebal": "bold",
    "Cipratan": "splash",
    "Ledakan": "explosion",
    "Cahaya": "light",
    "Gelap": "dark",
    "Lembut": "soft",
    "Tajam": "sharp",
    "Suara": "sound",
    "Byur": "splash",
    "Brak": "crash",
    "Dorr": "bang",
    "Wussh": "whoosh",
    "Gubrakk": "boom",
    "Ledak": "blast",
    "Getar": "vibration",
    "Petir": "lightning",
    "Pecah": "shatter",
    "Tidak ada": "" # Special case to remove this term
    # Add more terms as needed
}

# ==============================================================================
# === UI APPLICATION CLASS ===
# ==============================================================================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Dictionary Caption Translator")
        self.root.geometry("700x500")

        # --- UI Frames ---
        frame_input = tk.Frame(root, padx=10, pady=5)
        frame_input.pack(fill=tk.X)
        frame_output = tk.Frame(root, padx=10, pady=5)
        frame_output.pack(fill=tk.X)
        frame_log = tk.Frame(root, padx=10, pady=5)
        frame_log.pack(fill=tk.BOTH, expand=True)

        # --- Input Folder Selection ---
        tk.Label(frame_input, text="Input Folder:").pack(side=tk.LEFT)
        self.input_path_var = tk.StringVar()
        entry_input = tk.Entry(frame_input, textvariable=self.input_path_var, state='readonly')
        entry_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(frame_input, text="Browse...", command=lambda: self.browse_folder(self.input_path_var)).pack(side=tk.LEFT)

        # --- Output Folder Selection ---
        tk.Label(frame_output, text="Output Folder:").pack(side=tk.LEFT)
        self.output_path_var = tk.StringVar()
        entry_output = tk.Entry(frame_output, textvariable=self.output_path_var, state='readonly')
        entry_output.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(frame_output, text="Browse...", command=lambda: self.browse_folder(self.output_path_var)).pack(side=tk.LEFT)

        # --- Log Display ---
        tk.Label(frame_log, text="Progress Log:").pack(anchor='w')
        self.log_text = scrolledtext.ScrolledText(frame_log, wrap=tk.WORD, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # --- Action Button ---
        self.btn_start = tk.Button(root, text="Start Processing", command=self.start_processing, state='disabled', padx=10, pady=10)
        self.btn_start.pack(pady=10)

    def browse_folder(self, path_variable):
        """Opens a dialog to select a folder."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            path_variable.set(folder_selected)
            self.check_paths()

    def check_paths(self):
        """Enables the start button only if both paths are selected."""
        if self.input_path_var.get() and self.output_path_var.get():
            self.btn_start.config(state='normal')

    def log_message(self, message):
        """Adds a message to the log text area."""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def start_processing(self):
        """Starts the file processing in a new thread."""
        input_folder = self.input_path_var.get()
        output_folder = self.output_path_var.get()

        if not input_folder or not output_folder:
            messagebox.showwarning("Warning", "Please select both an input and an output folder.")
            return
        
        if input_folder == output_folder:
            if not messagebox.askyesno("Warning", "Input and Output folders are the same. This will overwrite original files. Are you sure you want to continue?"):
                return

        self.btn_start.config(state='disabled')
        self.log_message("\n--- Starting Translation Process ---")
        
        thread = threading.Thread(
            target=self.processing_worker,
            args=(input_folder, output_folder),
            daemon=True
        )
        thread.start()

    def processing_worker(self, input_folder, output_folder):
        """The core logic that runs in the background thread."""
        modified_count = 0
        
        # Ensure the output directory exists
        os.makedirs(output_folder, exist_ok=True)

        for filename in os.listdir(input_folder):
            if filename.lower().endswith(".txt"):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, filename)
                
                try:
                    with open(input_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()

                    # --- Translation Logic ---
                    words = [w.strip() for w in content.split(',')]
                    translated_words = []
                    for word in words:
                        # Replace the word if it's in the dictionary, otherwise keep it
                        translated_words.append(translation_dict.get(word, word))
                    
                    # Filter out any empty strings that may result from the translation
                    final_words = [w for w in translated_words if w]
                    new_content = ', '.join(final_words)
                    # --- End Translation Logic ---

                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    self.log_message(f"Processed: {filename}")
                    modified_count += 1
                
                except Exception as e:
                    self.log_message(f"❌ ERROR processing {filename}: {e}")

        summary = f"\n--- Process Complete ---\n✅ Updated {modified_count} caption files."
        self.log_message(summary)
        self.root.after(0, lambda: self.btn_start.config(state='normal'))
        self.root.after(0, lambda: messagebox.showinfo("Success", f"Process complete!\nUpdated {modified_count} files in the output folder."))


# --- How to Run the Script ---
if __name__ == "__main__":
    main_window = tk.Tk()
    app = App(main_window)
    main_window.mainloop()
