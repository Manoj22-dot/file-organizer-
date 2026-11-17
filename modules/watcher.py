"""
modules/watcher.py
Folder watcher that auto-organizes files when they are added/modified.
Uses polling (no watchdog dependency required).
"""

import os
import time
import threading
import logging
from datetime import datetime
from modules.organizer import organize_file
from modules.database import get_setting

logger = logging.getLogger("FileWatcher")
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")


class FolderWatcher:
    """
    Polls a folder at regular intervals and organizes new files automatically.
    """

    def __init__(self, watch_folder: str, organized_root: str,
                 db_path: str, interval: int = 5):
        self.watch_folder = watch_folder
        self.organized_root = organized_root
        self.db_path = db_path
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread = None
        self._seen_files = set()
        self.running = False

    def start(self):
        if self.running:
            logger.warning("Watcher already running.")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
        self.running = True
        logger.info(f"👁️  Watching folder: {self.watch_folder}")

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=10)
        self.running = False
        logger.info("Watcher stopped.")

    def _watch_loop(self):
        # Pre-populate seen files so existing ones aren't re-organized
        if os.path.exists(self.watch_folder):
            for f in os.listdir(self.watch_folder):
                self._seen_files.add(f)

        while not self._stop_event.is_set():
            self._check_for_new_files()
            time.sleep(self.interval)

    def _check_for_new_files(self):
        if not os.path.exists(self.watch_folder):
            return
        current_files = set(os.listdir(self.watch_folder))
        new_files = current_files - self._seen_files

        for fname in new_files:
            fpath = os.path.join(self.watch_folder, fname)
            if not os.path.isfile(fpath):
                continue
            if self._is_file_ready(fpath):
                logger.info(f"New file detected: {fname}")
                result = organize_file(
                    source_path=fpath,
                    organized_root=self.organized_root,
                    db_path=self.db_path,
                    strategy="move",
                    duplicate=get_setting(self.db_path,
                                          "duplicate_handling", "rename"),
                )
                if result["success"]:
                    logger.info(
                        f"✅ Organized '{fname}' → {result['category']}")
                else:
                    logger.error(
                        f"❌ Failed to organize '{fname}': {result['message']}")
                self._seen_files.add(fname)

    @staticmethod
    def _is_file_ready(filepath: str, wait: float = 0.5) -> bool:
        """Check if a file is fully written (stable size)."""
        try:
            size1 = os.path.getsize(filepath)
            time.sleep(wait)
            size2 = os.path.getsize(filepath)
            return size1 == size2 and size2 > 0
        except OSError:
            return False

    def status(self) -> dict:
        return {
            "running": self.running,
            "watch_folder": self.watch_folder,
            "interval_seconds": self.interval,
            "files_seen": len(self._seen_files),
        }


# ── Singleton watcher instance ────────────────────────────────────────────────
_watcher_instance: FolderWatcher = None


def get_watcher() -> FolderWatcher:
    return _watcher_instance


def start_watcher(watch_folder: str, organized_root: str,
                  db_path: str, interval: int = 5):
    global _watcher_instance
    if _watcher_instance and _watcher_instance.running:
        _watcher_instance.stop()
    _watcher_instance = FolderWatcher(watch_folder, organized_root,
                                      db_path, interval)
    _watcher_instance.start()
    return _watcher_instance


def stop_watcher():
    global _watcher_instance
    if _watcher_instance:
        _watcher_instance.stop()
