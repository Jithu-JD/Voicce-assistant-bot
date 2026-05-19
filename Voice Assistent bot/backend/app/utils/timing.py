# app/utils/timing.py
import time
from contextlib import contextmanager
from typing import Dict, Any, List, Tuple, Optional

def _now() -> float:
    return time.perf_counter()

def start_trace(tag: str):
    """
    Returns (ctx, log) where:
      - ctx is a dict storing spans: {"tag": str, "t0": float, "spans": [(label, dur_s), ...]}
      - log() prints a compact one-line summary
    """
    ctx: Dict[str, Any] = {"tag": tag, "t0": _now(), "spans": []}
    def log():
        total = _now() - ctx["t0"]
        parts = " | ".join(f"{name}: {dur*1000:.0f}ms" for name, dur in ctx["spans"])
        print(f"[TRACE] {ctx['tag']} :: {parts} || total: {total*1000:.0f}ms")
    return ctx, log

@contextmanager
def span(label: str, ctx: Optional[Dict[str, Any]] = None):
    """
    Time a block. If ctx is provided (from start_trace), append to ctx['spans'].
    Always prints a simple line for quick visibility.
    """
    t0 = _now()
    try:
        yield
    finally:
        dur = _now() - t0
        # append into trace context if available
        try:
            if ctx is not None and isinstance(ctx.get("spans", None), list):
                ctx["spans"].append((label, dur))
        except Exception:
            pass
        # also print a standalone SPAN (useful outside request contexts)
        print(f"[SPAN] {label}: {dur*1000:.0f}ms")
