import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from deep_translator import GoogleTranslator

# === Typo Fixes ===
typo_corrections = {
    "abu-bau": "abu-abu", "aspa": "asap", "bauu": "bau", "emas'": "emas",
    "hitqm": "hitam", "kejut": "kejutan", "kjning": "kuning",
    "miiring": "miring", "mirirng": "miring", "onomatopeia": "onomatopoeia",
    "onomatopoiea": "onomatopoeia", "oren": "oranye", "san-serif": "sans-serif",
    "titik-titik": "titik-titik", "duuutt": "duuttt", "duuuttt": "duuttt"
}
protected_sounds = {
    "byur", "dut", "duut", "duuttt", "gluduk", "gluduk gluduk",
    "gonggg", "thing", "tok", "tok tok tok"
}
manual_translation = {
    "putih": "white", "biru": "blue", "biru muda": "light blue", "abu-abu": "gray",
    "timbre": "tone", "dekoratif": "decorative", "tebal": "bold", "cipratan": "splash",
    "tumpah": "spill", "ledakan": "explosion", "cahaya": "light", "gelap": "dark",
    "lembut": "soft", "tajam": "sharp", "suara": "sound", "asap": "smoke", "bau": "smell",
    "emas": "gold", "hitam": "black", "kejutan": "shock", "kuning": "yellow",
    "miring": "slanted", "onomatopoeia": "onomatopoeia", "oranye": "orange",
    "sans-serif": "sans-serif", "titik-titik": "dots", "air": "water", "splash": "splash",
    "duuttt": "smelly fart sound", "gluduk": "thunderous noise",
    "gluduk gluduk": "repeated falling noise", "gonggg": "gong hit sound",
    "thing": "metallic hit", "tok": "knock", "tok tok tok": "repeated knock"
}

def log(msg):
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)
    root.update()

def correct_and_translate(words):
    translation_table = {}
    for word in sorted(set(words)):
        original = word.lower().strip()
        corrected = typo_corrections.get(original, original)

        if corrected in protected_sounds:
            translation_table[word] = corrected
            log(f"[🔒] Protected: {corrected} kept as-is")
        elif corrected in manual_translation:
            translation_table[word] = manual_translation[corrected]
            log(f"[✔] Manual: {corrected} → {manual_translation[corrected]}")
        else:
            try:
                translation = GoogleTranslator(source='auto', target='en').translate(corrected)
                translation_table[word] = translation
                log(f"[🌐] Google: {corrected} → {translation}")
            except Exception as e:
                translation_table[word] = corrected
                log(f"[⚠️] Error on {corrected}: {e}")
    return translation_table

def scan_words(folder):
    unique_words = set()
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                line = f.read().strip().lower()
                unique_words.update([w.strip() for w in line.split(",")])
    return unique_words

def apply_translation(folder, table):
    count = 0
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                content = f.read().strip().lower()
            words = [w.strip() for w in content.split(",")]
            new_caption = [f"{w} ({table.get(w, w)})" for w in words]
            with open(os.path.join(folder, file), "w", encoding="utf-8") as f:
                f.write(", ".join(new_caption))
            log(f"[✏️] Updated: {file}")
            count += 1
    return count

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        log_text.delete("1.0", tk.END)
        log("🔍 Scanning words in folder...")
        words = scan_words(folder)
        table = correct_and_translate(words)
        log("\n🔁 Replacing in caption files...")
        count = apply_translation(folder, table)
        log(f"\n✅ Done! {count} files updated.")
        messagebox.showinfo("Complete", f"Translated {count} caption files.")

# === GUI ===
root = tk.Tk()
root.title("Smart Caption Translator (Fix Typo + Translate)")
root.geometry("700x450")

tk.Label(root, text="Onomatopoeia Caption Fixer & Translator", font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="Select Caption Folder", command=select_folder, font=("Arial", 12)).pack(pady=10)

log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10), height=20)
log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

root.mainloop()
