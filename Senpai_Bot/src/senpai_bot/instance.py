from __future__ import annotations

import os
import tempfile
from pathlib import Path


class SingleInstance:
    """Hold a per-user application lock for the lifetime of the process."""

    def __init__(self, name: str):
        self.name = name
        self._windows_handle: int | None = None
        self._lock_file = None

    def acquire(self) -> bool:
        if os.name == "nt":
            return self._acquire_windows_mutex()
        return self._acquire_file_lock()

    def _acquire_windows_mutex(self) -> bool:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        create_mutex = kernel32.CreateMutexW
        create_mutex.argtypes = (wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR)
        create_mutex.restype = wintypes.HANDLE
        close_handle = kernel32.CloseHandle
        close_handle.argtypes = (wintypes.HANDLE,)
        close_handle.restype = wintypes.BOOL

        handle = create_mutex(None, False, f"Local\\{self.name}")
        if not handle:
            raise OSError(ctypes.get_last_error(), "Could not create the Senpai_Bot instance mutex")
        if ctypes.get_last_error() == 183:  # ERROR_ALREADY_EXISTS
            close_handle(handle)
            return False
        self._windows_handle = int(handle)
        return True

    def _acquire_file_lock(self) -> bool:
        import fcntl

        lock_path = Path(tempfile.gettempdir()) / f"{self.name}.lock"
        lock_file = lock_path.open("a+b")
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            lock_file.close()
            return False
        self._lock_file = lock_file
        return True

    def close(self) -> None:
        if self._windows_handle is not None:
            import ctypes
            from ctypes import wintypes

            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            close_handle = kernel32.CloseHandle
            close_handle.argtypes = (wintypes.HANDLE,)
            close_handle.restype = wintypes.BOOL
            close_handle(wintypes.HANDLE(self._windows_handle))
            self._windows_handle = None
        if self._lock_file is not None:
            import fcntl

            fcntl.flock(self._lock_file.fileno(), fcntl.LOCK_UN)
            self._lock_file.close()
            self._lock_file = None
