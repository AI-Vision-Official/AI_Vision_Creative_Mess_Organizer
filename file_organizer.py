import os
import shutil
import logging
from pathlib import Path
from datetime import datetime
from PIL import Image
from mutagen import File as AudioFile
from pymediainfo import MediaInfo
from ebooklib import epub
import PyPDF2

# ---------------- CONFIG ---------------- #
SOURCE_DIR = Path(r"J:\GIT\MyProject\FileOrganizer\TestFiles")
DEST_DIR = Path(r"J:\GIT\MyProject\FileOrganizer\Organized")
QUARANTINE_DIR = Path(r"J:\GIT\MyProject\FileOrganizer\Quarantine")
DRY_RUN = False  # Set to False to actually move files
# ----------------------------------------- #

# Ensure folders exist
DEST_DIR.mkdir(parents=True, exist_ok=True)
QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

# Setup logging
log_file = Path(__file__).parent / f"file_organizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_and_print(message):
    print(message)
    logging.info(message)

def get_file_type(file_path):
    """Detect file type based on extension & content"""
    ext = file_path.suffix.lower()

    if ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]:
        return "Images"
    elif ext in [".mp3", ".wav", ".flac", ".aac", ".ogg"]:
        return "Audio"
    elif ext in [".mp4", ".avi", ".mkv", ".mov", ".wmv"]:
        return "Video"
    elif ext in [".epub"]:
        return "eBooks"
    elif ext in [".pdf"]:
        return "PDFs"
    else:
        return "Other"

def organize_file(file_path):
    file_type = get_file_type(file_path)
    target_folder = DEST_DIR / file_type
    target_folder.mkdir(parents=True, exist_ok=True)

    new_path = target_folder / file_path.name

    if DRY_RUN:
        log_and_print(f"[DRY RUN] Would move: {file_path} → {new_path}")
    else:
        try:
            shutil.move(str(file_path), str(new_path))
            log_and_print(f"Moved: {file_path} → {new_path}")
        except Exception as e:
            # If move fails, send to quarantine
            quarantine_path = QUARANTINE_DIR / file_path.name
            shutil.move(str(file_path), str(quarantine_path))
            logging.error(f"Error moving {file_path}: {e}. Sent to quarantine.")

def main():
    log_and_print("=== File Organizer Started ===")
    log_and_print(f"Source: {SOURCE_DIR}")
    log_and_print(f"Destination: {DEST_DIR}")
    log_and_print(f"Quarantine: {QUARANTINE_DIR}")
    log_and_print(f"Dry-run mode: {DRY_RUN}")

    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = Path(root) / file
            organize_file(file_path)

    log_and_print("=== File Organizer Finished ===")

if __name__ == "__main__":
    main()
