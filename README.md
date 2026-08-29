# 🛠️ Utility Hub & AI Dataset Toolkit

<div align="center">

![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-success?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![i18n](https://img.shields.io/badge/i18n-EN%20%7C%20ID%20%7C%20ZH--TW-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

<p align="center">
  <b>A curated collection of ready-to-use interactive browser web tools and high-performance Python automation scripts for AI/LoRA dataset curation, visual diagramming, graphic manipulation, and precision measurement.</b>
</p>

### 🌐 [**&rarr; Open Live Web Portal (GitHub Pages)**](https://corneliox.github.io/Utility/)

</div>

---

## 📌 Table of Contents
- [✨ Key Features](#-key-features)
- [🌐 Interactive Web Utilities (Browser-Native)](#-interactive-web-utilities-browser-native)
- [🐍 Python AI Dataset & Desktop Pipelines](#-python-ai-dataset--desktop-pipelines)
- [🚀 Quick Start Guide](#-quick-start-guide)
- [📁 Repository Structure](#-repository-structure)
- [🤖 Auto-Cataloging CI/CD System](#-auto-cataloging-cicd-system)
- [⚙️ Enabling GitHub Pages](#️-enabling-github-pages)
- [📄 License & Attribution](#-license--attribution)

---

## ✨ Key Features

- **🌐 Unified Web Portal Dashboard ([`index.html`](index.html)):** Browse and launch all web tools seamlessly inside an in-page modal iframe or open them in a new tab.
- **🌍 Multilingual Support (i18n):** Instant switching between **English (Default)**, **Bahasa Indonesia (ID)**, and **Traditional Chinese (繁體中文 / ZH-TW)**.
- **🎨 Dual Aesthetic Themes:** Deep Cyber Dark Mode & Crisp Oceanic **Coral Blue Light Mode** with persistent `localStorage` preference.
- **🌌 Interactive JS Effects:** Real-time mouse-tracking particle mesh background, 3D perspective card tilt with specular glare, dynamic headline typewriter, and confetti celebration particle bursts.
- **🤖 Automated GitHub Actions Cataloging:** Automatically scans new `.html` and `.py` files on every `git push`, extracts metadata, generates `tools.json`, and deploys updates to GitHub Pages.

---

## 🌐 Interactive Web Utilities (Browser-Native)

All web applications below run 100% client-side inside modern web browsers without requiring backend servers or database setup:

| Application | Source File | Description & Capabilities |
| :--- | :--- | :--- |
| **Mermaid Flowchart Studio** | [`mermaid_flowchart_app.html`](mermaid_flowchart_app.html) | Advanced visual flowchart diagram editor powered by Mermaid.js with interactive canvas pan/zoom, preset templates, custom styling palettes, and high-resolution SVG/PNG export. |
| **Folder Tree Visualizer** | [`folder2tree.html`](folder2tree.html) | Interactive browser-based local folder explorer. Select specific files/subdirectories and generate formatted directory trees in Markdown or Plain Text. |
| **Custom Style QR Generator** | [`qrCode.html`](qrCode.html) | Modern QR code designer with custom hex color palettes, transparent background toggles, rounded/dot corner modules, center logos, and high-res download. |
| **Equal Aspect Image Splitter** | [`Crop_image_pembanding.html`](Crop_image_pembanding.html) | Splits single or multiple images into equal grid tiles for side-by-side comparison, comic panels, render validation, or AI dataset slicing. |
| **Precision Line Measure (px2mm)** | [`px2mm.html`](px2mm.html) | Optical/OCT calibrated distance measuring tool using standardized ratio (200 px = 1 mm), multi-point coordinate markers, and history logging. |
| **2D Scale Axis Ruler** | [`scalepx2mm.html`](scalepx2mm.html) | Image dimension measurement with simultaneous X and Y coordinate guides, customizable font sizing, and automated millimeter conversions. |

---

## 🐍 Python AI Dataset & Desktop Pipelines

High-throughput Python automation scripts engineered for dataset preparation, integrity audits, image normalization, and NLP caption cleaning (LoRA / Stable Diffusion / LLM):

### 1. 🔍 Dataset Integrity & Pair Validation
* **[`1_rawval_imgjpg_folder.py`](1_rawval_imgjpg_folder.py)**: Recursively traverses dataset directory trees, verifies that every image (`.jpg`, `.png`, `.webp`) has a corresponding annotation file (`.txt`), isolates anomalies, and produces detailed scan reports.
* **[`3_img_txt_validate.py`](3_img_txt_validate.py)**: Checks pair completeness and detects orphaned image or text annotation files.
* **[`4_validatedamaged.py`](4_validatedamaged.py)**: Inspects image bitstream integrity with Pillow to catch corrupt image headers and unreadable files before launching compute-intensive AI model training.

### 2. 🔤 NLP Caption Translation & Cleaning (ID &rarr; EN)
* **[`6_caption_bhs_to_eng.py`](6_caption_bhs_to_eng.py)**:
  * Automatically corrects Indonesian typographical errors with a built-in dictionary.
  * Preserves comic onomatopoeia and sound-effect tags (`gluduk`, `tok tok tok`, `byur`, etc.).
  * Batch translates captions into English with real-time GUI logging.

### 3. 🖼️ Image Normalization & Aspect-Ratio Resizing
* **[`5_Upscalermin256.py`](5_Upscalermin256.py)**: Scans directories and upscales/pads images below minimum dimensions (256&times;256 px) using high-fidelity Lanczos resampling.
* **[`5_1_Upscalermin256RGBA.py`](5_1_Upscalermin256RGBA.py)**: Extended version with dedicated alpha transparency channel handling (RGBA).

### 4. 🗂️ File & Workspace Utilities
* **[`folder2tree.py`](folder2tree.py)**: CLI utility to render clean terminal tree representations of directory hierarchies.
* **[`mergetxt_file.py`](mergetxt_file.py)** & **[`2_extractmergefile.py`](2_extractmergefile.py)**: Batch consolidator and extractor for distributed text annotation files.
* **[`library_scanner_app.py`](library_scanner_app.py)**: Desktop GUI to audit installed Python packages, detect version discrepancies, and export environment manifests.

---

## 🚀 Quick Start Guide

### Running the Web Portal Locally
Simply open **[`index.html`](index.html)** in any modern web browser (Chrome, Edge, Firefox, Safari) or run a local HTTP server:
```bash
# Using Python's built-in HTTP server
python -m http.server 8000
```
Then visit `http://localhost:8000` in your browser.

### Executing Python Scripts
1. **Ensure Python 3.8+ is installed:**
   ```bash
   python --version
   ```
2. **Install required dependencies:**
   ```bash
   pip install Pillow deep-translator
   ```
3. **Execute desired scripts:**
   ```bash
   python 1_rawval_imgjpg_folder.py
   python 6_caption_bhs_to_eng.py
   python 5_Upscalermin256.py
   ```

---

## 📁 Repository Structure

```text
Utility/
├── .github/
│   └── workflows/
│       └── deploy.yml           # 🤖 GitHub Actions CI/CD Auto-Deploy Pages
├── scripts/
│   └── generate_catalog.py      # ⚙️ Scanner & Manifest Generator
├── data/ (or root)
│   └── tools.json               # 📊 Dynamic Utility Catalog Manifest
├── index.html                   # 🌐 Web Portal Dashboard (GitHub Pages Entry)
├── Crop_image_pembanding.html   # ✂️ Equal Aspect Image Grid Splitter
├── folder2tree.html             # 🌳 Web Folder Tree Visualizer
├── mermaid_flowchart_app.html   # 📊 Mermaid Flowchart Studio
├── px2mm.html                   # 📏 Precision Line Measure (px2mm)
├── qrCode.html                  # 📱 Custom Style QR Generator
├── scalepx2mm.html              # 📐 2D Scale Axis Ruler
│
├── 1_rawval_imgjpg_folder.py    # 🔍 Dataset Folder & Pair Validator
├── 2_extractmergefile.py        # 📦 Dataset File Extractor & Merger
├── 3_img_txt_validate.py        # 📝 Annotation Completeness Check
├── 4_validatedamaged.py         # ⚠️ Corrupt Image Header Scanner
├── 5_Upscalermin256.py          # 🖼️ Minimum Dimension Image Upscaler
├── 5_1_Upscalermin256RGBA.py    # 🖼️ Image Upscaler with RGBA Alpha Channel
├── 6_caption_bhs_to_eng.py      # 🌐 Typo Fixer & Caption Translator (ID -> EN)
├── folder2tree.py               # 🌲 CLI Folder Tree Generator
├── library_scanner_app.py       # 📦 Desktop Python Environment Inspector
├── mergetxt_file.py             # 📄 Batch Text Merger
└── README.md                    # 📖 Project Documentation
```

---

## 🤖 Auto-Cataloging CI/CD System

This repository includes a native **Auto-Discovery & Auto-Cataloging** pipeline:
Every time you `git push` a new `.html` or `.py` file to the `main` branch, GitHub Actions will:
1. Run `scripts/generate_catalog.py`.
2. Scan new tools, parse metadata tags, and update `tools.json`.
3. Deploy the updated portal automatically to GitHub Pages.

### Adding Header Metadata to New Files (Optional):
To ensure your new tool renders with custom titles, categories, and icons, simply add a header comment block at the top of your file:

* **For Python Scripts (`.py`):**
  ```python
  """
  @title: Your Tool Name
  @category: AI & Dataset Prep
  @desc: Brief description of what this tool accomplishes.
  @deps: Pillow, deep-translator
  @icon: terminal
  """
  ```

* **For Web Applications (`.html`):**
  ```html
  <!-- @title: Web App Name | @category: Web Interactive | @desc: Description | @icon: globe -->
  ```

*(If omitted, the scanner utilizes intelligent regex fallbacks to parse `<title>` tags and module docstrings automatically).*

---

## ⚙️ Enabling GitHub Pages

1. Open your repository on GitHub (`Corneliox/Utility`).
2. Go to **Settings** &rarr; **Pages** in the left sidebar.
3. Under **Build and deployment** &rarr; **Source**:
   * Select **`GitHub Actions`** (the `.github/workflows/deploy.yml` workflow will automatically handle building and publishing).
4. Your website will be live and automatically kept up to date at: **`https://corneliox.github.io/Utility/`**

---

## 📄 License & Attribution

Distributed under the **MIT License**. See `LICENSE` for more information.

<div align="center">
  <sub>Engineered with passion by <b><a href="https://github.com/Corneliox">Corneliox</a></b> &bull; Open for contributions and feature requests.</sub>
</div>
