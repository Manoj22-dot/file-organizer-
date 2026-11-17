"""
modules/classifier.py
Content-based file classification engine.
Detects category by extension, MIME type, and (optionally) file content.
"""

import os
import mimetypes
import hashlib

# ── Category map ──────────────────────────────────────────────────────────────
CATEGORY_MAP = {
    # Code (before Documents so .py/.js etc. match here, not Documents)
    "Code": {
        "extensions": [".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".htm",
                        ".css", ".scss", ".sass", ".less", ".java", ".c", ".cpp",
                        ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".kt",
                        ".sh", ".bash", ".zsh", ".ps1", ".r", ".m", ".sql",
                        ".json", ".xml", ".yaml", ".yml", ".toml", ".ini",
                        ".cfg", ".conf", ".env", ".dockerfile", ".ipynb"],
        "mime_keywords": ["text/x-", "application/json", "application/xml",
                          "application/javascript"],
        "icon": "💻",
        "color": "#14b8a6"
    },
    # Spreadsheets (before Documents)
    "Spreadsheets": {
        "extensions": [".xlsx", ".xls", ".ods", ".csv", ".tsv", ".numbers"],
        "mime_keywords": ["spreadsheet", "excel", "csv"],
        "icon": "📊",
        "color": "#10b981"
    },
    # Presentations (before Documents)
    "Presentations": {
        "extensions": [".pptx", ".ppt", ".odp", ".key"],
        "mime_keywords": ["presentation", "powerpoint"],
        "icon": "📑",
        "color": "#f97316"
    },
    # Images
    "Images": {
        "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
                        ".webp", ".svg", ".ico", ".heic", ".heif", ".raw", ".cr2",
                        ".nef", ".arw", ".psd", ".ai", ".eps"],
        "mime_prefix": "image/",
        "icon": "🖼️",
        "color": "#f59e0b"
    },
    # Videos
    "Videos": {
        "extensions": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
                        ".m4v", ".3gp", ".ogv", ".ts", ".mts", ".m2ts"],
        "mime_prefix": "video/",
        "icon": "🎬",
        "color": "#8b5cf6"
    },
    # Audio
    "Audio": {
        "extensions": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",
                        ".opus", ".aiff", ".mid", ".midi"],
        "mime_prefix": "audio/",
        "icon": "🎵",
        "color": "#ec4899"
    },
    # Documents
    "Documents": {
        "extensions": [".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt", ".md",
                        ".tex", ".pages", ".wpd", ".wps"],
        "mime_keywords": ["pdf", "word", "document", "text"],
        "icon": "📄",
        "color": "#3b82f6"
    },
    # E-books (before Archives so .epub doesn't hit zip mime)
    "Ebooks": {
        "extensions": [".epub", ".mobi", ".azw", ".azw3", ".fb2", ".lit"],
        "mime_keywords": ["epub", "mobi"],
        "icon": "📚",
        "color": "#84cc16"
    },
    # Databases (before Executables so .db doesn't hit octet-stream)
    "Databases": {
        "extensions": [".db", ".sqlite", ".sqlite3", ".mdb", ".accdb", ".dump"],
        "mime_keywords": ["database", "sqlite"],
        "icon": "🗄️",
        "color": "#0ea5e9"
    },
    # Archives
    "Archives": {
        "extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
                        ".tar.gz", ".tar.bz2", ".tgz", ".iso", ".dmg"],
        "mime_keywords": ["zip", "compressed", "archive", "tar"],
        "icon": "🗜️",
        "color": "#6b7280"
    },
    # Executables
    "Executables": {
        "extensions": [".exe", ".msi", ".app", ".deb", ".rpm", ".apk", ".ipa",
                        ".bin", ".run", ".jar", ".bat", ".cmd"],
        "mime_keywords": ["executable", "octet-stream"],
        "icon": "⚙️",
        "color": "#ef4444"
    },
    # Fonts
    "Fonts": {
        "extensions": [".ttf", ".otf", ".woff", ".woff2", ".eot", ".fon"],
        "mime_prefix": "font/",
        "icon": "🔤",
        "color": "#a78bfa"
    },
}

DEFAULT_CATEGORY = "Others"
DEFAULT_ICON = "📁"
DEFAULT_COLOR = "#94a3b8"


# ── Core functions ────────────────────────────────────────────────────────────

def classify_file(filepath: str) -> dict:
    """
    Classify a file by content and return a rich metadata dict.
    Returns: { category, file_type, mime_type, icon, color, file_size, checksum }
    """
    ext = os.path.splitext(filepath)[1].lower()
    mime_type, _ = mimetypes.guess_type(filepath)
    mime_type = mime_type or "application/octet-stream"
    file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
    checksum = compute_checksum(filepath)
    category, icon, color = _detect_category(ext, mime_type)

    return {
        "category": category,
        "file_type": ext.lstrip(".").upper() or "UNKNOWN",
        "mime_type": mime_type,
        "icon": icon,
        "color": color,
        "file_size": file_size,
        "checksum": checksum,
    }


def classify_by_name(filename: str) -> dict:
    """Classify using only filename (no filesystem access required)."""
    ext = os.path.splitext(filename)[1].lower()
    mime_type, _ = mimetypes.guess_type(filename)
    mime_type = mime_type or "application/octet-stream"
    category, icon, color = _detect_category(ext, mime_type)
    return {
        "category": category,
        "file_type": ext.lstrip(".").upper() or "UNKNOWN",
        "mime_type": mime_type,
        "icon": icon,
        "color": color,
    }


def _detect_category(ext: str, mime_type: str) -> tuple:
    """Return (category, icon, color) tuple."""
    for cat_name, rules in CATEGORY_MAP.items():
        # Extension match
        if ext in rules.get("extensions", []):
            return cat_name, rules["icon"], rules["color"]
        # MIME prefix match
        if "mime_prefix" in rules and mime_type.startswith(rules["mime_prefix"]):
            return cat_name, rules["icon"], rules["color"]
        # MIME keyword match
        for kw in rules.get("mime_keywords", []):
            if kw in mime_type:
                return cat_name, rules["icon"], rules["color"]

    return DEFAULT_CATEGORY, DEFAULT_ICON, DEFAULT_COLOR


def compute_checksum(filepath: str, algo: str = "md5") -> str:
    """Compute file checksum for duplicate detection."""
    if not os.path.exists(filepath):
        return ""
    h = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    except (IOError, PermissionError):
        return ""
    return h.hexdigest()


def format_file_size(bytes_val: int) -> str:
    """Human-readable file size."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} PB"


def get_all_categories() -> list:
    """Return list of all category names."""
    return list(CATEGORY_MAP.keys()) + [DEFAULT_CATEGORY]


def get_category_info(category: str) -> dict:
    """Return icon and color for a category."""
    info = CATEGORY_MAP.get(category, {})
    return {
        "icon": info.get("icon", DEFAULT_ICON),
        "color": info.get("color", DEFAULT_COLOR),
    }
