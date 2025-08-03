import os
import tkinter as tk
from tkinter import filedialog, messagebox
from deep_translator import GoogleTranslator

# === Translation dictionary (lowercase) ===
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
    "splash": "splash"  # already English
}

def translate_caption(text):
    words = [w.strip().lower() for w in text.split(',')]
    translated = []
    for word in words:
        if word in translation_dict:
            translated.append(f"{word} ({translation_dict[word]})")
        else:
            try:
                # Fallback to Google Translate if not in dictionary
                english = GoogleTranslator(source='auto', target='en').translate(word)
                translated.append(f"{word} ({english})")
            except:
                translated.append(word)  # Fallback if API fails
    return ', '.join(translated)

def process_folder(folder_path):
    modified = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            full_path = os.path.join(folder_path, filename)
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            new_content = translate_caption(content)

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            modified += 1
    return modified

# === GUI Application ===
def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        count = process_folder(folder)
        messagebox.showinfo("Success", f"{count} caption files translated and updated.")

root = tk.Tk()
root.title("Onomatopoeia Caption Translator (with Auto-Translate)")
root.geometry("420x200")

tk.Label(root, text="Auto Translate Onomatopoeia Tags", font=("Arial", 14)).pack(pady=20)
tk.Button(root, text="Select Caption Folder", command=select_folder, font=("Arial", 12), width=30).pack(pady=10)

root.mainloop()
