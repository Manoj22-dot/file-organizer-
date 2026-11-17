"""
modules/organizer.py
Core file organization engine.
Moves/copies files into category-based folder structures.
"""

import os
import shutil
from datetime import datetime
from modules.classifier import classify_file, classify_by_name
from modules.database import insert_file, update_file_organized, insert_history


def organize_file(source_path: str, organized_root: str, db_path: str,
                  strategy: str = "copy", duplicate: str = "rename") -> dict:
    """
    Organize a single file into the proper category folder.

    Args:
        source_path: Absolute path to the source file
        organized_root: Root folder where organized files go
        db_path: SQLite database path
        strategy: 'copy' or 'move'
        duplicate: 'rename', 'skip', or 'overwrite'

    Returns:
        dict with keys: success, category, dest_path, file_id, message
    """
    if not os.path.exists(source_path):
        return {"success": False, "message": f"File not found: {source_path}"}

    filename = os.path.basename(source_path)
    meta = classify_file(source_path)
    category = meta["category"]

    # Build destination directory
    dest_dir = os.path.join(organized_root, category)
    os.makedirs(dest_dir, exist_ok=True)

    # Resolve destination path (handle duplicates)
    dest_path = _resolve_destination(dest_dir, filename, duplicate)

    # Insert file record
    file_id = insert_file(
        db_path,
        original_name=filename,
        original_path=source_path,
        file_size=meta["file_size"],
        file_type=meta["file_type"],
        category=category,
        mime_type=meta["mime_type"],
        checksum=meta["checksum"],
    )

    # Perform the operation
    try:
        if dest_path is None:
            # skip duplicate
            update_file_organized(db_path, file_id, source_path, status="skipped")
            insert_history(db_path, "skip", file_id, filename, source_path,
                           source_path, category, "Duplicate skipped", "success")
            return {
                "success": True,
                "category": category,
                "dest_path": source_path,
                "file_id": file_id,
                "message": "Duplicate skipped",
                "icon": meta["icon"],
                "color": meta["color"],
            }

        if strategy == "move":
            shutil.move(source_path, dest_path)
            action = "move"
        else:
            shutil.copy2(source_path, dest_path)
            action = "copy"

        update_file_organized(db_path, file_id, dest_path, status="organized")
        insert_history(db_path, action, file_id, filename, source_path,
                       dest_path, category,
                       f"{action.title()}d → {category}", "success")

        return {
            "success": True,
            "category": category,
            "dest_path": dest_path,
            "file_id": file_id,
            "message": f"File organized into {category}",
            "icon": meta["icon"],
            "color": meta["color"],
            "file_size": meta["file_size"],
            "file_type": meta["file_type"],
        }

    except Exception as e:
        update_file_organized(db_path, file_id, "", status="failed")
        insert_history(db_path, "error", file_id, filename, source_path,
                       "", category, str(e), "error")
        return {"success": False, "message": str(e), "file_id": file_id}


def organize_folder(source_folder: str, organized_root: str, db_path: str,
                    strategy: str = "copy", duplicate: str = "rename",
                    recursive: bool = True) -> dict:
    """
    Organize all files in a folder.

    Returns:
        dict with keys: total, organized, failed, skipped, results
    """
    results = []
    total = organized = failed = skipped = 0

    walk_fn = os.walk if recursive else _single_level_walk
    for dirpath, _, filenames in walk_fn(source_folder):
        for fname in filenames:
            src = os.path.join(dirpath, fname)
            total += 1
            result = organize_file(src, organized_root, db_path,
                                   strategy, duplicate)
            results.append({**result, "filename": fname})
            if result["success"]:
                if "skipped" in result.get("message", "").lower():
                    skipped += 1
                else:
                    organized += 1
            else:
                failed += 1

    return {
        "total": total,
        "organized": organized,
        "failed": failed,
        "skipped": skipped,
        "results": results,
    }


def preview_organization(filenames: list) -> list:
    """
    Given a list of filenames, return what category each would go into.
    Does NOT touch the filesystem.
    """
    preview = []
    for fname in filenames:
        meta = classify_by_name(fname)
        preview.append({
            "filename": fname,
            "category": meta["category"],
            "file_type": meta["file_type"],
            "icon": meta["icon"],
            "color": meta["color"],
        })
    return preview


def get_folder_tree(organized_root: str) -> dict:
    """Return a nested dict of organized_root contents."""
    tree = {}
    if not os.path.exists(organized_root):
        return tree
    for cat_folder in sorted(os.listdir(organized_root)):
        cat_path = os.path.join(organized_root, cat_folder)
        if os.path.isdir(cat_path):
            files = []
            for fname in sorted(os.listdir(cat_path)):
                fpath = os.path.join(cat_path, fname)
                if os.path.isfile(fpath):
                    files.append({
                        "name": fname,
                        "size": os.path.getsize(fpath),
                        "modified": datetime.fromtimestamp(
                            os.path.getmtime(fpath)
                        ).strftime("%Y-%m-%d %H:%M"),
                    })
            tree[cat_folder] = files
    return tree


# ── Helpers ───────────────────────────────────────────────────────────────────

def _resolve_destination(dest_dir: str, filename: str, duplicate: str):
    """Return final destination path or None (skip)."""
    dest_path = os.path.join(dest_dir, filename)
    if not os.path.exists(dest_path):
        return dest_path

    if duplicate == "skip":
        return None

    if duplicate == "overwrite":
        return dest_path

    # rename: append _1, _2, …
    name, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(dest_path):
        dest_path = os.path.join(dest_dir, f"{name}_{counter}{ext}")
        counter += 1
    return dest_path


def _single_level_walk(folder):
    """os.walk replacement that returns only the top level."""
    dirnames, filenames = [], []
    for entry in os.scandir(folder):
        if entry.is_dir():
            dirnames.append(entry.name)
        elif entry.is_file():
            filenames.append(entry.name)
    yield folder, dirnames, filenames
