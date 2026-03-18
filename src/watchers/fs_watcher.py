"""File system watcher.

Watches a configured folder for new files and creates a task in Vault/Needs_Action.

Run:
    python -m src.watchers.fs_watcher

Set `WATCH_FOLDER` in `.env` to the path you want to watch.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.config import settings
from src.utils.vault import normalize_filename, task_header, write_task


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() not in {".txt", ".md", ".pdf", ".docx", ".xlsx"}:
            return
        logging.info("Detected new file: %s", path)
        title = f"New file detected: {path.name}"
        body = f"**Path**: {path}\n\n**Created**: {path.stat().st_ctime}\n\n---\n\nPlease review this file and take action."
        filename = normalize_filename(f"{path.stem}_{path.stat().st_mtime}")
        content = task_header(title, {"source": "fs_watcher", "path": str(path)}) + body
        write_task("Needs_Action", filename, content)
        logging.info("Created task %s", filename)


def main() -> None:
    watch_folder = settings.WATCH_FOLDER
    if not watch_folder:
        print("Please set WATCH_FOLDER in your .env file.")
        sys.exit(1)

    watch_path = Path(watch_folder)
    if not watch_path.exists() or not watch_path.is_dir():
        print(f"WATCH_FOLDER path does not exist or is not a directory: {watch_path}")
        sys.exit(1)

    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, str(watch_path), recursive=False)
    observer.start()

    print(f"Watching folder {watch_path} for new files. Press Ctrl+C to stop.")
    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        print("Stopping watcher...")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
