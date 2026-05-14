"""
Hover inspector + interaction logger for any Windows UI (AutoCAD dialogs etc).

While running:
  * A small always-on-top, click-through overlay shows live UIA info about
    whatever element is under your mouse cursor.
  * Every mouse click (left/middle/right) is logged with the element that
    was under the cursor at the moment of the click.
  * Hotkeys (picked to avoid AutoCAD's F1–F12 toggles):

        Ctrl+Shift+P   pause / resume the hover overlay
        Ctrl+Shift+L   log the CURRENT hovered element without clicking
                       (useful for tooltips, hover-only UI, or anything
                        a real click would dismiss)
        Ctrl+Shift+Q   quit and write the summary

Outputs (written next to this script):
  ui_interactions.jsonl          one JSON record per logged event
  ui_interactions_summary.txt    final summary on quit

Requirements:
    pip install pywinauto pynput comtypes pywin32
Windows only; run with the same bitness as your AutoCAD.
"""

from __future__ import annotations

import json
import os
import sys
import threading
import time
from collections import Counter
from ctypes import Structure, byref, c_long, windll
from datetime import datetime
from pathlib import Path

import tkinter as tk

from pynput import keyboard, mouse
from pywinauto import Desktop


# ----------------------------- configuration ---------------------------------

OUT_DIR             = Path(__file__).parent
LOG_PATH            = OUT_DIR / "ui_interactions.jsonl"
SUMMARY_PATH        = OUT_DIR / "ui_interactions_summary.txt"

POLL_INTERVAL_S     = 0.20      # how often the background poller queries UIA
UI_REFRESH_MS       = 100       # how often tk refreshes the overlay
OVERLAY_GEOMETRY    = "460x300+20+20"   # WxH +x+y; top-left of screen
MAKE_CLICK_THROUGH  = True      # overlay won't catch clicks meant for AutoCAD

SELF_PID            = os.getpid()

# -----------------------------------------------------------------------------


if sys.platform != "win32":
    sys.exit("This script requires Windows.")


# -------- Win32 helpers ------------------------------------------------------

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def get_cursor_pos() -> tuple[int, int]:
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y


def make_window_click_through(tk_root: tk.Tk) -> None:
    """Apply WS_EX_LAYERED | WS_EX_TRANSPARENT so the overlay never steals input."""
    GWL_EXSTYLE        = -20
    WS_EX_LAYERED      = 0x00080000
    WS_EX_TRANSPARENT  = 0x00000020
    WS_EX_TOOLWINDOW   = 0x00000080
    hwnd = tk_root.winfo_id()
    user32 = windll.user32
    style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    user32.SetWindowLongW(
        hwnd, GWL_EXSTYLE,
        style | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW,
    )


# -------- UIA inspection -----------------------------------------------------

def safe(fn, default=None):
    try:
        return fn()
    except Exception:
        return default


def element_at_point(x: int, y: int):
    """Return the UIA wrapper at (x, y), or None. Skips elements in our own process."""
    elem = safe(lambda: Desktop(backend="uia").from_point(x, y))
    if elem is None:
        return None
    if safe(lambda: elem.element_info.process_id) == SELF_PID:
        return None
    return elem


def describe(elem) -> dict | None:
    """Pull every property worth having from a UIA element."""
    if elem is None:
        return None
    info = elem.element_info
    rect = info.rectangle
    rec: dict = {
        "ts":            datetime.now().isoformat(timespec="seconds"),
        "control_type":  info.control_type,
        "name":          info.name,
        "automation_id": info.automation_id,
        "class_name":    info.class_name,
        "framework":     getattr(info, "framework_id", None),
        "enabled":       info.enabled,
        "visible":       info.visible,
        "rect":          [rect.left, rect.top, rect.right, rect.bottom],
    }

    # Extra UIA properties via the raw IUIAutomationElement
    raw = safe(lambda: info.element)
    if raw is not None:
        for attr, key in [
            ("CurrentAccessKey",            "access_key"),
            ("CurrentAcceleratorKey",       "accelerator_key"),
            ("CurrentHelpText",             "help_text"),
            ("CurrentItemStatus",           "item_status"),
            ("CurrentLocalizedControlType", "localized_control_type"),
            ("CurrentIsKeyboardFocusable",  "keyboard_focusable"),
            ("CurrentIsPassword",           "is_password"),
        ]:
            val = safe(lambda a=attr: getattr(raw, a))
            if val not in (None, "", False):
                rec[key] = val

    # Type-specific value / state
    ctype = info.control_type
    if ctype == "CheckBox":
        rec["value"] = safe(elem.get_toggle_state)            # 0/1/2
    elif ctype == "RadioButton":
        rec["value"] = safe(elem.is_selected)
    elif ctype == "Edit":
        rec["value"] = safe(elem.get_value) or safe(elem.window_text)
    elif ctype == "ComboBox":
        rec["value"] = safe(elem.selected_text)
        items = safe(lambda: elem.item_texts(), None)
        if items:
            rec["items"] = items
    elif ctype == "TabItem":
        rec["value"] = safe(elem.is_selected)
    elif ctype == "Slider":
        rec["value"] = safe(elem.get_value)
    elif ctype in ("Button", "SplitButton", "Hyperlink", "MenuItem",
                   "Text", "Static"):
        rec["value"] = safe(elem.window_text)

    return {k: v for k, v in rec.items() if v not in (None, "", [], {})}


# -------- Persistent log -----------------------------------------------------

class JsonlLogger:
    def __init__(self, path: Path):
        self.path = path
        self.lock = threading.Lock()
        self.events_logged = 0
        self.by_event = Counter()
        self.by_type  = Counter()
        self.by_name  = Counter()

    def write(self, event: dict) -> None:
        with self.lock:
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
            self.events_logged += 1
            self.by_event[event.get("event", "?")] += 1
            if event.get("control_type"):
                self.by_type[event["control_type"]] += 1
            if event.get("name"):
                self.by_name[event["name"]] += 1

    def summary(self) -> str:
        lines = [
            f"Session ended: {datetime.now().isoformat(timespec='seconds')}",
            f"Total events logged: {self.events_logged}",
            "",
            "By event:",
        ]
        for k, n in self.by_event.most_common():
            lines.append(f"  {k:<15} {n}")
        lines += ["", "By control type:"]
        for k, n in self.by_type.most_common():
            lines.append(f"  {k:<20} {n}")
        lines += ["", "By element name (top 30):"]
        for k, n in self.by_name.most_common(30):
            lines.append(f"  {k!r:<45} {n}")
        return "\n".join(lines)


# -------- Hover overlay ------------------------------------------------------

class HoverInspector:
    def __init__(self, logger: JsonlLogger):
        self.logger        = logger
        self.paused        = False
        self.running       = True
        self.latest_info: dict | None = None
        self.latest_pos    = (0, 0)
        self.info_lock     = threading.Lock()
        self.flash_until   = 0.0
        self.flash_msg     = ""
        self._last_render_key = None

        # Tk window
        self.root = tk.Tk()
        self.root.title("UI Inspector")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.92)
        self.root.geometry(OVERLAY_GEOMETRY)
        self.root.configure(bg="#111111")

        self.hover_status = tk.StringVar(value="starting...")
        tk.Label(self.root, textvariable=self.hover_status,
                 font=("Consolas", 9), bg="#222222", fg="#bbbbbb",
                 anchor="w", padx=8).pack(fill="x")

        self.text = tk.Text(self.root, font=("Consolas", 10),
                            bg="#111111", fg="#e6e6e6", wrap="word",
                            borderwidth=0, highlightthickness=0)
        self.text.pack(fill="both", expand=True, padx=8, pady=(4, 0))
        self.text.configure(state="disabled")

        self.click_status = tk.StringVar(value="no events logged yet")
        tk.Label(self.root, textvariable=self.click_status,
                 font=("Consolas", 9), bg="#222222", fg="#86c986",
                 anchor="w", padx=8).pack(fill="x")

        tk.Label(self.root,
                 text=("Ctrl+Shift+P pause   "
                       "Ctrl+Shift+L log hover   "
                       "Ctrl+Shift+Q quit"),
                 font=("Consolas", 8), bg="#222222", fg="#888888",
                 anchor="w", padx=8).pack(fill="x")

        self.root.update_idletasks()
        if MAKE_CLICK_THROUGH:
            try:
                make_window_click_through(self.root)
            except Exception as e:
                print(f"[warn] couldn't make overlay click-through: {e}")

        # Background poller
        self.poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.poll_thread.start()

        # UI refresh loop
        self.root.after(UI_REFRESH_MS, self._refresh_ui)

    # --- poller (background thread) ---
    def _poll_loop(self):
        while self.running:
            if not self.paused:
                x, y = get_cursor_pos()
                elem = element_at_point(x, y)
                info = describe(elem)
                with self.info_lock:
                    self.latest_info = info
                    self.latest_pos = (x, y)
            time.sleep(POLL_INTERVAL_S)

    # --- UI refresh (main thread) ---
    def _refresh_ui(self):
        with self.info_lock:
            info = self.latest_info
            x, y = self.latest_pos

        self.hover_status.set(
            f"hover @ ({x}, {y})   |   {'PAUSED' if self.paused else 'live'}"
        )

        key = None if info is None else (
            info.get("control_type"), info.get("name"),
            info.get("automation_id"), str(info.get("value")),
            tuple(info.get("rect", [])),
        )
        if key != self._last_render_key:
            self._last_render_key = key
            self._render_body(info)

        # Clear flash message after its time has passed
        if self.flash_msg and time.time() > self.flash_until:
            self.flash_msg = ""
            self.click_status.set("waiting for clicks...")

        if self.running:
            self.root.after(UI_REFRESH_MS, self._refresh_ui)

    def _render_body(self, info: dict | None):
        if info is None:
            text = "(no element under cursor)"
        else:
            order = ("control_type", "localized_control_type", "name",
                     "automation_id", "class_name", "framework",
                     "value", "items", "access_key", "accelerator_key",
                     "help_text", "item_status", "keyboard_focusable",
                     "is_password", "enabled", "visible", "rect", "ts")
            lines = []
            for k in order:
                if k in info:
                    lines.append(f"{k:<22}: {info[k]!r}")
            # Any keys we forgot to order go at the end
            for k, v in info.items():
                if k not in order:
                    lines.append(f"{k:<22}: {v!r}")
            text = "\n".join(lines)

        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", text)
        self.text.configure(state="disabled")

    # --- public API for hotkeys / click listener ---
    def toggle_pause(self):
        self.paused = not self.paused

    def log_current_hover(self):
        with self.info_lock:
            info = self.latest_info
        if info is None:
            self.flash("nothing to log")
            return
        evt = dict(info)
        evt["event"] = "manual_log"
        self.logger.write(evt)
        self.flash(f"manual log: {evt.get('name') or evt.get('control_type')!r}")

    def report_click(self, evt: dict):
        name = evt.get("name") or evt.get("control_type") or "(no element)"
        self.flash(f"{evt['event']} {evt['button']}: {name!r}")

    def flash(self, msg: str, hold_s: float = 1.5):
        self.flash_msg   = msg
        self.flash_until = time.time() + hold_s
        # Schedule on UI thread to avoid races
        self.root.after(0, lambda: self.click_status.set(msg))

    def shutdown(self):
        self.running = False
        self.root.after(0, self.root.destroy)


# -------- Listeners ----------------------------------------------------------

def make_mouse_listener(inspector: HoverInspector, logger: JsonlLogger):
    def on_click(x, y, button, pressed):
        if not pressed:
            return
        elem = element_at_point(x, y)
        info = describe(elem) or {}
        evt = dict(info)
        evt["event"]   = "click"
        evt["button"]  = str(button)
        evt["mouse_x"] = x
        evt["mouse_y"] = y
        logger.write(evt)
        inspector.report_click(evt)
    listener = mouse.Listener(on_click=on_click)
    listener.daemon = True
    return listener


def make_hotkey_listener(inspector: HoverInspector):
    listener = keyboard.GlobalHotKeys({
        "<ctrl>+<shift>+p": inspector.toggle_pause,
        "<ctrl>+<shift>+l": inspector.log_current_hover,
        "<ctrl>+<shift>+q": inspector.shutdown,
    })
    listener.daemon = True
    return listener


# -------- main ---------------------------------------------------------------

def main():
    print(f"Logging to: {LOG_PATH}")
    print("Hotkeys:")
    print("  Ctrl+Shift+P   pause / resume hover")
    print("  Ctrl+Shift+L   log current hover (no click)")
    print("  Ctrl+Shift+Q   quit and write summary")
    print()

    logger = JsonlLogger(LOG_PATH)
    inspector = HoverInspector(logger)

    mouse_listener  = make_mouse_listener(inspector, logger)
    hotkey_listener = make_hotkey_listener(inspector)
    mouse_listener.start()
    hotkey_listener.start()

    try:
        inspector.root.mainloop()
    finally:
        inspector.running = False
        try:    mouse_listener.stop()
        except: pass
        try:    hotkey_listener.stop()
        except: pass

        summary = logger.summary()
        SUMMARY_PATH.write_text(summary, encoding="utf-8")
        print()
        print(summary)
        print()
        print(f"Log:     {LOG_PATH}")
        print(f"Summary: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()