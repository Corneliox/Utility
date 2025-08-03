import os
import tkinter as tk
from tkinter import filedialog, messagebox

# === Translation dictionary ===
translation_dict = {
    "Putih": "white",
    "Biru": "blue",
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
    # Add more as needed
}

def translate_caption(text):
    words = [w.strip() for w in text.split(',')]
    translated = []
    for word in words:
        if word in translation_dict:
            translated.append(f"{word} ({translation_dict[word]})")
        else:
            translated.append(word)
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

# === Create window ===
root = tk.Tk()
root.title("Onomatopoeia Caption Translator")
root.geometry("400x200")

title_label = tk.Label(root, text="Translate Caption Tags to English", font=("Arial", 14))
title_label.pack(pady=20)

select_button = tk.Button(root, text="Select Caption Folder", command=select_folder, font=("Arial", 12), width=25)
select_button.pack(pady=10)

root.mainloop()
