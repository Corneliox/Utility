# 🛠️ Utility Hub & AI Dataset Toolkit

<div align="center">

![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-success?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

<p align="center">
  <b>Koleksi perkakas web interaktif siap pakai dan automasi skrip Python untuk kurasi dataset AI/LoRA, manipulasi grafis, diagram visual, serta pengukuran presisi.</b>
</p>

### 🌐 [**&rarr; Buka Live Web Portal (GitHub Pages)**](https://corneliox.github.io/Utility/)

</div>

---

## 📌 Daftar Isi
- [🌐 Utilitas Web Interaktif (Browser Native)](#-utilitas-web-interaktif-browser-native)
- [🐍 Skrip Automasi Dataset AI & Python Desktop](#-skrip-automasi-dataset-ai--python-desktop)
- [🚀 Panduan Cepat (Quick Start)](#-panduan-cepat-quick-start)
- [📁 Struktur Repositori](#-struktur-repositori)
- [⚙️ Cara Mengaktifkan GitHub Pages](#-cara-mengaktifkan-github-pages)

---

## 🌐 Utilitas Web Interaktif (Browser Native)

Semua aplikasi web di bawah ini dapat langsung dijalankan di browser tanpa perlu instalasi backend server:

| Aplikasi / Tool | Berkas Sumber | Deskripsi & Kegunaan |
| :--- | :--- | :--- |
| **Mermaid Flowchart Studio** | [`mermaid_flowchart_app.html`](mermaid_flowchart_app.html) | Editor visual interaktif diagram alir (Flowchart Mermaid) dengan live canvas pan/zoom, template preset, kustomisasi style, dan ekspor SVG/PNG. |
| **Folder Tree Visualizer** | [`folder2tree.html`](folder2tree.html) | Eksplorasi folder lokal secara interaktif via browser, seleksi file/subfolder, dan generate pohon struktur folder ke format Markdown / Plain Text. |
| **Custom Style QR Generator** | [`qrCode.html`](qrCode.html) | Generator QR Code modern dengan styling warna bebas, background transparan, modul dots/rounded, dan ekspor resolusi tinggi. |
| **Pemotong Gambar Sama Rata** | [`Crop_image_pembanding.html`](Crop_image_pembanding.html) | Membagi gambar menjadi potongan sama rata (grid) untuk perbandingan detail aset komik, perbandingan render, atau slicing dataset. |
| **Pengukur Garis Presisi (px2mm)** | [`px2mm.html`](px2mm.html) | Kalibrasi pengukuran garis presisi pada citra visual / OCT dengan rasio standar 200 px = 1 mm, multi-titik, dan pencatatan riwayat. |
| **Skala Sumbu X & Y Presisi** | [`scalepx2mm.html`](scalepx2mm.html) | Pengukuran gambar dengan panduan skala sumbu X dan Y simultan, kontrol ukuran font label, serta konversi dimensi otomatis ke milimeter. |

---

## 🐍 Skrip Automasi Dataset AI & Python Desktop

Rangkaian skrip Python untuk mempercepat persiapan, validasi integritas, dan penerjemahan dataset pelatihan kecerdasan buatan (LoRA / Stable Diffusion / LLM):

### 1. 🔍 Validasi Dataset & Pasangan Berkas
* **[`1_rawval_imgjpg_folder.py`](1_rawval_imgjpg_folder.py)**: Memindai seluruh subfolder dataset secara rekursif, memvalidasi pasangan file gambar (`.jpg`, `.png`, `.webp`) dengan berkas anotasi `.txt`, mendeteksi anomali, dan menyimpan laporan detail.
* **[`3_img_txt_validate.py`](3_img_txt_validate.py)**: Memastikan setiap gambar memiliki pasangan file caption teks yang sesuai.
* **[`4_validatedamaged.py`](4_validatedamaged.py)**: Membuka dan memverifikasi integritas bitstream berkas citra untuk memastikan tidak ada gambar rusak (*corrupt file header*).

### 2. 🔤 NLP & Pembersihan Caption (Indonesian &rarr; English)
* **[`6_caption_bhs_to_eng.py`](6_caption_bhs_to_eng.py)**:
  * Memperbaiki saltik (*typo correction*) otomatis pada kosakata bahasa Indonesia.
  * Melindungi kata onomatope dan efek suara komik (`gluduk`, `tok tok tok`, `byur`, dll.).
  * Menerjemahkan caption dataset ke bahasa Inggris secara batch dengan live GUI log.

### 3. 🖼️ Penskalaan & Normalisasi Gambar
* **[`5_Upscalermin256.py`](5_Upscalermin256.py)**: Memindai dan melakukan *upscale / padding* pada gambar yang berada di bawah dimensi minimum (256&times;256 px) dengan interpolasi Lanczos berkualitas tinggi.
* **[`5_1_Upscalermin256RGBA.py`](5_1_Upscalermin256RGBA.py)**: Versi dengan penanganan khusus kanal transparansi (RGBA/alpha channel).

### 4. 🗂️ Utilitas Berkas & Sistem
* **[`folder2tree.py`](folder2tree.py)**: Generator representasi struktur direktori di terminal ke format teks.
* **[`mergetxt_file.py`](mergetxt_file.py)** & **[`2_extractmergefile.py`](2_extractmergefile.py)**: Penggabungan dan ekstraksi batch file teks anotasi.
* **[`library_scanner_app.py`](library_scanner_app.py)**: GUI desktop untuk menginspeksi paket-paket Python yang terpasang pada environment kerja.

---

## 🚀 Panduan Cepat (Quick Start)

### Menjalankan Web Portal Lokal
Cukup buka berkas **[`index.html`](index.html)** di browser modern (Chrome, Edge, Firefox, Safari) atau gunakan server lokal:
```bash
# Menggunakan Python built-in HTTP server
python -m http.server 8000
```
Buka browser di `http://localhost:8000`.

### Menjalankan Skrip Python
1. **Pastikan Python 3.8+ terpasang:**
   ```bash
   python --version
   ```
2. **Pasang dependensi yang dibutuhkan:**
   ```bash
   pip install Pillow deep-translator
   ```
3. **Jalankan skrip yang diinginkan:**
   ```bash
   python 1_rawval_imgjpg_folder.py
   python 6_caption_bhs_to_eng.py
   python 5_Upscalermin256.py
   ```

---

## 📁 Struktur Repositori

```text
Utility/
├── .github/
│   └── workflows/
│       └── deploy.yml           # 🤖 GitHub Actions CI/CD Auto-Deploy Pages
├── scripts/
│   └── generate_catalog.py      # ⚙️ Scanner & Generator tools.json Otomatis
├── data/ (or root)
│   └── tools.json               # 📊 Manifest Data Katalog Utilitas
├── index.html                   # 🌐 Web Portal Dashboard (GitHub Pages Entry)
├── Crop_image_pembanding.html   # ✂️ Pemotong Gambar Slicing / Grid
├── folder2tree.html             # 🌳 Web Folder Tree Visualizer
├── mermaid_flowchart_app.html   # 📊 Mermaid Flowchart Studio
├── px2mm.html                   # 📏 Pengukur Garis Presisi OCT
├── qrCode.html                  # 📱 Custom Style QR Generator
├── scalepx2mm.html              # 📐 Skala Sumbu X & Y Presisi
│
├── 1_rawval_imgjpg_folder.py    # 🔍 Validator Pasangan Dataset Gambar-Teks
├── 2_extractmergefile.py        # 📦 Ekstraksi & Penggabungan Berkas
├── 3_img_txt_validate.py        # 📝 Pemeriksa Kelengkapan Anotasi
├── 4_validatedamaged.py         # ⚠️ Detektor Berkas Gambar Corrupt
├── 5_Upscalermin256.py          # 🖼️ Image Upscaler Minimum 256px
├── 5_1_Upscalermin256RGBA.py    # 🖼️ Image Upscaler dengan Alpha RGBA
├── 6_caption_bhs_to_eng.py      # 🌐 Typo Fixer & Translator Caption Dataset
├── folder2tree.py               # 🌲 CLI Folder Tree Generator
├── library_scanner_app.py       # 📦 GUI Scanner Dependensi Python
├── mergetxt_file.py             # 📄 Batch Text Merger
└── README.md                    # 📖 Dokumentasi Repositori
```

---

## 🤖 Sistem Auto-Cataloging (CI/CD GitHub Actions)

Repositori ini dilengkapi sistem **Auto-Discovery & Auto-Cataloging**:
Setiap kali Anda melakukan `git push` berkas `.html` atau `.py` baru ke branch `main`, GitHub Actions akan:
1. Menjalankan `scripts/generate_catalog.py`.
2. Memindai berkas baru, mengekstrak metadata, dan memperbarui `tools.json`.
3. Mendeploy versi terbaru secara otomatis ke GitHub Pages.

### Menambahkan Header Metadata pada File Baru (Opsional):
Agar informasi tool baru tampil sempurna di website, Anda cukup menyisipkan komentar di awal file:

* **Pada skrip Python (`.py`):**
  ```python
  """
  @title: Nama Tool Anda
  @category: AI & Dataset Prep
  @desc: Deskripsi singkat kegunaan tool ini.
  @deps: Pillow, deep-translator
  @icon: terminal
  """
  ```

* **Pada aplikasi Web (`.html`):**
  ```html
  <!-- @title: Nama Web App | @category: Web Interactive | @desc: Deskripsi aplikasi | @icon: globe -->
  ```

*(Jika tidak menyertakan komentar di atas, sistem tetap akan mendeteksi dan mengkategorikan tool baru secara cerdas via fallback parsing).*

---

## ⚙️ Cara Mengaktifkan GitHub Pages

1. Masuk ke repositori Anda di GitHub (`Corneliox/Utility`).
2. Buka tab **Settings** &rarr; menu **Pages** di bilah kiri.
3. Pada bagian **Build and deployment** &rarr; **Source**:
   * Pilih **GitHub Actions** (alur kerja `.github/workflows/deploy.yml` akan menangani build & deploy otomatis).
4. Website Anda akan aktif di: **`https://corneliox.github.io/Utility/`**

---

<div align="center">
  <sub>Dikembangkan oleh <b><a href="https://github.com/Corneliox">Corneliox</a></b> &bull; Terbuka untuk kontribusi dan kolaborasi.</sub>
</div>
