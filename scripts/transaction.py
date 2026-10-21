"""Recoverable multi-file writes for the catalog and its generated documentation.

Replacement is atomic per file, not across filesystem readers. Writers share a
lock; failed writes roll back, and interrupted writes recover on the next run.
"""

from contextlib import contextmanager
import json
import os
from pathlib import Path
import shutil

try:
    from .catalog import CatalogError, atomic_write
except ImportError:
    from catalog import CatalogError, atomic_write


def _target(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or path == root:
        raise CatalogError("Transaction target escapes project root")
    return path


def recover(root):
    """Restore the pre-write snapshot unless the commit marker was persisted."""
    root = Path(root).resolve()
    folder = root / ".cache" / "catalog-transaction"
    manifest = folder / "manifest.json"
    if not manifest.exists():
        if folder.exists():
            shutil.rmtree(folder)
        return
    record = json.loads(manifest.read_text(encoding="utf-8"))
    if record["state"] != "committed":
        for index, entry in enumerate(record["files"]):
            target = _target(root, entry["path"])
            if entry["existed"]:
                # Preserve backups until every restoration has completed, allowing retries.
                temporary = folder / f"restore-{index}"
                shutil.copy2(folder / f"old-{index}", temporary)
                os.replace(temporary, target)
            else:
                target.unlink(missing_ok=True)
    shutil.rmtree(folder)


@contextmanager
def write_lock(root):
    """Serialize maintenance writers and recover any previous interrupted write."""
    root = Path(root).resolve()
    cache = root / ".cache"
    cache.mkdir(parents=True, exist_ok=True)
    with (cache / "catalog-write.lock").open("a+b") as handle:
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise CatalogError("Another catalog writer is running; retry after it finishes") from None
        try:
            recover(root)
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def commit_files(outputs, root):
    """Commit prepared outputs while holding write_lock(root)."""
    root = Path(root).resolve()
    changed = {}
    for path, text in outputs.items():
        path = Path(path).resolve()
        _target(root, path.relative_to(root))
        encoded = text.encode("utf-8")
        if not path.exists() or path.read_bytes() != encoded:
            changed[path] = encoded
    if not changed:
        return
    folder = root / ".cache" / "catalog-transaction"
    folder.mkdir(parents=True)
    record = {"state": "prepared", "files": []}
    try:
        for index, (target, content) in enumerate(changed.items()):
            target.parent.mkdir(parents=True, exist_ok=True)
            existed = target.exists()
            if existed:
                shutil.copy2(target, folder / f"old-{index}")
            with (folder / f"new-{index}").open("wb") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            record["files"].append({"path": target.relative_to(root).as_posix(), "existed": existed})
        atomic_write(folder / "manifest.json", json.dumps(record))
        for index, target in enumerate(changed):
            os.replace(folder / f"new-{index}", target)
        record["state"] = "committed"
        atomic_write(folder / "manifest.json", json.dumps(record))
    except BaseException:
        # Includes a graceful interrupt. A hard process termination leaves the
        # journal for write_lock() to recover before any subsequent reads/writes.
        try:
            recover(root)
        except OSError as exc:
            raise CatalogError("Write failed and recovery is pending in .cache/catalog-transaction; fix disk access and rerun maintenance") from exc
        raise
    shutil.rmtree(folder)
