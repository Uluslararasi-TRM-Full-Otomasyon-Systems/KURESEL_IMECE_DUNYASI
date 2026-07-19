import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = ROOT_DIR / "Uluslararası TRM Otonom Ekosistemi"
IGNORE_NAMES = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "streamlit_env",
    ".streamlit-lib",
    ".python-libs",
    ".python-user",
}


def slugify(name):
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip()).strip("-").lower()
    return slug or "yeni-firma"


def append_tenant_config(config_path, company_name, tenant_slug):
    block = f"""

# === MULTI-TENANT KLON AYARLARI ===
TENANT_COMPANY_NAME = {company_name!r}
TENANT_SLUG = {tenant_slug!r}
GUARDIAN_AGENT_COUNT = 165
GUARDIAN_HEARTBEAT_INTERVAL_SECONDS = 60
GUARDIAN_HEARTBEAT_TIMEOUT_SECONDS = 180
GUARDIAN_BACKUP_DIR = "backups"
GUARDIAN_AUTO_START = True
GUARDIAN_HEARTBEAT_FILES = ["worker_status.json", "healthcheck_status.json"]
GUARDIAN_TELEGRAM_BOT_TOKEN = ""
GUARDIAN_TELEGRAM_CHAT_ID = ""
"""
    existing = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    if "TENANT_COMPANY_NAME" in existing:
        return
    config_path.write_text(existing + block, encoding="utf-8")


def create_start_guardian_script(target_dir):
    script_path = target_dir / "START_GUARDIAN.bat"
    script_path.write_text(
        "@echo off\n"
        "cd /d %~dp0\n"
        "python guardian_agent.py --daemon\n",
        encoding="utf-8",
    )


def create_initial_backup(target_dir):
    backup_dir = target_dir / "backups"
    backup_dir.mkdir(exist_ok=True)
    backup_name = backup_dir / f"baseline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    with zipfile.ZipFile(backup_name, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in target_dir.rglob("*"):
            if not path.is_file():
                continue
            if "backups" in path.parts or "__pycache__" in path.parts:
                continue
            archive.write(path, path.relative_to(target_dir))
    return backup_name


def start_guardian_process(target_dir):
    command = [sys.executable, "guardian_agent.py", "--daemon"]
    creationflags = 0
    if sys.platform.startswith("win"):
        creationflags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    process = subprocess.Popen(
        command,
        cwd=str(target_dir),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=creationflags,
        close_fds=False,
    )
    return process.pid


def clone_company_system(company_name, start_guardian=True):
    if not TEMPLATE_DIR.exists():
        raise FileNotFoundError(f"Şablon klasörü bulunamadı: {TEMPLATE_DIR}")

    tenant_slug = slugify(company_name)
    target_dir = ROOT_DIR / tenant_slug
    if target_dir.exists():
        raise FileExistsError(f"Hedef klasör zaten var: {target_dir}")

    shutil.copytree(
        TEMPLATE_DIR,
        target_dir,
        ignore=shutil.ignore_patterns(*IGNORE_NAMES),
    )

    guardian_source = TEMPLATE_DIR / "guardian_agent.py"
    guardian_target = target_dir / "guardian_agent.py"
    if not guardian_target.exists() and guardian_source.exists():
        shutil.copy2(guardian_source, guardian_target)

    config_path = target_dir / "config.py"
    if not config_path.exists():
        config_path.write_text("# Auto-generated tenant config\n", encoding="utf-8")
    append_tenant_config(config_path, company_name, tenant_slug)
    create_start_guardian_script(target_dir)
    backup_zip = create_initial_backup(target_dir)

    pid = None
    if start_guardian:
        pid = start_guardian_process(target_dir)

    manifest = {
        "company_name": company_name,
        "tenant_slug": tenant_slug,
        "target_dir": str(target_dir),
        "guardian_pid": pid,
        "guardian_status_file": str(target_dir / "guardian_status.json"),
        "guardian_start_script": str(target_dir / "START_GUARDIAN.bat"),
        "baseline_backup": str(backup_zip),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    (target_dir / "clone_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return manifest


def main():
    parser = argparse.ArgumentParser(description="TRM çoklu-tenant firma klonlayıcı")
    parser.add_argument("company_name", help="Yeni firma adı")
    parser.add_argument("--no-start", action="store_true", help="Guardian ajanını otomatik başlatma")
    args = parser.parse_args()

    manifest = clone_company_system(args.company_name, start_guardian=not args.no_start)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
