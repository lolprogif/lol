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


def wait_for_pid(pid: int, timeout_ms: int = 120000):
    if os.name != "nt" or pid <= 0:
        return True
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_uint]
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint]
    kernel.WaitForSingleObject.restype = ctypes.c_uint
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    handle = kernel.OpenProcess(0x00100000, False, pid)  # SYNCHRONIZE
    if not handle:
        # If the old process has already exited, no wait is needed.
        return True
    try:
        result = kernel.WaitForSingleObject(handle, timeout_ms)
        if result == 0:  # WAIT_OBJECT_0
            return True
        if result == 0x102:  # WAIT_TIMEOUT
            return False
        raise ctypes.WinError(ctypes.get_last_error())
    finally:
        kernel.CloseHandle(handle)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_member(name: str) -> bool:
    # ZIP directory entries conventionally end with '/'; allow that only for
    # the _internal tree, while still rejecting traversal and absolute paths.
    normalized = name.replace("\\\\", "/")
    is_dir = normalized.endswith("/")
    normalized = normalized.rstrip("/")
    parts = normalized.split("/")
    if not normalized or normalized.startswith("/") or any(part in ("", ".", "..") for part in parts):
        return False
    if is_dir:
        return normalized == "_internal" or normalized.startswith("_internal/")
    return normalized == APP_EXE or normalized.startswith("_internal/")

def main():
    if len(sys.argv) < 5:
        raise SystemExit("Uso: update_helper.exe <install_dir> <zip> <pid> <sha256>")
    install = Path(sys.argv[1]).resolve()
    archive = Path(sys.argv[2]).resolve()
    pid = int(sys.argv[3])
    expected = sys.argv[4].strip().lower()
    if not install.is_dir() or not archive.is_file():
        raise RuntimeError("Pasta de instalação ou pacote de atualização não encontrado.")
    if len(expected) != 64 or sha256_file(archive) != expected:
        raise RuntimeError("Hash SHA-256 do pacote não confere. Atualização cancelada.")
    if not wait_for_pid(pid):
        raise RuntimeError("O LOI antigo não fechou no tempo esperado. Atualização cancelada para evitar substituir arquivos em uso.")
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
            # Reject symbolic links and duplicate archive paths.
            seen = set()
            for member in members:
                normalized = member.filename.replace("\\", "/")
                if normalized in seen:
                    raise RuntimeError("Pacote contém caminhos duplicados.")
                seen.add(normalized)
                if (member.external_attr >> 16) & 0o170000 == 0o120000:
                    raise RuntimeError("Pacote contém link simbólico; atualização bloqueada.")
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
            # Register before replacing so a partially failed copy is also rolled back.
            changed.append(item)
            if target.exists():
                if target.is_dir(): shutil.rmtree(target)
                else: target.unlink()
            shutil.copytree(source, target) if source.is_dir() else shutil.copy2(source, target)
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
