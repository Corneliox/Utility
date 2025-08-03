import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from deep_translator import GoogleTranslator

# === Local translation dictionary (lowercase keys) ===
translation_dict = {
    "putih": "white",
    "biru": "blue",
    "biru muda": "light blue",
    "abu-abu": "gray",
    "timbre": "tone",
    "dekoratif": "decorative",
    "tebal": "bold",
    "cipratan": "splash",
    "tumpah": "spill",
    "ledakan": "explosion",
    "cahaya": "light",
    "gelap": "dark",
    "lembut": "soft",
    "tajam": "sharp",
    "suara": "sound",
    "byur": "splash",
    "brak": "crash",
    "dorr": "bang",
    "wussh": "whoosh",
    "gubrakk": "boom",
    "ledak": "blast",
    "getar": "vibration",
    "petir": "lightning",
    "pecah": "shatter",
    "air": "water",
    "splash": "splash",
}

# === Helper: Smart translate all words and cache ===
def build_translation_table(folder_path, log_func):
    unique_words = set()
    
    # Gather all unique words
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                words = f.read().lower().strip().split(',')
                unique_words.update(w.strip() for w in words if w.strip())

    translation_table = {}
    for word in sorted(unique_words):
        if word in translation_dict:
            translation_table[word] = translation_dict[word]
            log_func(f"[✔] Local: {word} → {translation_dict[word]}")
        else:
            try:
                translated = GoogleTranslator(source='auto', target='en').translate(word)
                translation_table[word] = translated
                log_func(f"[🌐] Google: {word} → {translated}")
            except Exception as e:
                translation_table[word] = word  # fallback to original
                log_func(f"[⚠️] Failed: {word} ({str(e)})")
    
    return translation_table

# === Apply translated words back into each file ===
def apply_translation(folder_path, translation_table, log_func):
    count = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            full_path = os.path.join(folder_path, filename)
            with open(full_path, 'r', encoding='utf-8') as f:
                original = f.read().strip().lower()
                words = [w.strip() for w in original.split(',')]

            new_caption = []
            for word in words:
                translated = translation_table.get(word, word)
                new_caption.append(f"{word} ({translated})")
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(', '.join(new_caption))
            
            count += 1
            log_func(f"[✏️] Updated: {filename}")
    
    return count

# === GUI ===
def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        log_text.delete(1.0, tk.END)
        log("🔍 Scanning folder...")
        table = build_translation_table(folder, log)
        log("\n🔁 Replacing captions...")
        count = apply_translation(folder, table, log)
        log(f"\n✅ Done. Updated {count} caption files.")
        messagebox.showinfo("Completed", f"Updated {count} caption files with translations.")

def log(msg):
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)
    root.update()

root = tk.Tk()
root.title("Smart Caption Translator (with Log)")
root.geometry("600x400")

tk.Label(root, text="Onomatopoeia Caption Translator", font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="Select Caption Folder", command=select_folder, font=("Arial", 12), width=30).pack(pady=10)

log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10), height=15)
log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

root.mainloop()
