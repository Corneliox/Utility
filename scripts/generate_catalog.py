#!/usr/bin/env python3
"""
Catalog Generator for Utility Hub
Scans all .html and .py tools in the repository and generates `tools.json`.
Supports header metadata tags (@title, @category, @desc, @deps, @tags, @icon).
"""

import os
import re
import json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_JSON = os.path.join(REPO_ROOT, "tools.json")

IGNORE_FILES = {"index.html"}
IGNORE_DIRS = {".git", ".github", "scripts", "__pycache__", "node_modules", "dist", "build"}

DEFAULT_METADATA = {
    # HTML Tools Defaults
    "mermaid_flowchart_app.html": {
        "title": "Mermaid Flowchart Studio",
        "category": "Diagram & Studio",
        "desc": "Editor visual canggih untuk diagram alir (Flowchart Mermaid) dengan live canvas pan/zoom, template preset, ekspor SVG/PNG, dan kustomisasi style.",
        "icon": "git-fork",
        "tags": ["mermaid", "flowchart", "diagram", "visual", "docs", "web"]
    },
    "folder2tree.html": {
        "title": "Folder Tree Browser & Generator",
        "category": "File & Directory",
        "desc": "Eksplorasi folder lokal secara interaktif via browser, seleksi berkas tertentu, dan generate pohon struktur folder ke format Markdown / Plain Text.",
        "icon": "folder-tree",
        "tags": ["folder", "tree", "directory", "generator", "text", "docs", "web"]
    },
    "qrCode.html": {
        "title": "Custom Style QR Generator",
        "category": "Design & Utility",
        "desc": "Generator QR Code modern dengan styling warna bebas, opsi background transparan, pemilihan bentuk modul (dots/rounded), dan ekspor resolusi tinggi.",
        "icon": "qr-code",
        "tags": ["qr", "code", "generator", "custom", "style", "image", "web"]
    },
    "Crop_image_pembanding.html": {
        "title": "Pemotong Gambar Sama Rata",
        "category": "Image Processing",
        "desc": "Membagi satu atau beberapa gambar menjadi potongan sama rata (grid) untuk perbandingan detail, aset komik, atau kurasi dataset AI.",
        "icon": "crop",
        "tags": ["crop", "image", "slice", "splitter", "perbandingan", "visual", "web"]
    },
    "px2mm.html": {
        "title": "Pengukur Garis Presisi (px2mm)",
        "category": "Optical & Measurement",
        "desc": "Kalibrasi pengukuran garis presisi pada citra visual (OCT) dengan rasio standar 200 px = 1 mm, pengukuran multi-titik, dan pencatatan riwayat.",
        "icon": "ruler",
        "tags": ["px2mm", "measure", "measurement", "oct", "distance", "ruler", "optical", "web"]
    },
    "scalepx2mm.html": {
        "title": "Skala Sumbu X & Y Presisi",
        "category": "Optical & Measurement",
        "desc": "Pengukuran gambar dengan panduan skala sumbu X dan Y simultan, kontrol ukuran font label, serta penghitungan dimensi otomatis dalam milimeter.",
        "icon": "maximize",
        "tags": ["scalepx2mm", "measure", "measurement", "scale", "xy", "font", "ruler", "web"]
    },

    # Python Tools Defaults
    "1_rawval_imgjpg_folder.py": {
        "title": "Dataset Folder & Pair Validator",
        "category": "AI & Dataset Prep",
        "desc": "Memindai seluruh subfolder dataset secara rekursif, memvalidasi pasangan file gambar (.jpg, .png, .webp) dengan berkas anotasi .txt, dan membuat laporan scan.",
        "deps": "Pillow (opsional)",
        "command": "python 1_rawval_imgjpg_folder.py",
        "icon": "check-circle-2",
        "tags": ["dataset", "validator", "pairs", "raw", "image", "text", "ai", "lora", "python"]
    },
    "2_extractmergefile.py": {
        "title": "Dataset File Extractor & Merger",
        "category": "File & Text Tool",
        "desc": "Skrip automasi untuk mengekstrak dan menggabungkan kumpulan berkas dataset dari berbagai subfolder.",
        "deps": "-",
        "command": "python 2_extractmergefile.py",
        "icon": "archive",
        "tags": ["extract", "merge", "dataset", "files", "python"]
    },
    "3_img_txt_validate.py": {
        "title": "Image-Text Pair Completeness Check",
        "category": "AI & Dataset Prep",
        "desc": "Memvalidasi kelengkapan berkas gambar dan berkas teks pendamping agar tidak ada gambar tanpa anotasi atau teks tanpa gambar.",
        "deps": "-",
        "command": "python 3_img_txt_validate.py",
        "icon": "file-check",
        "tags": ["validate", "image", "text", "caption", "pairs", "dataset", "python"]
    },
    "4_validatedamaged.py": {
        "title": "Corrupt Image Detector & Anomaly Scanner",
        "category": "AI & Dataset Prep",
        "desc": "Membuka dan memverifikasi integritas bitstream berkas citra untuk memastikan tidak ada gambar rusak atau header corrupt.",
        "deps": "Pillow",
        "command": "python 4_validatedamaged.py",
        "icon": "alert-triangle",
        "tags": ["damaged", "image", "validator", "corrupt", "file", "check", "dataset", "python"]
    },
    "5_Upscalermin256.py": {
        "title": "Aspect-Ratio Aware Image Upscaler",
        "category": "Image Processing",
        "desc": "Memindai dan melakukan upscale pada gambar yang dimensinya di bawah 256x256 px dengan filter Lanczos berkualitas tinggi.",
        "deps": "Pillow",
        "command": "python 5_Upscalermin256.py",
        "icon": "image-plus",
        "tags": ["upscaler", "image", "resize", "pillow", "min", "dimension", "lora", "ai", "dataset", "python"]
    },
    "5_1_Upscalermin256RGBA.py": {
        "title": "Image Upscaler with Alpha Channel (RGBA)",
        "category": "Image Processing",
        "desc": "Penskalaan gambar beresolusi minimal 256x256 px dengan penanganan khusus kanal transparansi RGBA.",
        "deps": "Pillow",
        "command": "python 5_1_Upscalermin256RGBA.py",
        "icon": "layers",
        "tags": ["upscaler", "rgba", "transparent", "image", "pillow", "python"]
    },
    "6_caption_bhs_to_eng.py": {
        "title": "Dataset Caption Typo Fixer & Translator",
        "category": "NLP & Translation",
        "desc": "Koreksi otomatis saltik (typo), perlindungan tag onomatope/efek suara komik, dan penerjemahan batch caption dataset ke Bahasa Inggris.",
        "deps": "deep-translator",
        "command": "python 6_caption_bhs_to_eng.py",
        "icon": "languages",
        "tags": ["caption", "translate", "indonesian", "english", "typo", "fix", "ai", "lora", "dataset", "python"]
    },
    "folder2tree.py": {
        "title": "CLI Directory Tree Generator",
        "category": "File & Text Tool",
        "desc": "Menghasilkan representasi visual struktur folder ke terminal atau file teks markdown secara cepat.",
        "deps": "-",
        "command": "python folder2tree.py",
        "icon": "folder-git",
        "tags": ["tree", "folder", "cli", "markdown", "python"]
    },
    "library_scanner_app.py": {
        "title": "Python Environment & Library Scanner",
        "category": "Developer Tool",
        "desc": "Aplikasi GUI desktop untuk memindai paket-paket Python yang terpasang dan mengekspor daftar dependensi lingkungan kerja.",
        "deps": "-",
        "command": "python library_scanner_app.py",
        "icon": "cpu",
        "tags": ["library", "scanner", "dependencies", "environment", "inspector", "python"]
    },
    "mergetxt_file.py": {
        "title": "Batch Text Merger Utility",
        "category": "File & Text Tool",
        "desc": "Menggabungkan banyak berkas teks (.txt) dari satu direktori menjadi satu berkas terkonsolidasi.",
        "deps": "-",
        "command": "python mergetxt_file.py",
        "icon": "files",
        "tags": ["merge", "text", "files", "batch", "python"]
    }
}


def parse_metadata_from_content(filename, content):
    """Parses @title, @category, @desc, @deps, @tags from file content."""
    meta = {}

    # Extract tags format @key: value or @key value
    title_match = re.search(r"@title\s*:\s*([^\r\n*]+)", content, re.IGNORECASE)
    if title_match:
        meta["title"] = title_match.group(1).strip()

    category_match = re.search(r"@category\s*:\s*([^\r\n*]+)", content, re.IGNORECASE)
    if category_match:
        meta["category"] = category_match.group(1).strip()

    desc_match = re.search(r"@desc(?:ription)?\s*:\s*([^\r\n*]+)", content, re.IGNORECASE)
    if desc_match:
        meta["desc"] = desc_match.group(1).strip()

    deps_match = re.search(r"@deps?\s*:\s*([^\r\n*]+)", content, re.IGNORECASE)
    if deps_match:
        meta["deps"] = deps_match.group(1).strip()

    tags_match = re.search(r"@tags?\s*:\s*([^\r\n*]+)", content, re.IGNORECASE)
    if tags_match:
        tags = [t.strip().lower() for t in re.split(r"[, ]+", tags_match.group(1)) if t.strip()]
        meta["tags"] = tags

    icon_match = re.search(r"@icon\s*:\s*([^\r\n*]+)", content, re.IGNORECASE)
    if icon_match:
        meta["icon"] = icon_match.group(1).strip()

    return meta


def process_html_file(filepath, filename):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

    # Defaults
    data = DEFAULT_METADATA.get(filename, {}).copy()

    # Parse in-file header
    extracted = parse_metadata_from_content(filename, content)
    data.update(extracted)

    # Fallbacks if still missing
    if "title" not in data:
        # Check <title> tag
        title_tag = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
        if title_tag:
            data["title"] = title_tag.group(1).strip()
        else:
            data["title"] = filename.replace(".html", "").replace("_", " ").title()

    if "category" not in data:
        data["category"] = "Web Interactive"

    if "desc" not in data:
        meta_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        if meta_desc:
            data["desc"] = meta_desc.group(1).strip()
        else:
            data["desc"] = f"Aplikasi web interaktif {data['title']} siap pakai di browser."

    if "icon" not in data:
        data["icon"] = "globe"

    if "tags" not in data:
        data["tags"] = [word.lower() for word in re.split(r"[_ -]+", filename.replace(".html", "")) if len(word) > 1]
        data["tags"].extend(["web", "interactive"])

    data["filename"] = filename
    data["type"] = "web"
    data["url"] = filename

    return data


def process_py_file(filepath, filename):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

    # Defaults
    data = DEFAULT_METADATA.get(filename, {}).copy()

    # Parse in-file header
    extracted = parse_metadata_from_content(filename, content)
    data.update(extracted)

    # Fallbacks
    if "title" not in data:
        # Check first docstring
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if docstring_match:
            first_line = docstring_match.group(1).strip().split("\n")[0]
            if len(first_line) > 3 and len(first_line) < 80:
                data["title"] = first_line
        if "title" not in data:
            data["title"] = filename.replace(".py", "").replace("_", " ").title()

    if "category" not in data:
        if "img" in filename.lower() or "upscale" in filename.lower():
            data["category"] = "Image Processing"
        elif "val" in filename.lower() or "dataset" in filename.lower():
            data["category"] = "AI & Dataset Prep"
        elif "caption" in filename.lower() or "translate" in filename.lower():
            data["category"] = "NLP & Translation"
        else:
            data["category"] = "Python Utility"

    if "desc" not in data:
        data["desc"] = f"Skrip Python automasi {data['title']} untuk pemrosesan file lokal."

    if "deps" not in data:
        deps = []
        if "PIL" in content or "Pillow" in content:
            deps.append("Pillow")
        if "deep_translator" in content:
            deps.append("deep-translator")
        data["deps"] = ", ".join(deps) if deps else "-"

    if "command" not in data:
        data["command"] = f"python {filename}"

    if "icon" not in data:
        data["icon"] = "terminal"

    if "tags" not in data:
        data["tags"] = [word.lower() for word in re.split(r"[_ -]+", filename.replace(".py", "")) if len(word) > 1]
        data["tags"].extend(["python", "script", "automation"])

    data["filename"] = filename
    data["type"] = "python"

    return data


def scan_tools():
    tools = []
    
    for root, dirs, files in os.walk(REPO_ROOT):
        # Remove ignored directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
        
        for file in sorted(files):
            if file in IGNORE_FILES:
                continue

            rel_path = os.path.relpath(os.path.join(root, file), REPO_ROOT).replace("\\", "/")

            if file.endswith(".html"):
                item = process_html_file(os.path.join(root, file), rel_path)
                if item:
                    tools.append(item)
            elif file.endswith(".py"):
                item = process_py_file(os.path.join(root, file), rel_path)
                if item:
                    tools.append(item)

    return tools


def main():
    print(f"Scanning tools in {REPO_ROOT}...")
    tools = scan_tools()
    
    output_data = {
        "version": "2.0.0",
        "generated_at": None,
        "total_tools": len(tools),
        "web_count": sum(1 for t in tools if t["type"] == "web"),
        "python_count": sum(1 for t in tools if t["type"] == "python"),
        "tools": tools
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Successfully cataloged {len(tools)} tools ({output_data['web_count']} Web, {output_data['python_count']} Python).")
    print(f"Saved to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
