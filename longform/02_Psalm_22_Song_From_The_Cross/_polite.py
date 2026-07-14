"""Keep CPU-heavy child processes (ffmpeg) polite so the rest of the machine stays usable.

On Windows a child process inherits its parent's PRIORITY CLASS and CPU AFFINITY. So setting
them once on THIS python process throttles every ffmpeg it later spawns — including the calls
inside the locked comic_engine — with no per-ffmpeg edits and no admin rights / extra tools.

Tune with the POLITE_CPU env var = target % of logical CPUs (snapped to whole cores):
    POLITE_CPU=33   (default) -> ffmpeg capped to ~a third of the threads (machine stays free)
    POLITE_CPU=50             -> ~half (faster renders, machine less free)
    POLITE_CPU=0              -> off (full speed, old behaviour)

Gentler since 2026-07-14: IDLE priority (render yields the instant the user does anything)
+ LOW memory priority (Windows reclaims the render job's RAM pages first under pressure).

Import and call be_polite() at the very top of a build script, before any ffmpeg runs.
"""
import os
import sys

IDLE_PRIORITY_CLASS = 0x00000040
MEMORY_PRIORITY_LOW = 2


def be_polite():
    """Lower this process (and inherited ffmpeg children) to Idle priority + cap it to
    the lowest `keep` logical CPUs + LOW memory priority. No-op off-Windows or POLITE_CPU=0."""
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
    # Declare types: HANDLE is 64-bit — without this, ctypes truncates the pseudo-handle and
    # the calls silently no-op.
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
              f"err={ctypes.get_last_error()}) — running at full speed", flush=True)
        return
    try:  # memory priority LOW (this process only; Win8+)
        k32.SetProcessInformation.argtypes = [wintypes.HANDLE, ctypes.c_int,
                                              ctypes.c_void_p, wintypes.DWORD]
        mp = ctypes.c_ulong(MEMORY_PRIORITY_LOW)
        k32.SetProcessInformation(h, 0, ctypes.byref(mp), 4)  # 0 = ProcessMemoryPriority
    except Exception:
        pass
    print(f"[polite] ffmpeg capped to {keep}/{n} logical CPUs (~{pct}%) + Idle priority "
          f"+ low memory priority (POLITE_CPU=0 to disable)", flush=True)
