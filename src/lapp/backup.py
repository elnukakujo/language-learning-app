from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import shutil
import os

# Use absolute paths to avoid issues from different working directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "db" / "languages.db"
BACKUP_DIR = BASE_DIR / "backups"  # safer than "../../backups"

def restore_sqlite():
    if not BACKUP_DIR.exists():
        print(f"[Restore] Backup directory {BACKUP_DIR} does not exist. Restore skipped.")
        return

    backup_files = list(BACKUP_DIR.glob("backup_*.sqlite"))
    if not backup_files:
        print(f"[Restore] No backups found in {BACKUP_DIR}. Restore skipped.")
        return
    elif len(backup_files) > 20:
        # If more than 10 backups, delete the oldest one
        oldest_backup = min(backup_files, key=lambda f: f.stat().st_ctime)
        oldest_backup.unlink()
        os.remove(oldest_backup)

    latest_backup = max(backup_files, key=lambda f: f.stat().st_ctime)
    shutil.copy(latest_backup, DB_PATH)
    print(f"[Restore] Restored from {latest_backup}")

def backup_sqlite():
    if not DB_PATH.exists():
        print(f"[Backup] Database file {DB_PATH} does not exist. Backup skipped.")
        return
    
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"backup_{timestamp}.sqlite"
    shutil.copy(DB_PATH, backup_path)
    print(f"[Backup] Saved to {backup_path}")

def start_backup_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(backup_sqlite, 'interval', minutes=15)
    scheduler.start()
    print("[Backup] Scheduler started")