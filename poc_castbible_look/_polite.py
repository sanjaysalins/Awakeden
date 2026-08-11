"""Keep this process (and anything it spawns, e.g. ffmpeg) polite so the rest of
the machine stays usable -- same recipe as day_of_atonement/_polite.py, copied
per-folder per this project's own convention (bronze_serpent, psalm_22 do the
same) rather than cross-imported.

On Windows a child process inherits its parent's PRIORITY CLASS and CPU AFFINITY,
and the affinity mask also limits in-process worker threads (e.g. whisperx/torch),
so calling this once at the top of a script throttles everything it does.

    POLITE_CPU=33   (default) -> capped to ~a third of logical CPUs
    POLITE_CPU=0              -> off (full speed)

Import and call be_polite() at the very top of a build/align script, before any
heavy work runs.
"""
import os
import sys

IDLE_PRIORITY_CLASS = 0x00000040
MEMORY_PRIORITY_LOW = 2


def be_polite():
    try:
        pct = int(os.environ.get("POLITE_CPU", "33"))
    except ValueError:
        return
    if pct <= 0 or pct >= 100 or sys.platform != "win32":
        return
    import ctypes
    from ctypes import wintypes
    n = os.cpu_count() or 1
    keep = max(1, min(n, round(n * pct / 100)))
    mask = (1 << keep) - 1
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.GetCurrentProcess.restype = wintypes.HANDLE
    k32.SetPriorityClass.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    k32.SetPriorityClass.restype = wintypes.BOOL
    k32.SetProcessAffinityMask.argtypes = [wintypes.HANDLE, ctypes.c_size_t]
    k32.SetProcessAffinityMask.restype = wintypes.BOOL
    h = k32.GetCurrentProcess()
    ok_prio = k32.SetPriorityClass(h, IDLE_PRIORITY_CLASS)
    ok_aff = k32.SetProcessAffinityMask(h, mask)
    if not (ok_prio and ok_aff):
        print(f"[polite] WARNING: throttle failed (prio={bool(ok_prio)} aff={bool(ok_aff)}, "
              f"err={ctypes.get_last_error()}) -- running at full speed", flush=True)
        return
    try:
        k32.SetProcessInformation.argtypes = [wintypes.HANDLE, ctypes.c_int,
                                              ctypes.c_void_p, wintypes.DWORD]
        mp = ctypes.c_ulong(MEMORY_PRIORITY_LOW)
        k32.SetProcessInformation(h, 0, ctypes.byref(mp), 4)
    except Exception:
        pass
    print(f"[polite] capped to {keep}/{n} logical CPUs (~{pct}%) + Idle priority "
          f"+ low memory priority (POLITE_CPU=0 to disable)", flush=True)
