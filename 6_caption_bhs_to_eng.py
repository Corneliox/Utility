import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import queue
import asyncio

# --- Dependency Checker ---
# This tool requires two external libraries: googletrans and langdetect.
# We will check if they are installed and guide the user if they are not.
try:
    from googletrans import Translator
    from langdetect import detect, LangDetectException
except ImportError:
    messagebox.showerror(
        "Dependencies Missing",
        "This tool requires 'googletrans' and 'langdetect'.\n\nPlease install them by running this command in your terminal or command prompt:\n\npip install googletrans==4.0.0-rc1 langdetect"
    )
    exit()

# --- Main Application Class ---
class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caption Translator (Bahasa -> English)")
        self.root.geometry("700x500")

        self.translator = Translator()
        self.log_queue = queue.Queue()

        # --- UI Elements ---
        # Folder Selection Frame
        frame_folder = tk.Frame(root, padx=10, pady=10)
        frame_folder.pack(fill=tk.X)

        tk.Label(frame_folder, text="Dataset Folder:").pack(side=tk.LEFT)
        self.folder_path_var = tk.StringVar()
        entry_folder = tk.Entry(frame_folder, textvariable=self.folder_path_var, state='readonly')
        entry_folder.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        btn_browse = tk.Button(frame_folder, text="Browse...", command=self.browse_folder)
        btn_browse.pack(side=tk.LEFT)

        # Log Display Frame
        frame_log = tk.Frame(root, padx=10, pady=5)
        frame_log.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame_log, text="Progress Log:").pack(anchor='w')
        self.log_text = scrolledtext.ScrolledText(frame_log, wrap=tk.WORD, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Action Button
        self.btn_start = tk.Button(root, text="Start Translation", command=self.start_translation, state='disabled', padx=10, pady=10)
        self.btn_start.pack(pady=10)
        
        # Start the queue processor to update the log from the thread
        self.process_log_queue()

    def browse_folder(self):
        """Opens a dialog to select a folder and enables the start button."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path_var.set(folder_selected)
            self.btn_start.config(state='normal')
            self.log_message(f"Selected folder: {folder_selected}")

    def log_message(self, message):
        """Adds a message to the log text area in a thread-safe way."""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END) # Auto-scroll

    def process_log_queue(self):
        """Checks the queue for new log messages and displays them."""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_message(message)
        except queue.Empty:
            pass
        self.root.after(100, self.process_log_queue)

    def start_translation(self):
        """Starts the translation process in a new thread to avoid freezing the UI."""
        folder_path = self.folder_path_var.get()
        if not folder_path:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return

        self.btn_start.config(state='disabled')
        self.log_queue.put("\n--- Starting Translation Process ---")
        
        # Run the heavy work in a separate thread
        translation_thread = threading.Thread(
            target=self.translation_worker, 
            args=(folder_path,),
            daemon=True
        )
        translation_thread.start()

    def translation_worker(self, folder_path):
        """The actual translation logic that runs in the background."""
        # NEW: List of onomatopoeia words to exclude from translation (case-insensitive)
        exclusion_list = {'byur', 'duuttt', 'gluduk', 'gong', 'thing', 'tok'}
        
        total_files = 0
        changed_files = 0

        for dirpath, _, filenames in os.walk(folder_path):
            for filename in filenames:
                if filename.lower().endswith('.txt'):
                    total_files += 1
                    file_path = os.path.join(dirpath, filename)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            original_content = f.read()

                        parts = [p.strip() for p in original_content.split(',')]
                        translated_parts = []
                        made_change = False

                        for part in parts:
                            if not part: # Skip empty parts
                                continue
                            
                            # NEW: Check if the part is in the exclusion list
                            if part.lower() in exclusion_list:
                                translated_parts.append(part)
                                continue # Skip to the next part

                            try:
                                # Detect language. If it's Indonesian, translate it.
                                if detect(part) == 'id':
                                    # FIX: Use asyncio to run the async translate function correctly
                                    loop = asyncio.new_event_loop()
                                    asyncio.set_event_loop(loop)
                                    result = loop.run_until_complete(
                                        self.translator.translate(part, src='id', dest='en')
                                    )
                                    translated_text = result.text
                                    loop.close()

                                    translated_parts.append(translated_text)
                                    self.log_queue.put(f"  - In '{filename}', translated '{part}' -> '{translated_text}'")
                                    made_change = True
                                else:
                                    # If not Indonesian, keep the original part
                                    translated_parts.append(part)
                            except LangDetectException:
                                # If language detection fails (e.g., for short terms), keep it.
                                translated_parts.append(part)
                            except Exception as e:
                                # Handle potential translation API errors
                                self.log_queue.put(f"  - WARNING: Could not process '{part}'. Error: {e}")
                                translated_parts.append(part)

                        if made_change:
                            changed_files += 1
                            new_content = ", ".join(translated_parts)
                            # Overwrite the original file with the new content
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            self.log_queue.put(f"✅ Updated '{filename}'")

                    except Exception as e:
                        self.log_queue.put(f"❌ ERROR: Could not process file '{filename}'. Reason: {e}")
        
        # --- Final Report ---
        summary = (
            f"\n--- Process Complete ---\n"
            f"Scanned: {total_files} .txt files.\n"
            f"Modified: {changed_files} files.\n"
        )
        self.log_queue.put(summary)
        # Re-enable the button on the main thread
        self.root.after(0, lambda: self.btn_start.config(state='normal'))


# --- How to Run the Script ---
if __name__ == "__main__":
    main_window = tk.Tk()
    app = TranslatorApp(main_window)
    main_window.mainloop()
