# 🗂️ FileOrganizer Pro

An **intelligent, content-aware file organization automation tool** built in Python.
Automatically classifies files by type, moves them into structured folders, stores
everything in a SQLite database, and provides a full-featured web dashboard.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 Smart Classification | Detects category by extension, MIME type, and content |
| 📁 Folder Hierarchy | Auto-creates category folders: Images, Videos, Code, Documents, etc. |
| 🗄️ SQLite Database | Full schema: files, history, stats, settings |
| 👁️ Auto-Watcher | Background thread monitors folders and organizes new files in real-time |
| 🔍 Duplicate Detection | MD5 checksum comparison; configurable rename/skip/overwrite strategy |
| 📊 Dashboard | Live stats, category breakdown, activity timeline |
| 🌐 Web UI | 7 pages: Home, Dashboard, Organize, Files, History, About, Contact |
| ⚙️ REST API | JSON endpoints for upload, preview, stats, settings, history |

---

## 📦 Project Structure

```
FileOrganizerPro/
├── app.py                          # Application factory & entry point
├── requirements.txt
├── modules/
│   ├── __init__.py
│   ├── classifier.py               # Content-aware file classification
│   ├── organizer.py                # Core organization engine
│   ├── database.py                 # SQLite schema & CRUD helpers
│   ├── routes.py                   # All Flask routes & REST API
│   └── watcher.py                  # Background folder watcher
├── templates/
│   ├── __init__.py
│   └── html_templates.py           # All 7 HTML pages
├── database/
│   └── organizer.db                # Auto-created SQLite database
├── uploads_demo/                   # Temporary upload staging area
└── organized/                      # Final organized output
    ├── Images/
    ├── Videos/
    ├── Audio/
    ├── Documents/
    ├── Spreadsheets/
    ├── Code/
    ├── Archives/
    └── ...
```

---

## 🚀 Quick Start

```bash
# 1. Install dependency (only Flask required)
pip install flask

# 2. Run
python app.py

# 3. Open browser
open http://localhost:5000
```

---

## 🌐 Pages & Routes

| URL | Page |
|---|---|
| `/` | Home — hero, features, stats |
| `/dashboard` | Live analytics & recent activity |
| `/organize` | Drag-and-drop file upload & organization |
| `/files` | Filterable file library |
| `/history` | Full audit trail with search |
| `/about` | Project overview & module docs |
| `/contact` | Contact form |

## 🔌 REST API

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/upload` | Upload & organize files |
| `POST` | `/api/preview` | Preview classification without uploading |
| `GET`  | `/api/stats` | Dashboard statistics |
| `GET`  | `/api/history` | History log (JSON) |
| `GET`  | `/api/folder-tree` | Organized folder structure |
| `GET/POST` | `/api/settings` | Read/write user settings |
| `POST` | `/api/contact` | Contact form submission |

---

## 📂 Supported Categories (14)

Images · Videos · Audio · Documents · Spreadsheets · Presentations ·
Archives · Code · Executables · Fonts · Databases · Ebooks · Others

---

## 🧩 Module Details

### `modules/classifier.py`
- `classify_file(path)` — full metadata from filesystem
- `classify_by_name(filename)` — metadata from filename only (no I/O)
- `compute_checksum(path)` — MD5 for duplicate detection
- `format_file_size(bytes)` — human-readable size

### `modules/organizer.py`
- `organize_file(src, root, db, strategy, duplicate)` — single file
- `organize_folder(src, root, db, ...)` — batch folder processing
- `preview_organization(filenames)` — preview without filesystem changes
- `get_folder_tree(root)` — nested dict of organized output

### `modules/database.py`
- Schema: `files`, `history`, `stats`, `settings`
- `insert_file()`, `update_file_organized()`, `insert_history()`
- `get_all_files()`, `get_all_history()`, `get_dashboard_stats()`
- `get_setting()`, `set_setting()`

### `modules/watcher.py`
- `FolderWatcher` class — polling-based, threaded
- `start_watcher(folder, root, db)` — singleton instance
- `stop_watcher()` — graceful shutdown

---

## License
MIT
