"""LOI updater helper. Windows-only at runtime; safely replaces app files and rolls back."""
import ctypes
import hashlib
import os
import shutil
import sys
import tempfile
import time
import zipfile
from pathlib import Path

APP_EXE = "LOICatFarmPro.exe"


def wait_for_pid(pid: int):
    if os.name != "nt" or pid <= 0:
        return
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_uint]
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint]
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    handle = kernel.OpenProcess(0x00100000, False, pid)  # SYNCHRONIZE
    if handle:
        try:
            kernel.WaitForSingleObject(handle, 120000)
        finally:
            kernel.CloseHandle(handle)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_member(name: str) -> bool:
    p = Path(name)
    if p.is_absolute() or ".." in p.parts or name.startswith(("/", "\\")):
        return False
    normalized = str(p).replace("\\", "/")
    return normalized == APP_EXE or normalized.startswith("_internal/") or normalized == "_internal"


def main():
    if len(sys.argv) < 4:
        raise SystemExit("Uso: update_helper.exe <install_dir> <zip> <pid> <sha256>")
    install = Path(sys.argv[1]).resolve()
    archive = Path(sys.argv[2]).resolve()
    pid = int(sys.argv[3])
    expected = sys.argv[4].strip().lower()
    if not install.is_dir() or not archive.is_file():
        raise RuntimeError("Pasta de instalação ou pacote de atualização não encontrado.")
    if len(expected) != 64 or sha256_file(archive) != expected:
        raise RuntimeError("Hash SHA-256 do pacote não confere. Atualização cancelada.")
    wait_for_pid(pid)
    local = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "LOI_CATFARM_PRO" / "update_work"
    local.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="stage_", dir=str(local)))
    backup = Path(tempfile.mkdtemp(prefix="backup_", dir=str(local)))
    changed = []
    try:
        with zipfile.ZipFile(archive) as z:
            members = z.infolist()
            if not members or any(not safe_member(m.filename) for m in members):
                raise RuntimeError("Pacote contém caminhos inválidos ou arquivos fora do aplicativo.")
            z.extractall(stage)
        if not (stage / APP_EXE).is_file() or not (stage / "_internal").is_dir():
            raise RuntimeError("Pacote de atualização incompleto: executável ou _internal ausente.")
        # Preserve locally stored JSON preferences in the PyInstaller internal folder.
        old_internal = install / "_internal"
        if old_internal.is_dir():
            for config in old_internal.glob("*.json"):
                target_config = stage / "_internal" / config.name
                if config.is_file() and not target_config.exists():
                    shutil.copy2(config, target_config)
        # Prepare backups of the two app components, leaving all user data untouched.
        for item in (APP_EXE, "_internal"):
            target = install / item
            if target.exists():
                shutil.copytree(target, backup / item) if target.is_dir() else shutil.copy2(target, backup / item)
        for item in ("_internal", APP_EXE):
            source, target = stage / item, install / item
            if target.exists():
                if target.is_dir(): shutil.rmtree(target)
                else: target.unlink()
            shutil.copytree(source, target) if source.is_dir() else shutil.copy2(source, target)
            changed.append(item)
        os.startfile(str(install / APP_EXE))
    except Exception:
        for item in reversed(changed):
            target, old = install / item, backup / item
            if target.exists():
                if target.is_dir(): shutil.rmtree(target)
                else: target.unlink()
            if old.exists():
                shutil.copytree(old, target) if old.is_dir() else shutil.copy2(old, target)
        raise
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        try: archive.unlink()
        except OSError: pass


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk(); root.withdraw(); messagebox.showerror("LOI CATFARM PRO — Atualização", str(exc)); root.destroy()
        except Exception:
            print(exc, file=sys.stderr)
        raise
