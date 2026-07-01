import base64
import csv
import ctypes
import hashlib
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import ipaddress
import zipfile
import ssl
import webbrowser
from xml.sax.saxutils import escape
from pathlib import Path
from tkinter import BOTH, END, LEFT, RIGHT, VERTICAL, BooleanVar, Canvas, Listbox, PhotoImage, StringVar, Text, Tk, filedialog, messagebox, Toplevel, Label
from tkinter import font as tkfont
from tkinter import ttk

try:
    import winreg
except ImportError:  # pragma: no cover
    winreg = None


ROOT = Path(__file__).resolve().parent
CFG = ROOT / "config"
DESIGN_REF = ROOT / "docs" / "design-references"
SETTINGS_PATH = ROOT / "settings.json"
API_KEYS_PATH = ROOT / "api_keys.json"
BRAND_LOGO_LIGHT_PATH = ROOT / "assets" / "brand" / "logo_light.png"
BRAND_LOGO_DARK_PATH = ROOT / "assets" / "brand" / "logo_dark.png"
BRAND_LOGO_AMOLED_PATH = ROOT / "assets" / "brand" / "logo_amoled.png"
BRAND_LOGO_CYBERPUNK_PATH = ROOT / "assets" / "brand" / "logo_cyberpunk.png"
BRAND_ICON_LIGHT_PATH = ROOT / "assets" / "brand" / "icon_light.png"
BRAND_ICON_DARK_PATH = ROOT / "assets" / "brand" / "icon_dark.png"
BRAND_ICON_AMOLED_PATH = ROOT / "assets" / "brand" / "icon_amoled.png"
BRAND_ICON_CYBERPUNK_PATH = ROOT / "assets" / "brand" / "icon_cyberpunk.png"
START2_PATH = ROOT / "assets" / "start" / "start2.bin"
PROFILE_SETUP_PATH = ROOT / "tools" / "powershell-profile" / "setup.ps1"
APP_NAME = "UsefulWindowsUtils"
APP_VERSION = "1.0.1"
API_KEY_NAMES = ("vt_key", "tf_key", "otx_key", "pd_key", "ha_key")
C2_SOURCES = ("ThreatFox", "URLhaus", "MalwareBazaar", "AlienVault OTX", "Pulsedive", "Hybrid Analysis")
C2_KEY = {
    "ThreatFox": "tf_key",
    "URLhaus": "tf_key",
    "MalwareBazaar": "tf_key",
    "AlienVault OTX": "otx_key",
    "Pulsedive": "pd_key",
    "Hybrid Analysis": "ha_key",
}
DESIGN_REFERENCE_FILES = (
    DESIGN_REF / "logo-light.png",
    DESIGN_REF / "logo-dark.png",
    DESIGN_REF / "logo-amoled.png",
    DESIGN_REF / "logo-cyberpunk.png",
    DESIGN_REF / "ui-light.png",
    DESIGN_REF / "ui-dark.png",
    DESIGN_REF / "ui-amoled.png",
    DESIGN_REF / "ui-cyberpunk.png",
    DESIGN_REF / "controls-light.png",
    DESIGN_REF / "controls-dark.png",
    DESIGN_REF / "controls-amoled.png",
    DESIGN_REF / "controls-cyberpunk.png",
    DESIGN_REF / "usefulwindowsutils_ui_redesign_codex_brief.md",
)
BUNDLED_FILES = (
    CFG / "applications.json",
    CFG / "dns.json",
    CFG / "feature.json",
    CFG / "offline-references.json",
    CFG / "presets.json",
    CFG / "tweaks.json",
    CFG / "win11debloat-apps.json",
    BRAND_LOGO_LIGHT_PATH,
    BRAND_LOGO_DARK_PATH,
    BRAND_LOGO_AMOLED_PATH,
    BRAND_LOGO_CYBERPUNK_PATH,
    BRAND_ICON_LIGHT_PATH,
    BRAND_ICON_DARK_PATH,
    BRAND_ICON_AMOLED_PATH,
    BRAND_ICON_CYBERPUNK_PATH,
    START2_PATH,
    PROFILE_SETUP_PATH,
    *DESIGN_REFERENCE_FILES,
)

TRANSLATIONS = {
    "Spanish": {
        "Apps": "Aplicaciones",
        "Installed": "Instalado",
        "Windows Tweaks": "Ajustes",
        "Features": "Características",
        "Security": "Seguridad",
        "Settings": "Ajustes",
        "About": "Acerca de",
        "Ready": "Listo",
        "Install Selected": "Instalar Seleccionado",
        "Upgrade Selected": "Actualizar Seleccionado"
    },
    "French": {
        "Apps": "Applications",
        "Installed": "Installé",
        "Windows Tweaks": "Modifications",
        "Features": "Fonctionnalités",
        "Security": "Sécurité",
        "Settings": "Paramètres",
        "About": "À propos",
        "Ready": "Prêt",
        "Install Selected": "Installer la sélection",
        "Upgrade Selected": "Mettre à niveau"
    },
    "Russian": {
        "Apps": "Приложения",
        "Installed": "Установлено",
        "Windows Tweaks": "Твики",
        "Features": "Функции",
        "Security": "Безопасность",
        "Settings": "Настройки",
        "About": "О программе",
        "Ready": "Готов",
        "Install Selected": "Установить выбранное",
        "Upgrade Selected": "Обновить выбранное"
    },
    "Hindi": {
        "Apps": "ऐप्स",
        "Installed": "इंस्टॉल किए गए",
        "Windows Tweaks": "विंडोज बदलाव",
        "Features": "विशेषताएं",
        "Security": "सुरक्षा",
        "Settings": "सेटिंग्स",
        "About": "के बारे में",
        "Ready": "तैयार",
        "Install Selected": "चयनित इंस्टॉल करें",
        "Upgrade Selected": "चयनित अपग्रेड करें"
    }
}

THEMES = {
    "Light": {
        "background": "#F8FAFC", "surface": "#FFFFFF", "surface_subtle": "#F1F5F9", "surface_elevated": "#FFFFFF", "surface_pressed": "#EAF2FF",
        "text": "#0F172A", "text_muted": "#64748B", "text_subtle": "#94A3B8", "border": "#E2E8F0", "border_strong": "#CBD5E1",
        "primary": "#0A84FF", "primary_hover": "#0072E5", "primary_pressed": "#005FBF", "primary_soft": "#E7F2FF",
        "teal": "#00B8A9", "violet": "#7C3AED", "success": "#10B981", "success_soft": "#E8F8F2",
        "warning": "#F59E0B", "warning_soft": "#FFF7E6", "danger": "#EF4444", "danger_soft": "#FEECEC",
        "disabled_bg": "#F1F5F9", "disabled_text": "#A3AAB8", "focus_ring": "#0A84FF", "shadow": "#0F172A22",
        "log": "#0B1220", "log_text": "#E2E8F0",
    },
    "Dark": {
        "background": "#0F141C", "surface": "#111827", "surface_subtle": "#162032", "surface_elevated": "#1B2637", "surface_pressed": "#1E3350",
        "text": "#E2E8F0", "text_muted": "#94A3B8", "text_subtle": "#64748B", "border": "#2E3A4C", "border_strong": "#3B4A60",
        "primary": "#0D6EFD", "primary_hover": "#2384FF", "primary_pressed": "#0A58CA", "primary_soft": "#102A4D",
        "teal": "#00B8A9", "violet": "#7C3AED", "success": "#10B981", "success_soft": "#0B2A22",
        "warning": "#F59E0B", "warning_soft": "#2D2108", "danger": "#EF4444", "danger_soft": "#2A1010",
        "disabled_bg": "#1A202C", "disabled_text": "#64748B", "focus_ring": "#0D6EFD", "shadow": "#00000066",
        "log": "#090D14", "log_text": "#D7E3F1",
    },
    "AMOLED": {
        "background": "#000000", "surface": "#050505", "surface_subtle": "#0A0A0A", "surface_elevated": "#101010", "surface_pressed": "#111A24",
        "text": "#F8FAFC", "text_muted": "#A1A1AA", "text_subtle": "#71717A", "border": "#242424", "border_strong": "#383838",
        "primary": "#0A84FF", "primary_hover": "#2994FF", "primary_pressed": "#006AD6", "primary_soft": "#061A33",
        "teal": "#00D1C1", "violet": "#8B5CF6", "success": "#22C55E", "success_soft": "#061A10",
        "warning": "#FBBF24", "warning_soft": "#1C1404", "danger": "#F43F5E", "danger_soft": "#21060B",
        "disabled_bg": "#111111", "disabled_text": "#525252", "focus_ring": "#0A84FF", "shadow": "#000000",
        "log": "#000000", "log_text": "#F8FAFC",
    },
    "Cyberpunk": {
        "background": "#050816", "surface": "#0B1024", "surface_subtle": "#101735", "surface_elevated": "#111936", "surface_pressed": "#172554",
        "text": "#E2F0FF", "text_muted": "#9CA3D6", "text_subtle": "#64748B", "border": "#22304A", "border_strong": "#334155",
        "primary": "#00C8FF", "primary_hover": "#33D6FF", "primary_pressed": "#0099CC", "primary_soft": "#06283A",
        "teal": "#00E8D1", "violet": "#9D4EDD", "magenta": "#FF2BD6", "success": "#00E8A2", "success_soft": "#04251C",
        "warning": "#FFB020", "warning_soft": "#2A1700", "danger": "#FF3B5C", "danger_soft": "#2A0610",
        "disabled_bg": "#111827", "disabled_text": "#4B5563", "focus_ring": "#00C8FF", "glow_cyan": "#00C8FF88", "glow_magenta": "#FF2BD688", "shadow": "#00000099",
        "log": "#030611", "log_text": "#DDF7FF",
    },
}


def _with_legacy_aliases(tokens):
    merged = tokens.copy()
    merged.update({
        "bg": tokens["background"],
        "panel": tokens["surface"],
        "glass": tokens["surface_subtle"],
        "hover": tokens["surface_pressed"],
        "pressed": tokens["primary_pressed"],
        "muted": tokens["text_muted"],
        "line": tokens["border"],
        "accent": tokens["primary"],
        "green": tokens["success"],
        "red": tokens["danger"],
    })
    return merged


THEMES = {name: _with_legacy_aliases(tokens) for name, tokens in THEMES.items()}
COLORS = THEMES["Light"].copy()


def set_colors(theme):
    COLORS.clear()
    COLORS.update(THEMES.get(theme, THEMES["Light"]))


def brand_logo_path(theme):
    return {
        "Light": BRAND_LOGO_LIGHT_PATH,
        "Dark": BRAND_LOGO_DARK_PATH,
        "AMOLED": BRAND_LOGO_AMOLED_PATH,
        "Cyberpunk": BRAND_LOGO_CYBERPUNK_PATH,
    }.get(theme, BRAND_LOGO_LIGHT_PATH)


def brand_icon_path(theme):
    return {
        "Light": BRAND_ICON_LIGHT_PATH,
        "Dark": BRAND_ICON_DARK_PATH,
        "AMOLED": BRAND_ICON_AMOLED_PATH,
        "Cyberpunk": BRAND_ICON_CYBERPUNK_PATH,
    }.get(theme, BRAND_ICON_LIGHT_PATH)


def load_json(name):
    with open(CFG / name, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def norm_pkg(value):
    value = (value or "").strip()
    return value if value.lower() not in {"", "na", "n/a", "none", "null"} else ""


def run_capture(cmd):
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, errors="replace")


def bundled_path(value, default="outputs"):
    path = Path(value or default)
    return path if path.is_absolute() else ROOT / path


def is_inside_root(path):
    try:
        Path(path).resolve().relative_to(ROOT)
        return True
    except ValueError:
        return False


def check_bundled_files():
    missing = [str(path.relative_to(ROOT)) for path in BUNDLED_FILES if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing bundled files: " + ", ".join(missing))


class ThemedScrollbar(Canvas):
    def __init__(self, master, command):
        super().__init__(master, width=14, highlightthickness=0, borderwidth=0, background=COLORS["glass"], cursor="hand2")
        self.command = command
        self.first = 0.0
        self.last = 1.0
        self.bind("<Button-1>", self._jump)
        self.bind("<B1-Motion>", self._jump)
        self.bind("<Configure>", lambda _e: self._draw())

    def set(self, first, last):
        self.first, self.last = float(first), float(last)
        self._draw()

    def _draw(self):
        self.delete("all")
        h = max(1, self.winfo_height())
        top = max(3, int(self.first * h))
        bottom = min(h - 3, max(top + 24, int(self.last * h)))
        self.configure(background=COLORS["glass"])
        _rounded_rect(self, 2, 2, 12, h - 2, 6, fill=COLORS["surface_subtle"], outline=COLORS["border"], width=1)
        _rounded_rect(self, 4, top, 10, bottom, 4, fill=COLORS["primary"], outline=COLORS["primary_hover"], width=1)

    def _jump(self, event):
        h = max(1, self.winfo_height())
        span = max(0.05, self.last - self.first)
        self.command("moveto", max(0, min(1 - span, (event.y / h) - span / 2)))


class ScrollFrame(ttk.Frame):
    active = None

    def __init__(self, master):
        super().__init__(master)
        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0, background=COLORS["panel"])
        self.inner = ttk.Frame(self.canvas, style="Panel.TFrame")
        self.scroll = ThemedScrollbar(self, self.canvas.yview)
        self.window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scroll.pack(side=RIGHT, fill="y")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window, width=e.width))
        self.canvas.bind("<Enter>", self._activate)
        self.inner.bind("<Enter>", self._activate)
        self.canvas.bind_all("<MouseWheel>", self._wheel, add="+")
        self.canvas.bind_all("<Button-4>", self._wheel, add="+")
        self.canvas.bind_all("<Button-5>", self._wheel, add="+")

    def _activate(self, _event=None):
        ScrollFrame.active = self

    def _wheel(self, event):
        if not self._owns_pointer(event):
            return
        if getattr(event, "num", None) == 4:
            delta = -3
        elif getattr(event, "num", None) == 5:
            delta = 3
        else:
            delta = int(-event.delta / 120) or (-1 if event.delta > 0 else 1)
        self.canvas.yview_scroll(delta, "units")

    def _owns_pointer(self, event):
        try:
            target = self.winfo_containing(event.x_root, event.y_root)
        except KeyError:
            return False
        while target:
            if target in {self, self.canvas, self.inner}:
                return True
            target = getattr(target, "master", None)
        return False


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        self.widget.bind("<Enter>", self.enter, add="+")
        self.widget.bind("<Leave>", self.leave, add="+")

    def enter(self, event=None):
        if self.tip or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + getattr(self.widget, "winfo_height", lambda: 20)()
        self.tip = Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        # Keep it on top
        self.tip.attributes("-topmost", True)
        label = Label(self.tip, text=self.text, background=COLORS["panel"], foreground=COLORS["text"], relief="solid", borderwidth=1, padx=6, pady=4, font=("Segoe UI", 9), wraplength=400, justify="left")
        label.pack()

    def leave(self, event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None


_TTK_BUTTON = ttk.Button
_TTK_CHECKBUTTON = ttk.Checkbutton
_TTK_RADIOBUTTON = ttk.Radiobutton
_TTK_PROGRESSBAR = ttk.Progressbar


def _rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)


class RoundedButton(Canvas):
    def __init__(self, master, text="", command=None, style=None, width=None, state="normal", **kwargs):
        self.text = text or ""
        self.command = command
        self.style_name = style or self._style_from_text(self.text)
        self.state = state
        self.hover = False
        self.down = False
        self.char_width = width
        w = max(40, int(width) * 9 if width else max(82, len(self.text) * 8 + 44))
        super().__init__(master, width=w, height=36, highlightthickness=0, borderwidth=0, background=COLORS["background"], cursor="hand2", **{k: v for k, v in kwargs.items() if k in {"name"}})
        self.bind("<Configure>", lambda _e: self._draw())
        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        self.bind("<ButtonPress-1>", self._press)
        self.bind("<ButtonRelease-1>", self._release)
        self.bind("<Return>", lambda _e: self.invoke())
        self.bind("<space>", lambda _e: self.invoke())
        self._draw()

    @staticmethod
    def _style_from_text(text):
        text = text.lower()
        if any(word in text for word in ("uninstall", "remove", "delete", "reset", "debloat", "clear files", "clear dashboard", "overwrite")):
            return "Danger.TButton"
        if any(word in text for word in ("install selected", "upgrade selected", "apply selected", "run selected", "create iso", "move files", "collect data", "save settings", "save path", "search", "confirm", "lookup", "save")):
            return "Accent.TButton"
        return "Secondary.TButton"

    def _palette(self):
        disabled = str(self.state) == "disabled"
        style = self.style_name or "Secondary.TButton"
        if disabled:
            return COLORS["disabled_bg"], COLORS["disabled_text"], COLORS["border"]
        if style in ("Accent.TButton", "Primary.TButton"):
            fill = COLORS["primary_pressed"] if self.down else COLORS["primary_hover"] if self.hover else COLORS["primary"]
            return fill, "#FFFFFF", COLORS["primary"]
        if style in ("Danger.TButton", "Destructive.TButton"):
            fill = COLORS["danger_soft"] if self.down else COLORS["danger"]
            return fill, "#FFFFFF", COLORS["danger"]
        if style == "DangerOutline.TButton":
            return COLORS["surface_pressed"] if self.hover else COLORS["surface"], COLORS["danger"], COLORS["danger"]
        if style == "Nav.TButton":
            return COLORS["surface_pressed"] if self.hover else COLORS["surface"], COLORS["text"], COLORS["border"]
        if style in ("Subtle.TButton", "Icon.TButton"):
            return COLORS["surface_pressed"] if self.hover or self.down else COLORS["background"], COLORS["text"], COLORS["background"]
        return COLORS["surface_pressed"] if self.hover or self.down else COLORS["surface"], COLORS["text"], COLORS["border"]

    def _draw(self):
        self.delete("all")
        fill, fg, border = self._palette()
        w, h = max(1, self.winfo_width()), max(1, self.winfo_height())
        bg = COLORS["surface"] if self.style_name not in ("Subtle.TButton",) else COLORS["background"]
        Canvas.configure(self, background=bg)
        _rounded_rect(self, 1, 1, w - 1, h - 1, 9, fill=fill, outline=border, width=1)
        if self.style_name in ("Accent.TButton", "Primary.TButton") and COLORS.get("glow_cyan"):
            _rounded_rect(self, 2, 2, w - 2, h - 2, 9, fill="", outline=COLORS["primary"], width=1)
        size = 10
        while size > 8 and tkfont.Font(family="Segoe UI Variable Text", size=size, weight="bold").measure(self.text.replace("\t", "  ")) > w - 20:
            size -= 1
        font = ("Segoe UI Variable Text", size, "bold")
        if self.style_name == "Nav.TButton" and "\t" in self.text:
            icon, label = self.text.split("\t", 1)
            self.create_text(18, h // 2, text=icon, fill=fg, anchor="center", font=("Segoe UI Symbol", size + 1))
            self.create_text(44, h // 2, text=label, fill=fg, anchor="w", font=font)
        else:
            anchor = "w" if self.style_name == "Nav.TButton" else "center"
            x = 44 if self.style_name == "Nav.TButton" else w // 2
            self.create_text(x, h // 2, text=self.text, fill=fg, anchor=anchor, font=font, width=max(20, w - x - 8 if anchor == "w" else w - 18))

    def _enter(self, _event=None):
        self.hover = True
        self._draw()

    def _leave(self, _event=None):
        self.hover = self.down = False
        self._draw()

    def _press(self, _event=None):
        self.down = True
        self._draw()

    def _release(self, event=None):
        was_down = self.down
        self.down = False
        self._draw()
        if was_down and self.command and str(self.state) != "disabled":
            self.command()

    def invoke(self):
        if self.command and str(self.state) != "disabled":
            return self.command()

    def configure(self, cnf=None, **kwargs):
        opts = {}
        if cnf:
            opts.update(cnf)
        opts.update(kwargs)
        for key in list(opts):
            if key == "text":
                self.text = opts.pop(key) or ""
                if not self.char_width:
                    Canvas.configure(self, width=max(82, len(self.text) * 8 + 44))
            elif key == "command":
                self.command = opts.pop(key)
            elif key == "style":
                self.style_name = opts.pop(key)
            elif key == "state":
                self.state = opts.pop(key)
            elif key in {"foreground", "background"}:
                opts.pop(key)
        if opts:
            super().configure(**opts)
        self._draw()

    config = configure

    def cget(self, key):
        if key == "text":
            return self.text
        if key == "style":
            return self.style_name
        if key == "state":
            return self.state
        return super().cget(key)

    def keys(self):
        return list(super().keys()) + ["text", "style", "state"]


ttk.Button = RoundedButton


class ModernCheckbutton(Canvas):
    def __init__(
        self,
        master,
        text="",
        variable=None,
        command=None,
        style=None,
        state="normal",
        onvalue=True,
        offvalue=False,
        **kwargs,
    ):
        self.text = text or ""
        self.variable = variable or BooleanVar(master=master, value=False)
        self.command = command
        self.style_name = style or "TCheckbutton"
        self.state = state
        self.onvalue = onvalue
        self.offvalue = offvalue
        self.hover = False
        self._trace_id = None
        width = kwargs.pop("width", None)
        super().__init__(
            master,
            width=self._desired_width(width),
            height=self._desired_height(),
            highlightthickness=0,
            borderwidth=0,
            background=self._bg(),
            cursor="hand2",
            **{k: v for k, v in kwargs.items() if k in {"name"}},
        )
        self.bind("<Button-1>", self._click)
        self.bind("<Enter>", lambda _e: self._set_hover(True))
        self.bind("<Leave>", lambda _e: self._set_hover(False))
        self.bind("<Configure>", lambda _e: self._draw())
        self._watch_variable()
        self._draw()

    def _desired_width(self, requested=None):
        if requested:
            return max(28, int(requested) * 8)
        if not self.text:
            return 28
        return min(760, max(130, len(self.text) * 7 + 40))

    def _desired_height(self):
        width = max(80, self._desired_width() - 36)
        lines = max(1, (len(self.text) * 7) // width + 1)
        return max(28, min(64, lines * 16 + 10))

    def _bg(self):
        try:
            parent_style = self.master.cget("style") if "style" in self.master.keys() else ""
        except Exception:
            parent_style = ""
        if "Panel" in (self.style_name or "") or "Panel" in parent_style:
            return COLORS["surface"]
        return COLORS["background"]

    def _checked(self):
        try:
            return self.variable.get() == self.onvalue
        except Exception:
            return bool(self.variable.get())

    def _label_color(self):
        if str(self.state) == "disabled":
            return COLORS["disabled_text"]
        if "Risk" in (self.style_name or ""):
            return COLORS["danger"]
        if "Green" in (self.style_name or ""):
            return COLORS["success"]
        return COLORS["text"]

    def _watch_variable(self):
        if self._trace_id:
            try:
                self.variable.trace_remove("write", self._trace_id)
            except Exception:
                pass
        try:
            self._trace_id = self.variable.trace_add("write", lambda *_: self._draw())
        except Exception:
            self._trace_id = None

    def _set_hover(self, value):
        self.hover = value
        self._draw()

    def _click(self, _event=None):
        if str(self.state) == "disabled":
            return
        self.variable.set(self.offvalue if self._checked() else self.onvalue)
        self._draw()
        if self.command:
            self.command()

    def _draw_box(self, x1, y1, x2, y2, checked, disabled):
        if checked:
            fill = COLORS["disabled_bg"] if disabled else COLORS["primary"]
            border = COLORS["disabled_text"] if disabled else COLORS["primary_hover"]
        else:
            fill = self._bg()
            border = COLORS["disabled_text"] if disabled else COLORS["border_strong"]
        _rounded_rect(self, x1, y1, x2, y2, 5, fill=fill, outline=border, width=1)
        if checked:
            self.create_line(x1 + 5, y1 + 11, x1 + 9, y1 + 15, x2 - 5, y1 + 6, fill="#FFFFFF", width=2, capstyle="round", joinstyle="round")
        elif self.hover and not disabled:
            _rounded_rect(self, x1, y1, x2, y2, 5, fill="", outline=COLORS["focus_ring"], width=1)

    def _draw(self):
        self.delete("all")
        disabled = str(self.state) == "disabled"
        bg = self._bg()
        Canvas.configure(self, background=bg)
        checked = self._checked()
        self._draw_box(3, 5, 23, 25, checked, disabled)
        if self.text:
            self.create_text(32, 15, text=self.text, fill=self._label_color(), anchor="w", font=("Segoe UI Variable Text", 10), width=max(80, self.winfo_width() - 36))

    def configure(self, cnf=None, **kwargs):
        opts = {}
        if cnf:
            opts.update(cnf)
        opts.update(kwargs)
        redraw = False
        for key in list(opts):
            if key == "text":
                self.text = opts.pop(key) or ""
                Canvas.configure(self, width=self._desired_width(), height=self._desired_height())
                redraw = True
            elif key == "variable":
                self.variable = opts.pop(key)
                self._watch_variable()
                redraw = True
            elif key == "command":
                self.command = opts.pop(key)
            elif key == "style":
                self.style_name = opts.pop(key) or "TCheckbutton"
                redraw = True
            elif key == "state":
                self.state = opts.pop(key)
                redraw = True
            elif key == "onvalue":
                self.onvalue = opts.pop(key)
                redraw = True
            elif key == "offvalue":
                self.offvalue = opts.pop(key)
                redraw = True
            elif key in {"foreground", "background", "font", "padding"}:
                opts.pop(key)
        if opts:
            Canvas.configure(self, **opts)
        self._draw()

    config = configure

    def cget(self, key):
        if key == "text":
            return self.text
        if key == "style":
            return self.style_name
        if key == "state":
            return self.state
        return Canvas.cget(self, key)

    def keys(self):
        return list(Canvas.keys(self)) + ["text", "style", "state", "variable", "command"]


class ModernRadiobutton(ModernCheckbutton):
    def __init__(self, master, text="", variable=None, value=None, command=None, style=None, state="normal", **kwargs):
        self.value = value if value is not None else text
        super().__init__(master, text=text, variable=variable or StringVar(master=master), command=command, style=style or "TRadiobutton", state=state, **kwargs)

    def _checked(self):
        try:
            return self.variable.get() == self.value
        except Exception:
            return False

    def _click(self, _event=None):
        if str(self.state) == "disabled":
            return
        self.variable.set(self.value)
        self._draw()
        if self.command:
            self.command()

    def _draw_box(self, x1, y1, x2, y2, checked, disabled):
        border = COLORS["disabled_text"] if disabled else COLORS["primary"] if checked else COLORS["border_strong"]
        fill = self._bg()
        self.create_oval(x1, y1, x2, y2, fill=fill, outline=border, width=2)
        if checked:
            self.create_oval(x1 + 6, y1 + 6, x2 - 6, y2 - 6, fill=COLORS["primary"], outline="")
        elif self.hover and not disabled:
            self.create_oval(x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill="", outline=COLORS["focus_ring"], width=1)

    def configure(self, cnf=None, **kwargs):
        opts = {}
        if cnf:
            opts.update(cnf)
        opts.update(kwargs)
        if "value" in opts:
            self.value = opts.pop("value")
        return super().configure(opts)


ttk.Checkbutton = ModernCheckbutton
ttk.Radiobutton = ModernRadiobutton


class ToggleSwitch(Canvas):
    def __init__(self, master, variable, command=None, state="normal"):
        super().__init__(master, width=50, height=28, highlightthickness=0, borderwidth=0, background=COLORS["surface"], cursor="hand2")
        self.variable = variable
        self.command = command
        self.state = state
        self.hover = False
        self.bind("<Button-1>", self._toggle)
        self.bind("<Enter>", lambda _e: self._set_hover(True))
        self.bind("<Leave>", lambda _e: self._set_hover(False))
        self.bind("<Configure>", lambda _e: self._draw())
        self._draw()

    def _set_hover(self, value):
        self.hover = value
        self._draw()

    def _toggle(self, _event=None):
        if str(self.state) == "disabled":
            return
        self.variable.set(not self.variable.get())
        self._draw()
        if self.command:
            self.command()

    def _draw(self):
        self.delete("all")
        try:
            parent_style = self.master.cget("style") if "style" in self.master.keys() else ""
        except Exception:
            parent_style = ""
        Canvas.configure(self, background=COLORS["surface"] if "Panel" in parent_style else COLORS["background"])
        on = bool(self.variable.get())
        disabled = str(self.state) == "disabled"
        track = COLORS["disabled_bg"] if disabled else COLORS["primary"] if on else COLORS["surface_subtle"]
        border = COLORS["disabled_text"] if disabled else COLORS["primary"] if on else COLORS["border_strong"]
        knob = COLORS["disabled_text"] if disabled else "#FFFFFF" if on else COLORS["text"]
        _rounded_rect(self, 1, 3, 49, 25, 13, fill=track, outline=border, width=1)
        x = 36 if on else 14
        self.create_oval(x - 9, 5, x + 9, 23, fill=knob, outline=COLORS["border"])
        if self.hover and not disabled:
            _rounded_rect(self, 1, 3, 49, 25, 13, fill="", outline=COLORS["focus_ring"], width=1)

    def configure(self, cnf=None, **kwargs):
        opts = {}
        if cnf:
            opts.update(cnf)
        opts.update(kwargs)
        if "state" in opts:
            self.state = opts.pop("state")
        if opts:
            Canvas.configure(self, **opts)
        self._draw()

    config = configure


class ThemedProgressbar(Canvas):
    def __init__(self, master, mode="determinate", length=None, maximum=100, value=0, style=None, **kwargs):
        width = int(length or kwargs.pop("width", 280))
        super().__init__(master, width=width, height=14, highlightthickness=0, borderwidth=0, background=COLORS["background"])
        self.mode = mode
        self.maximum = max(1, float(maximum))
        self.value = float(value)
        self._running = False
        self._phase = 0
        self.bind("<Configure>", lambda _e: self._draw())
        self._draw()

    def _draw(self):
        self.delete("all")
        w, h = max(1, self.winfo_width()), max(1, self.winfo_height())
        Canvas.configure(self, background=COLORS["background"])
        _rounded_rect(self, 1, 3, w - 1, h - 3, 6, fill=COLORS["surface_subtle"], outline=COLORS["border"], width=1)
        if self.mode == "indeterminate" and self._running:
            span = max(42, w // 4)
            x = (self._phase % max(1, w + span)) - span
            _rounded_rect(self, max(2, x), 4, min(w - 2, x + span), h - 4, 5, fill=COLORS["primary"], outline="", width=0)
        else:
            frac = max(0, min(1, self.value / self.maximum))
            if frac:
                _rounded_rect(self, 2, 4, max(8, int((w - 4) * frac)), h - 4, 5, fill=COLORS["primary"], outline="", width=0)

    def _tick(self):
        if not self._running:
            return
        self._phase += 12
        self._draw()
        self.after(35, self._tick)

    def start(self, interval=None):
        if self._running:
            return
        self._running = True
        self.mode = "indeterminate"
        self._tick()

    def stop(self):
        self._running = False
        self._draw()

    def configure(self, cnf=None, **kwargs):
        opts = {}
        if cnf:
            opts.update(cnf)
        opts.update(kwargs)
        for key in list(opts):
            if key == "mode":
                self.mode = opts.pop(key)
            elif key == "maximum":
                self.maximum = max(1, float(opts.pop(key)))
            elif key == "value":
                self.value = float(opts.pop(key))
            elif key in {"style", "length"}:
                if key == "length":
                    Canvas.configure(self, width=int(opts[key]))
                opts.pop(key)
        if opts:
            Canvas.configure(self, **opts)
        self._draw()

    config = configure

    def cget(self, key):
        if key == "mode":
            return self.mode
        if key == "maximum":
            return self.maximum
        if key == "value":
            return self.value
        return Canvas.cget(self, key)

    def keys(self):
        return list(Canvas.keys(self)) + ["mode", "maximum", "value", "style", "length"]


ttk.Progressbar = ThemedProgressbar


BUTTON_STYLES = {
    "primary": "Primary.TButton",
    "secondary": "Secondary.TButton",
    "subtle": "Subtle.TButton",
    "ghost": "Subtle.TButton",
    "danger": "Destructive.TButton",
    "destructive": "Destructive.TButton",
    "danger_outline": "DangerOutline.TButton",
    "icon": "Icon.TButton",
}


def ThemedButton(parent, text="", variant="secondary", command=None, **kwargs):
    return ttk.Button(parent, text=text, command=command, style=BUTTON_STYLES.get(variant, "Secondary.TButton"), **kwargs)


def Card(parent, title=None, subtitle=None, variant="outlined", padding=16):
    frame = ttk.Frame(parent, style=f"Card.{variant.title()}.TFrame", padding=padding)
    if title:
        ttk.Label(frame, text=title, style="Section.TLabel").pack(anchor="w")
    if subtitle:
        ttk.Label(frame, text=subtitle, style="Muted.Panel.TLabel", wraplength=920).pack(anchor="w", pady=(2, 0))
    return frame


def SectionHeader(parent, title, subtitle=None):
    frame = ttk.Frame(parent)
    ttk.Label(frame, text=title, style="Section.TLabel").pack(anchor="w")
    if subtitle:
        ttk.Label(frame, text=subtitle, style="Muted.TLabel", wraplength=920).pack(anchor="w", pady=(2, 0))
    return frame


def Badge(parent, text, variant="neutral"):
    return ttk.Label(parent, text=text, style=f"Badge.{variant.title()}.TLabel")


class RoundedInputShell(Canvas):
    def __init__(self, master, width=240, height=34):
        super().__init__(master, width=width, height=height, highlightthickness=0, borderwidth=0, background=COLORS["background"])
        self.focused = False
        self.bind("<Configure>", lambda _e: self._draw())

    def set_focused(self, value):
        self.focused = value
        self._draw()

    def _draw(self):
        self.delete("shell")
        w, h = max(1, self.winfo_width()), max(1, self.winfo_height())
        try:
            parent_style = self.master.cget("style") if "style" in self.master.keys() else ""
        except Exception:
            parent_style = ""
        bg = COLORS["surface"] if "Panel" in parent_style else COLORS["background"]
        Canvas.configure(self, background=bg)
        border = COLORS["focus_ring"] if self.focused else COLORS["border_strong"]
        _rounded_rect(self, 1, 1, w - 1, h - 1, 8, fill=COLORS["surface"], outline=border, width=1, tags="shell")
        self.itemconfigure("search_icon", fill=COLORS["muted"])


def SearchEntry(parent, textvariable, command=None, width=32):
    frame = RoundedInputShell(parent, width=max(180, width * 8 + 36), height=36)
    entry = ttk.Entry(frame, textvariable=textvariable, width=width, style="Search.TEntry")
    frame.create_text(18, 18, text="⌕", fill=COLORS["muted"], font=("Segoe UI Symbol", 13), tags=("search_icon",))
    frame.create_window(34, 18, window=entry, anchor="w", width=max(120, width * 8 - 4), height=24, tags=("entry_window",))
    entry.bind("<FocusIn>", lambda _e: frame.set_focused(True), add="+")
    entry.bind("<FocusOut>", lambda _e: frame.set_focused(False), add="+")
    if command:
        entry.bind("<KeyRelease>", command)
    return frame, entry


def PasswordEntry(parent, variable):
    frame = ttk.Frame(parent)
    entry = ttk.Entry(frame, textvariable=variable, show="*")
    entry.pack(side=LEFT, fill="x", expand=True)
    shown = BooleanVar(value=False)

    def toggle():
        shown.set(not shown.get())
        entry.configure(show="" if shown.get() else "*")

    ThemedButton(frame, text="Show", variant="subtle", command=toggle).pack(side=LEFT, padx=(6, 0))
    return frame, entry


def ConfirmDialog(title, message, severity="warning"):
    icon = "error" if severity in {"danger", "destructive"} else "warning"
    return messagebox.askyesno(title, message, icon=icon)


class ToastManager:
    def __init__(self, status_label):
        self.status_label = status_label

    def show(self, message, variant="info"):
        self.status_label.configure(text=message, foreground=COLORS.get({"success": "green", "warning": "warning", "danger": "red"}.get(variant, "accent"), COLORS["text"]))


class App:
    def __init__(self):
        check_bundled_files()
        self.root = Tk()
        self.root.withdraw()  # hide window while building UI
        self.root.title(f"{APP_NAME} - Made by Kuljit Singh")
        self.root.geometry("1280x820")
        self.root.minsize(1080, 700)
        self.q = queue.Queue()
        self.settings = self.load_settings()
        self.api_keys = self.load_api_keys()
        self.app_log = []

        system_theme = "Dark"
        if winreg:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                if value == 1:
                    system_theme = "Light"
                winreg.CloseKey(key)
            except Exception:
                pass

        set_colors(system_theme)

        try:
            import sv_ttk
            sv_ttk.set_theme(system_theme.lower())
        except ImportError:
            pass
        try:
            import pywinstyles
            pywinstyles.apply_style(self.root, "mica")
        except Exception:
            pass

        self.root.option_add("*Font", ("Segoe UI Variable Text", 10))

        self.apps = self.load_apps()
        self.tweaks = self.load_tweaks()
        self.tweak_presets = self.load_tweak_presets()
        self.debloat_apps = self.load_debloat_apps()
        self.features = self.load_features()
        self.dns = self.load_dns()
        self.app_vars = {}
        self.tweak_vars = {}
        self.debloat_vars = {}
        self.feature_vars = {}
        self.installed_rows = {}
        self.installed_selected = {}
        self.toggle_widgets = []
        self.vt_cache = {}
        self.c2_indicator_sources = {}
        self.c2_indicator_meta = {}
        self.c2_details = {}
        self._style()
        self._build()
        self.root.after(100, self._drain)
        self.apply_theme(self.settings.get("theme", "Light"), force=True)
        self.root.deiconify()  # show window now that UI is ready

    def _(self, text):
        lang = self.settings.get("language", "English")
        if lang == "English" or lang not in TRANSLATIONS:
            return text
        return TRANSLATIONS[lang].get(text, text)

    def load_settings(self):
        defaults = {
            "theme": "Light",
            "font_scale": "100",
            "language": "English",
            "package_mode": "Winget then Chocolatey",
            "c2_sources": {name: True for name in C2_SOURCES},
            "c2_limits": {name: 100 for name in C2_SOURCES},
            "c2_days": "7",
            "c2_output_dir": "outputs",
        }
        if SETTINGS_PATH.exists():
            try:
                data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
                defaults.update({k: v for k, v in data.items() if k not in API_KEY_NAMES})
            except Exception:
                pass
        c2_dir = bundled_path(defaults.get("c2_output_dir"))
        if not is_inside_root(c2_dir) or not c2_dir.exists():
            defaults["c2_output_dir"] = "outputs"
        if defaults.get("theme") not in THEMES:
            defaults["theme"] = "Light"
        return defaults

    def load_api_keys(self):
        keys = {name: "" for name in API_KEY_NAMES}
        for path in (SETTINGS_PATH, API_KEYS_PATH):
            if path.exists():
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                    keys.update({k: data.get(k, keys[k]) for k in API_KEY_NAMES if data.get(k)})
                except Exception:
                    pass
        return keys

    def load_apps(self):
        raw = load_json("applications.json")
        seen, out = set(), []
        for key, item in raw.items():
            winget, choco = norm_pkg(item.get("winget")), norm_pkg(item.get("choco"))
            ids = {f"w:{winget.lower()}"} if winget else set()
            ids |= {f"c:{x.strip().lower()}" for x in re.split(r"[;,]", choco) if norm_pkg(x)}
            name_key = "n:" + re.sub(r"[^a-z0-9]+", "", item.get("content", "").lower())
            ids.add(name_key)
            if seen & ids or not (winget or choco):
                continue
            seen |= ids
            out.append({
                "key": key,
                "name": item.get("content", key),
                "category": item.get("category", "Other"),
                "winget": winget,
                "choco": choco,
                "source": item.get("source", ""),
                "desc": item.get("description", ""),
                "foss": bool(item.get("foss")),
            })
        for app in [
            {"key": "LabSystemInformer", "name": "System Informer", "category": "Malware Analysis", "winget": "WinsiderSS.SystemInformer", "choco": "systeminformer", "desc": "Advanced process and system monitor", "foss": True},
            {"key": "LabProcmon", "name": "Process Monitor", "category": "Malware Analysis", "winget": "Microsoft.Sysinternals.ProcessMonitor", "choco": "procmon", "desc": "Sysinternals process, registry, and file monitor", "foss": False},
            {"key": "LabWireshark", "name": "Wireshark", "category": "Malware Analysis", "winget": "WiresharkFoundation.Wireshark", "choco": "wireshark", "desc": "Network protocol analyzer", "foss": True},
            {"key": "LabPEStudio", "name": "PE Studio", "category": "Malware Analysis", "winget": "", "choco": "", "portable_zip": "https://www.winitor.com/tools/pestudio/current/pestudio.zip", "install_dir": "PEStudio", "desc": "Portable PE and malware triage tool", "foss": False},
            {"key": "LabIDAFree", "name": "IDA Free", "category": "Malware Analysis", "winget": "Hex-Rays.IDA.Free", "choco": "ida-free", "desc": "Free disassembler", "foss": False},
            {"key": "LabGhidra", "name": "Ghidra", "category": "Malware Analysis", "winget": "NSA.Ghidra", "choco": "ghidra", "desc": "Reverse engineering suite", "foss": True},
            {"key": "LabDIE", "name": "Detect It Easy", "category": "Malware Analysis", "winget": "horsicq.DIE", "choco": "die", "desc": "File type and packer detector", "foss": True},
            {"key": "LabX64Dbg", "name": "x64dbg", "category": "Malware Analysis", "winget": "x64dbg.x64dbg", "choco": "x64dbg.portable", "desc": "Windows debugger", "foss": True},
        ]:
            ids = {f"w:{app['winget'].lower()}"} if app.get("winget") else set()
            ids |= {f"c:{app['choco'].lower()}"} if app.get("choco") else set()
            ids.add("n:" + re.sub(r"[^a-z0-9]+", "", app["name"].lower()))
            if not (seen & ids):
                seen |= ids
                out.append(app)
        return sorted(out, key=lambda x: (x["category"], x["name"].lower()))

    def load_tweaks(self):
        raw = load_json("tweaks.json")
        out = []
        for key, item in raw.items():
            if key == "WPFTweaksDeBloat":
                continue
            if item.get("Type") == "Combobox":
                continue
            cat = {"Essential Tweaks": "Essential", "z__Advanced Tweaks - CAUTION": "Advanced", "Customize Preferences": "Preferences"}.get(item.get("category"), item.get("category", "Other"))
            if cat == "Advanced":
                continue
            out.append({
                "key": key,
                "name": item.get("Content", key),
                "category": cat,
                "desc": item.get("Description", ""),
                "toggle": item.get("Type") == "Toggle" or cat == "Preferences",
                "registry": self.as_list(item.get("registry")),
                "service": self.as_list(item.get("service")),
                "invoke": self.as_list(item.get("InvokeScript")),
                "undo": self.as_list(item.get("UndoScript")),
                "default": any(str(r.get("DefaultState", "")).lower() == "true" for r in self.as_list(item.get("registry"))),
            })
        return sorted(out, key=lambda x: (x["category"], x["name"].lower()))

    def load_tweak_presets(self):
        try:
            data = load_json("presets.json")
            return {k: [str(x) for x in v] for k, v in data.items() if isinstance(v, list) and k.lower() != "advanced"}
        except Exception:
            return {}

    def load_debloat_apps(self):
        try:
            raw = load_json("win11debloat-apps.json")
        except Exception:
            return []
        apps = raw.get("Apps", []) if isinstance(raw, dict) else []
        out = []
        for item in apps:
            appid = str(item.get("AppId", "")).strip()
            if not appid:
                continue
            out.append({
                "name": item.get("FriendlyName", appid),
                "appid": appid,
                "desc": item.get("Description", ""),
                "selected": bool(item.get("SelectedByDefault")),
                "recommendation": item.get("Recommendation", ""),
                "method": item.get("RemovalMethod", "Appx"),
            })
        return sorted(out, key=lambda x: (x["recommendation"], x["name"].lower()))

    def load_features(self):
        raw = load_json("feature.json")
        out = []
        for key, item in raw.items():
            if key == "WPFFeatureInstall":
                continue
            out.append({
                "key": key,
                "name": item.get("Content", key),
                "category": item.get("category", "Features"),
                "desc": item.get("Description", ""),
                "features": self.as_list(item.get("feature")),
                "scripts": self.as_list(item.get("InvokeScript")) + ([item["function"]] if item.get("function") else []),
            })
        return sorted(out, key=lambda x: (x["category"], x["name"].lower()))

    def load_dns(self):
        raw = load_json("dns.json")
        dns = {"Default": {}, "DHCP": {}}
        for name, item in raw.items():
            dns[name] = {"v4": [item.get("Primary"), item.get("Secondary")], "v6": [item.get("Primary6"), item.get("Secondary6")]}
        return dns

    @staticmethod
    def as_list(value):
        if value in (None, ""):
            return []
        return value if isinstance(value, list) else [value]

    def fsize(self, size):
        return max(8, round(size * int(self.settings.get("font_scale", "100")) / 100))

    def _style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        bg, panel, glass = COLORS["background"], COLORS["surface"], COLORS["surface_subtle"]
        elevated = COLORS["surface_elevated"]
        hover = COLORS.get("hover", glass)
        pressed = COLORS.get("pressed", hover)
        disabled_bg = COLORS.get("disabled_bg", glass)
        disabled_text = COLORS.get("disabled_text", COLORS["muted"])
        font_scale = int(self.settings.get("font_scale", "100")) / 100 if hasattr(self, "settings") else 1
        body_size = max(9, int(10 * font_scale))
        small_size = max(8, int(9 * font_scale))
        body_font = ("Segoe UI Variable Text", body_size)
        button_font = ("Segoe UI Variable Text", body_size, "bold")
        heading_font = ("Segoe UI Variable Display", max(14, int(16 * font_scale)), "bold")
        style.configure(".", background=bg, foreground=COLORS["text"], font=body_font)
        style.configure("TFrame", background=bg)
        style.configure("App.TFrame", background=bg)
        style.configure("Surface.TFrame", background=panel)
        style.configure("Panel.TFrame", background=panel, borderwidth=1, relief="solid", bordercolor=COLORS["border"])
        style.configure("PanelInner.TFrame", background=panel)
        style.configure("Search.TFrame", background=glass, borderwidth=1, relief="solid", bordercolor=COLORS["border"])
        style.configure("Card.Outlined.TFrame", background=panel, borderwidth=1, relief="solid", bordercolor=COLORS["border"])
        style.configure("Card.Elevated.TFrame", background=elevated, borderwidth=1, relief="solid", bordercolor=COLORS["border"])
        style.configure("Card.Subtle.TFrame", background=glass, borderwidth=1, relief="solid", bordercolor=COLORS["border"])
        style.configure("Card.Warning.TFrame", background=COLORS["warning_soft"], borderwidth=1, relief="solid", bordercolor=COLORS["warning"])
        style.configure("Card.Danger.TFrame", background=COLORS["danger_soft"], borderwidth=1, relief="solid", bordercolor=COLORS["danger"])
        style.configure("TLabel", background=bg, foreground=COLORS["text"], font=body_font)
        style.configure("Heading.TLabel", background=bg, foreground=COLORS["text"], font=heading_font)
        style.configure("Section.TLabel", background=panel, foreground=COLORS["text"], font=heading_font)
        style.configure("Muted.TLabel", background=bg, foreground=COLORS["muted"], font=body_font)
        style.configure("Panel.TLabel", background=panel, foreground=COLORS["text"], font=body_font)
        style.configure("Muted.Panel.TLabel", background=panel, foreground=COLORS["muted"], font=("Segoe UI Variable Text", small_size))
        style.configure("Risk.TLabel", background=panel, foreground=COLORS["red"], font=body_font)
        for variant, fg, bgc in (
            ("Primary", "#FFFFFF", COLORS["primary"]),
            ("Success", COLORS["success"], COLORS["success_soft"]),
            ("Info", COLORS["primary"], COLORS["primary_soft"]),
            ("Warning", COLORS["warning"], COLORS["warning_soft"]),
            ("Danger", COLORS["danger"], COLORS["danger_soft"]),
            ("Neutral", COLORS["text_muted"], glass),
        ):
            style.configure(f"Badge.{variant}.TLabel", background=bgc, foreground=fg, padding=(8, 3), font=("Segoe UI Variable Text", small_size, "bold"))
        style.configure("TCheckbutton", background=panel, foreground=COLORS["text"], font=body_font)
        style.configure("Panel.TCheckbutton", background=panel, foreground=COLORS["text"], font=body_font)
        style.configure("Green.TCheckbutton", background=panel, foreground=COLORS["green"], font=body_font)
        style.configure("Risk.TCheckbutton", background=panel, foreground=COLORS["red"], font=body_font)
        style.map("TCheckbutton", background=[("active", hover)], foreground=[("disabled", disabled_text)])
        style.map("TRadiobutton", background=[("active", hover)], foreground=[("disabled", disabled_text)])
        style.map("Green.TCheckbutton", foreground=[("!disabled", COLORS["green"])])
        style.map("Risk.TCheckbutton", foreground=[("!disabled", COLORS["red"])])
        style.configure("TRadiobutton", background=panel, foreground=COLORS["text"], font=body_font)
        style.configure("TEntry", fieldbackground=glass, foreground=COLORS["text"], insertcolor=COLORS["text"], bordercolor=COLORS["border"], lightcolor=COLORS["border"], darkcolor=COLORS["border"], padding=(8, 6))
        style.map("TEntry", fieldbackground=[("disabled", disabled_bg), ("focus", panel)], bordercolor=[("focus", COLORS["focus_ring"])], foreground=[("disabled", disabled_text)])
        style.configure("Search.TEntry", fieldbackground=panel, background=panel, foreground=COLORS["text"], insertcolor=COLORS["text"], bordercolor=panel, lightcolor=panel, darkcolor=panel, padding=(0, 2))
        style.map("Search.TEntry", fieldbackground=[("focus", panel), ("!disabled", panel)], foreground=[("disabled", disabled_text)])
        style.configure("TCombobox", fieldbackground=glass, foreground=COLORS["text"], arrowcolor=COLORS["muted"], bordercolor=COLORS["border"], lightcolor=COLORS["border"], darkcolor=COLORS["border"], padding=(8, 6))
        style.map("TCombobox", fieldbackground=[("readonly", glass), ("disabled", disabled_bg)], foreground=[("disabled", disabled_text)], bordercolor=[("focus", COLORS["focus_ring"])])
        style.configure("TButton", background=panel, foreground=COLORS["text"], bordercolor=COLORS["border"], lightcolor=COLORS["border"], darkcolor=COLORS["border"], focusthickness=1, focuscolor=COLORS["focus_ring"], padding=(14, 8), font=button_font)
        style.map("TButton", background=[("disabled", disabled_bg), ("pressed", pressed), ("active", hover)], foreground=[("disabled", disabled_text)])
        for name in ("Accent", "Primary"):
            style.configure(f"{name}.TButton", background=COLORS["primary"], foreground="#FFFFFF", bordercolor=COLORS["primary"], lightcolor=COLORS["primary"], darkcolor=COLORS["primary"], padding=(14, 8), font=button_font)
            style.map(f"{name}.TButton", background=[("disabled", disabled_bg), ("pressed", COLORS["primary_pressed"]), ("active", COLORS["primary_hover"])], foreground=[("disabled", disabled_text), ("!disabled", "#FFFFFF")])
        style.configure("Secondary.TButton", background=panel, foreground=COLORS["text"], bordercolor=COLORS["border"], lightcolor=COLORS["border"], darkcolor=COLORS["border"], padding=(14, 8), font=button_font)
        style.map("Secondary.TButton", background=[("disabled", disabled_bg), ("pressed", pressed), ("active", hover)], foreground=[("disabled", disabled_text)])
        style.configure("Subtle.TButton", background=bg, foreground=COLORS["text"], bordercolor=bg, lightcolor=bg, darkcolor=bg, padding=(12, 7), font=button_font)
        style.map("Subtle.TButton", background=[("disabled", bg), ("pressed", pressed), ("active", hover)], foreground=[("disabled", disabled_text)])
        for name in ("Danger", "Destructive"):
            style.configure(f"{name}.TButton", background=COLORS["danger"], foreground="#FFFFFF", bordercolor=COLORS["danger"], lightcolor=COLORS["danger"], darkcolor=COLORS["danger"], padding=(14, 8), font=button_font)
            style.map(f"{name}.TButton", background=[("disabled", disabled_bg), ("active", COLORS["danger"]), ("pressed", COLORS["danger_soft"])], foreground=[("disabled", disabled_text), ("!disabled", "#FFFFFF")])
        style.configure("DangerOutline.TButton", background=panel, foreground=COLORS["danger"], bordercolor=COLORS["danger"], lightcolor=COLORS["danger"], darkcolor=COLORS["danger"], padding=(14, 8), font=button_font)
        style.configure("Icon.TButton", background=panel, foreground=COLORS["text"], bordercolor=COLORS["border"], padding=(8, 6), font=button_font)
        style.configure("Treeview", background=panel, fieldbackground=panel, foreground=COLORS["text"], bordercolor=COLORS["border"], rowheight=max(30, int(32 * font_scale)), font=body_font)
        style.configure("Treeview.Heading", background=glass, foreground=COLORS["text"], bordercolor=COLORS["border"], relief="flat", padding=(8, 6), font=("Segoe UI Variable Text", small_size, "bold"))
        style.map("Treeview", background=[("selected", COLORS["primary_soft"])], foreground=[("selected", COLORS["text"])])
        style.configure("Visible.Horizontal.TProgressbar", thickness=10, troughcolor=COLORS["border"], background=COLORS["primary"], lightcolor=COLORS["primary"], darkcolor=COLORS["primary"], bordercolor=COLORS["border"])
        style.configure("Vertical.TScrollbar", background=glass, troughcolor=glass, bordercolor=COLORS["border"], arrowcolor=COLORS["muted"], gripcount=0, width=12)
        style.map("Vertical.TScrollbar", background=[("active", COLORS["primary"]), ("pressed", pressed)], arrowcolor=[("active", COLORS["text"])])
        style.configure("Horizontal.TScrollbar", background=glass, troughcolor=glass, bordercolor=COLORS["border"], arrowcolor=COLORS["muted"], gripcount=0, width=12)
        style.map("Horizontal.TScrollbar", background=[("active", COLORS["primary"]), ("pressed", pressed)], arrowcolor=[("active", COLORS["text"])])
        style.configure("TNotebook", background=bg, borderwidth=0)
        style.configure("TNotebook.Tab", background=panel, foreground=COLORS["muted"], padding=(14, 8), borderwidth=1, font=button_font)
        style.map("TNotebook.Tab", background=[("selected", hover), ("active", glass)], foreground=[("selected", COLORS["text"]), ("active", COLORS["text"])])
        style.configure("TLabelframe", background=panel, foreground=COLORS["text"], bordercolor=COLORS["border"])
        style.configure("TLabelframe.Label", background=panel, foreground=COLORS["text"], font=heading_font)
        style.configure("Nav.TButton", padding=(12, 9), anchor="w", background=panel, foreground=COLORS["text"], bordercolor=COLORS["border"], font=button_font)
        style.map("Nav.TButton", background=[("active", hover), ("pressed", pressed)], foreground=[("active", COLORS["text"])])
        # Hide notebook tabs — navigation is via the side rail only
        style.layout("Rail.TNotebook.Tab", [])
        style.configure("Green.TCheckbutton", foreground=COLORS["green"])

    def _build(self):
        header = ttk.Frame(self.root, padding=18)
        header.pack(fill="x", padx=18, pady=(18, 10))
        header_top = ttk.Frame(header)
        header_top.pack(fill="x")
        title_box = ttk.Frame(header_top)
        title_box.pack(side=LEFT, fill="x", expand=True)
        brand = ttk.Frame(title_box)
        brand.pack(anchor="w")
        self.brand_logo_label = ttk.Label(brand)
        self.brand_logo_label.pack(side=LEFT, padx=(0, 14))
        self.set_brand_logo(self.settings.get("theme", "Light"))
        copy = ttk.Frame(brand)
        copy.pack(side=LEFT, fill="x", expand=True)
        word_row = ttk.Frame(copy)
        word_row.pack(anchor="w")
        title_font = ("Segoe UI Variable Display", 28, "bold")
        self.brand_useful_label = ttk.Label(word_row, text="Useful", font=title_font)
        self.brand_windows_label = ttk.Label(word_row, text="Windows", font=title_font)
        self.brand_utils_label = ttk.Label(word_row, text="Utils", font=title_font)
        self.brand_useful_label.pack(side=LEFT)
        self.brand_windows_label.pack(side=LEFT)
        self.brand_utils_label.pack(side=LEFT)
        self.brand_subtitle_label = ttk.Label(copy, text="Install apps, tune Windows, inspect security signals.", style="Muted.TLabel")
        self.brand_subtitle_label.pack(anchor="w")
        self.update_brand_colors(self.settings.get("theme", "Light"))
        search = ttk.Frame(header_top, style="Panel.TFrame", padding=(10, 8))
        search.pack(side=RIGHT, fill="x", padx=(16, 0))
        self.search_text = StringVar()
        search_row, self.search_entry = SearchEntry(search, self.search_text, self.global_search, width=28)
        search_row.pack(side=LEFT, fill="x", expand=True)
        self.search_entry.bind("<Return>", self.open_selected_search_result)
        self.search_entry.bind("<Escape>", lambda _e: (self.search_text.set(""), self.update_search_results([])))
        ThemedButton(search, text="Search", variant="primary", command=self.global_search).pack(side=LEFT, padx=(8, 0))
        self.search_matches = []
        self.search_results = Listbox(self.root, height=5, bg=COLORS["panel"], fg=COLORS["text"], selectbackground=COLORS["accent"], relief="flat")
        self.search_results.bind("<Double-Button-1>", self.open_selected_search_result)
        self.search_results.bind("<Return>", self.open_selected_search_result)

        body = ttk.Frame(self.root)
        body.pack(fill=BOTH, expand=True, padx=18, pady=(0, 10))
        self.nav = ttk.Frame(body, padding=8)
        self.nav.pack(side=LEFT, fill="y", padx=(0, 10))
        self.nav.configure(width=220)
        self.nav.pack_propagate(False)
        self.tabs = ttk.Notebook(body, style="Rail.TNotebook")
        self.tabs.pack(side=LEFT, fill=BOTH, expand=True)
        self._apps_tab()
        self._installed_tab()
        self._tweaks_tab()
        self._features_tab()
        self._security_tab()
        self._path_tab()
        self._iso_tab()
        self._file_mover_tab()
        self._settings_tab()
        self._about_tab()
        self._build_nav()

        bottom = ttk.Frame(self.root, padding=(12, 8))
        bottom.pack(fill="x", padx=18, pady=(0, 18))
        self.progress = ttk.Progressbar(bottom, mode="determinate", length=400, style="Visible.Horizontal.TProgressbar")
        self.progress.pack(side=LEFT, fill="x", expand=True, padx=(0, 12), ipady=3)
        self.status = ttk.Label(bottom, text="Ready", foreground=COLORS["muted"])
        self.status.pack(side=RIGHT)

    def set_brand_logo(self, theme):
        if not hasattr(self, "brand_logo_label"):
            return
        try:
            img = PhotoImage(file=str(brand_icon_path(theme)))
            factor = max(1, img.width() // 64, img.height() // 64)
            self.brand_logo = img.subsample(factor, factor)
            self.brand_logo_label.configure(image=self.brand_logo)
            try:
                self.root.iconphoto(True, self.brand_logo)
            except Exception:
                pass
        except Exception:
            self.brand_logo_label.configure(image="")

    def update_brand_colors(self, theme):
        if hasattr(self, "brand_useful_label"):
            base = "#0F172A" if theme == "Light" else "#F8FAFC"
            self.brand_useful_label.configure(foreground=base)
            self.brand_windows_label.configure(foreground=COLORS["primary"])
            self.brand_utils_label.configure(foreground=COLORS.get("magenta", base) if theme == "Cyberpunk" else base)
        if hasattr(self, "brand_subtitle_label"):
            self.brand_subtitle_label.configure(foreground=COLORS["muted"])
        if hasattr(self, "about_useful_label"):
            base = "#0F172A" if theme == "Light" else "#F8FAFC"
            self.about_useful_label.configure(foreground=base)
            self.about_windows_label.configure(foreground=COLORS["primary"])
            self.about_utils_label.configure(foreground=COLORS.get("magenta", base) if theme == "Cyberpunk" else base)

    def _recursive_panel_style(self, widget, in_panel=False):
        try:
            current_style = widget.cget("style") if "style" in widget.keys() else ""
        except Exception:
            current_style = ""
            
        if current_style == "Panel.TFrame":
            in_panel = True
            
        if in_panel:
            wtype = widget.winfo_class()
            if wtype == "TLabel":
                widget.configure(style="Panel.TLabel")
            elif wtype == "TFrame" and current_style == "":
                widget.configure(style="PanelInner.TFrame")
            elif wtype == "TCheckbutton" and current_style in ("", "TCheckbutton"):
                widget.configure(style="Panel.TCheckbutton")
                
        for child in widget.winfo_children():
            self._recursive_panel_style(child, in_panel)

    def _repaint_widget_backgrounds(self, widget, parent_bg=None):
        bg = COLORS["bg"] if parent_bg is None else parent_bg
        try:
            style_name = widget.cget("style") if "style" in widget.keys() else ""
        except Exception:
            style_name = ""
        wtype = widget.winfo_class()
        if widget is self.root:
            bg = COLORS["bg"]
        elif style_name in {"Panel.TFrame", "PanelInner.TFrame"}:
            bg = COLORS["panel"]
        elif isinstance(widget, RoundedButton):
            widget._draw()
            bg = COLORS["panel"]
        elif isinstance(widget, ToggleSwitch):
            widget._draw()
            bg = COLORS["panel"]
        elif isinstance(widget, (ModernCheckbutton, ModernRadiobutton, RoundedInputShell)):
            widget._draw()
            bg = widget.cget("background")
        elif isinstance(widget, ThemedProgressbar):
            widget._draw()
            bg = COLORS["background"]
        elif isinstance(widget, ThemedScrollbar):
            bg = COLORS["glass"]
            widget._draw()
        elif wtype == "Canvas":
            bg = COLORS["panel"]
            widget.configure(background=bg)
        elif wtype == "Text" and not getattr(widget, "_uwu_logbox", False):
            bg = COLORS["panel"]
        elif wtype == "Listbox":
            widget.configure(bg=COLORS["panel"], fg=COLORS["text"], selectbackground=COLORS["accent"], selectforeground="#FFFFFF", highlightbackground=COLORS["line"], highlightcolor=COLORS["accent"])
        if wtype in {"TLabel", "TCheckbutton", "TRadiobutton"}:
            try:
                widget.configure(background=parent_bg or COLORS["bg"])
            except Exception:
                pass
        for child in widget.winfo_children():
            self._repaint_widget_backgrounds(child, bg)

    def _build_nav(self):
        for w in self.nav.winfo_children():
            w.destroy()
        icon_map = {
            "Apps": "▦",
            "Installed": "▣",
            "Windows Tweaks": "⚙",
            "Features": "✦",
            "Security": "🛡",
            "PATH": "⌁",
            "ISO": "◉",
            "File Mover": "↔",
            "Settings": "⚙",
            "About": "ⓘ",
        }
        for i in range(self.tabs.index("end")):
            label = self.tabs.tab(i, "text")
            trans_label = self._(label)
            text = f"{icon_map.get(label, '')}\t{trans_label}"
            ttk.Button(self.nav, text=text, style="Nav.TButton", width=24, command=lambda idx=i: self.tabs.select(idx)).pack(fill="x", pady=2)
    def _logbox(self, parent, height=8):
        box = Text(parent, height=height, bg=COLORS["log"], fg=COLORS["log_text"], insertbackground=COLORS["log_text"], relief="flat", padx=12, pady=10, bd=0, highlightthickness=1, highlightbackground=COLORS["border"], highlightcolor=COLORS["focus_ring"])
        box.configure(font=("Consolas", 10))
        box.tag_configure("info", foreground=COLORS["primary"])
        box.tag_configure("success", foreground=COLORS["success"])
        box.tag_configure("warning", foreground=COLORS["warning"])
        box.tag_configure("danger", foreground=COLORS["danger"])
        box._uwu_logbox = True
        return box

    def _log_tools(self, parent, box):
        row = ttk.Frame(parent, style="Panel.TFrame")
        row.pack(fill="x", pady=(0, 4), before=box)
        ThemedButton(row, text="Export Log", variant="secondary", command=lambda: self.export_log(box)).pack(side=RIGHT)

    def export_log(self, box):
        text = box.get("1.0", END).strip()
        if not text:
            self.status.configure(text="No log content to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log", "*.log"), ("Text", "*.txt"), ("All", "*.*")])
        if path:
            Path(path).write_text(text + "\n", encoding="utf-8")
            self.status.configure(text=f"Log exported: {path}")

    def export_app_log(self):
        if not self.app_log:
            self.status.configure(text="No application log content to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log", "*.log"), ("Text", "*.txt"), ("All", "*.*")])
        if path:
            Path(path).write_text("\n".join(self.app_log) + "\n", encoding="utf-8")
            self.status.configure(text=f"Application log exported: {path}")

    def tab_index(self, label):
        for i in range(self.tabs.index("end")):
            if self.tabs.tab(i, "text") == label:
                return i
        return 0

    def search_records(self, term):
        records = []
        for app in self.apps:
            hay = " ".join([app["name"], app.get("category", ""), app.get("desc", ""), app.get("winget", ""), app.get("choco", "")]).lower()
            if term in hay:
                records.append(("Apps", "App: " + app["name"], app.get("desc", "")))
        for tw in self.tweaks:
            hay = " ".join([tw["name"], tw["category"], tw["key"], tw["desc"]]).lower()
            if term in hay:
                records.append(("Windows Tweaks", "Tweak: " + tw["name"], tw["desc"]))
        for feat in self.features:
            hay = " ".join([feat["name"], feat["category"], feat["desc"]]).lower()
            if term in hay:
                records.append(("Features", "Feature: " + feat["name"], feat["desc"]))
        if hasattr(self, "installed_rows"):
            for row in self.installed_rows.values():
                hay = " ".join(row.values()).lower()
                if term in hay:
                    records.append(("Installed", "Installed: " + row.get("name", ""), row.get("id", "")))
        for row in getattr(self, "c2_rows", []):
            hay = " ".join(str(x) for x in row).lower()
            if term in hay:
                records.append(("Security", "C2: " + str(row[0]), str(row[7])[:180] if len(row) > 7 else ""))
        for line in self.app_log[-300:]:
            if term in line.lower():
                records.append(("Settings", "Log: " + line[:120], "Application log"))
        return records[:60]

    def global_search(self, event=None):
        term = self.search_text.get().strip().lower()
        if not term:
            self.update_search_results([])
            return
        records = self.search_records(term)
        if not records:
            self.status.configure(text=f"No matches for: {term}")
            self.update_search_results([])
            return
        self.update_search_results(records)

    def update_search_results(self, records):
        self.search_matches = records
        if not hasattr(self, "search_results"):
            return
        self.search_results.delete(0, END)
        for tab, title, _detail in records[:8]:
            self.search_results.insert(END, f"{tab} - {title}")
        if records:
            self.search_results.selection_set(0)
            self.root.update_idletasks()
            x = self.search_entry.winfo_rootx() - self.root.winfo_rootx()
            y = self.search_entry.winfo_rooty() - self.root.winfo_rooty() + self.search_entry.winfo_height() + 4
            height = min(5, len(records)) * 24 + 6
            width = max(360, self.search_entry.winfo_width() + 90)
            self.search_results.place(x=x, y=y, width=width, height=height)
            self.search_results.lift()
        else:
            self.search_results.place_forget()

    def open_selected_search_result(self, event=None):
        if not getattr(self, "search_matches", None):
            self.global_search()
        sel = self.search_results.curselection() if hasattr(self, "search_results") else ()
        if self.search_matches:
            self.open_search_record(self.search_matches[sel[0] if sel else 0])

    def open_search_record(self, record):
        tab, title, detail = record
        self.tabs.select(self.tab_index(tab))
        if hasattr(self, "search_results"):
            self.search_results.place_forget()
        self.status.configure(text=(title + (" - " + detail if detail else ""))[:180])

    def _hero_banner(self, parent, icon, title, subtitle):
        banner = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        banner.pack(fill="x", pady=(0, 16), padx=10)
        ttk.Label(banner, text=icon, font=("Segoe UI Emoji", 34), style="Panel.TLabel").pack(side=LEFT, padx=(2, 16))
        text_frame = ttk.Frame(banner, style="PanelInner.TFrame")
        text_frame.pack(side=LEFT, fill="both", expand=True)
        ttk.Label(text_frame, text=title, font=("Segoe UI Variable Display", 18, "bold"), style="Panel.TLabel").pack(anchor="w")
        ttk.Label(text_frame, text=subtitle, foreground=COLORS["muted"], font=("Segoe UI Variable Text", 10)).pack(anchor="w")
        return banner

    def _apps_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="Apps")
        self._hero_banner(tab, "🛍️", "App Store", "Discover and install essential Windows applications securely.")
        
        top = ttk.Frame(tab, style="Panel.TFrame")
        top.pack(fill="x", pady=(0, 12), padx=10, ipady=6)
        ttk.Button(top, text="✓ Recommended", command=self.select_recommended).pack(side=LEFT, padx=(12, 4))
        ttk.Button(top, text="+ All", command=lambda: self.set_app_checks(True)).pack(side=LEFT, padx=4)
        ttk.Button(top, text="× Clear", command=lambda: self.set_app_checks(False)).pack(side=LEFT, padx=4)
        ttk.Label(top, text="Open-source apps are highlighted in green.", foreground=COLORS["green"]).pack(side=LEFT, padx=16)
        
        custom = ttk.Frame(top)
        custom.pack(side=LEFT, fill="x", expand=True, padx=(8, 0))
        self.winget_search_text = StringVar()
        ttk.Entry(custom, textvariable=self.winget_search_text, width=24).pack(side=LEFT, padx=(0, 4))
        ttk.Button(custom, text="Search Winget/Choco", command=self.install_winget_search).pack(side=LEFT)

        actions = ttk.Frame(top)
        actions.pack(side=RIGHT, padx=12)
        self.install_selected_button = ttk.Button(actions, text="⬇ " + self._("Install Selected"), style="Accent.TButton", command=lambda: self.package_selected("install"))
        self.install_selected_button.pack(side=RIGHT, padx=4)
        self.upgrade_selected_button = ttk.Button(actions, text="↻ " + self._("Upgrade Selected"), command=lambda: self.package_selected("upgrade"))
        self.upgrade_selected_button.pack(side=RIGHT, padx=4)
        self.mode = StringVar(value=self.settings.get("package_mode", "Winget then Chocolatey"))
        ttk.Combobox(actions, textvariable=self.mode, values=["Winget then Chocolatey", "Winget only", "Chocolatey only"], state="readonly", width=24).pack(side=RIGHT, padx=8)

        vsplit = ttk.PanedWindow(tab, orient="vertical")
        vsplit.pack(fill=BOTH, expand=True, padx=10)
        body = ttk.Frame(vsplit)
        vsplit.add(body, weight=3)
        sf = ScrollFrame(body)
        sf.pack(fill=BOTH, expand=True)
        
        for cat in sorted({a["category"] for a in self.apps}):
            cat_frame = ttk.Frame(sf.inner, style="Panel.TFrame")
            cat_frame.pack(fill="x", pady=(0, 12), padx=4)
            ttk.Label(cat_frame, text=cat, font=("Segoe UI", 13, "bold"), foreground=COLORS["accent"]).pack(anchor="w", pady=(12, 8), padx=12)
            grid = ttk.Frame(cat_frame)
            grid.pack(fill="x", padx=12, pady=(0, 12))
            for col in range(4):
                grid.columnconfigure(col, weight=1, uniform="apps")
            for i, app in enumerate([a for a in self.apps if a["category"] == cat]):
                var = self.app_vars[app["key"]] = BooleanVar(value=False)
                cb_style = "Green.TCheckbutton" if app.get("foss") else "TCheckbutton"
                cb = ttk.Checkbutton(grid, text=app["name"], variable=var, style=cb_style)
                cb.grid(row=i // 4, column=i % 4, sticky="w", padx=8, pady=4)
                cb.configure(command=lambda a=app: self.status.configure(text=a["desc"][:140] or a["name"]))
                Tooltip(cb, app["desc"])
                
        log_pane = ttk.Frame(vsplit)
        vsplit.add(log_pane, weight=1)
        self.apps_log = self._logbox(log_pane)
        self.apps_log.pack(fill=BOTH, expand=True)
        self._log_tools(log_pane, self.apps_log)

    def _installed_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="Installed")
        self._hero_banner(tab, "📦", "Installed Applications", "Manage, upgrade, and uninstall your Windows software.")
        
        top = ttk.Frame(tab, style="Panel.TFrame")
        top.pack(fill="x", pady=(0, 12), padx=10, ipady=6)
        ttk.Button(top, text="Refresh", command=self.refresh_installed).pack(side=LEFT, padx=(12, 4))
        section_row = ttk.Frame(top, style="PanelInner.TFrame")
        section_row.pack(side=LEFT, padx=8)
        self.installed_sections = {}
        self.installed_section_buttons = {}
        for name in ("Installer", "Debloater"):
            btn = ttk.Button(section_row, text=name, style="Secondary.TButton", width=14, command=lambda n=name: self.show_installed_section(n))
            btn.pack(side=LEFT, padx=4)
            self.installed_section_buttons[name] = btn
        
        actions = ttk.Frame(top)
        actions.pack(side=RIGHT, padx=12)
        ttk.Button(actions, text="↻ Upgrade All", command=lambda: self.thread("Upgrade all", self.run_cmd, ["winget", "upgrade", "--all", "--silent", "--accept-source-agreements", "--accept-package-agreements"], self.installed_log)).pack(side=LEFT, padx=4)
        ttk.Button(actions, text="↻ Upgrade Selected", style="Accent.TButton", command=self.upgrade_installed).pack(side=LEFT, padx=4)
        ttk.Button(actions, text="⌫ Uninstall Selected", style="Danger.TButton", command=self.uninstall_installed).pack(side=LEFT, padx=4)

        content = ttk.Frame(tab)
        content.pack(fill=BOTH, expand=True, padx=10)
        apps_tab = ttk.Frame(content, padding=8)
        debloat_tab = ttk.Frame(content, padding=8)
        self.installed_sections["Installer"] = apps_tab
        self.installed_sections["Debloater"] = debloat_tab
        self._debloater_section(debloat_tab)

        vsplit = ttk.PanedWindow(apps_tab, orient="vertical")
        vsplit.pack(fill=BOTH, expand=True)
        tree_frame = ttk.Frame(vsplit)
        vsplit.add(tree_frame, weight=3)
        self.installed_tree = ttk.Treeview(tree_frame, columns=("sel", "name", "id", "version"), show="headings")
        self.installed_tree.heading("sel", text="")
        self.installed_tree.heading("name", text="Name")
        self.installed_tree.heading("id", text="Package ID")
        self.installed_tree.heading("version", text="Version")
        self.installed_tree.column("sel", width=48, minwidth=48, stretch=False, anchor="center")
        self.installed_tree.pack(fill=BOTH, expand=True, pady=(0, 10))
        self.installed_tree.bind("<Button-1>", self.installed_tree_click, add="+")
        
        log_pane = ttk.Frame(vsplit)
        vsplit.add(log_pane, weight=1)
        self.installed_log = self._logbox(log_pane)
        self.installed_log.pack(fill=BOTH, expand=True)
        self._log_tools(log_pane, self.installed_log)
        self.show_installed_section("Installer")
        self.root.after(1200, self.refresh_installed)

    def show_installed_section(self, name):
        for section in self.installed_sections.values():
            section.pack_forget()
        for section_name, button in self.installed_section_buttons.items():
            button.configure(style="Accent.TButton" if section_name == name else "Secondary.TButton")
        self.installed_sections[name].pack(fill=BOTH, expand=True)

    def _debloater_section(self, tab):
        top = ttk.Frame(tab, style="Panel.TFrame")
        top.pack(fill="x", pady=(0, 12), ipady=6)
        ttk.Label(top, text="Win11Debloat + CTT Debloat", font=("Segoe UI", 12, "bold")).pack(side=LEFT, padx=12)
        ttk.Button(top, text="Select Recommended", command=self.select_recommended_debloat).pack(side=RIGHT, padx=(4, 12))
        ttk.Button(top, text="Clear", command=self.clear_debloat_apps).pack(side=RIGHT, padx=4)
        ttk.Button(top, text="Run CTT Debloat", style="Danger.TButton", command=self.run_ctt_debloat).pack(side=RIGHT, padx=4)
        ttk.Button(top, text="Remove Selected", style="Danger.TButton", command=self.remove_selected_debloat).pack(side=RIGHT, padx=4)

        vsplit = ttk.PanedWindow(tab, orient="vertical")
        vsplit.pack(fill=BOTH, expand=True)
        list_frame = ttk.Frame(vsplit)
        vsplit.add(list_frame, weight=3)
        sf = ScrollFrame(list_frame)
        sf.pack(fill=BOTH, expand=True)
        rec_order = {"safe": 0, "optional": 1, "limited": 2, "advanced": 3, "unsafe": 4, "": 99}
        recommendations = sorted({str(a.get("recommendation", "")).lower() for a in self.debloat_apps}, key=lambda r: (rec_order.get(r, 50), r))
        for rec in recommendations:
            apps = [a for a in self.debloat_apps if str(a.get("recommendation", "")).lower() == rec]
            if not apps:
                continue
            title = rec.title() if rec else "Other"
            cat_frame = ttk.Frame(sf.inner, style="Panel.TFrame")
            cat_frame.pack(fill="x", pady=(0, 10), padx=4)
            ttk.Label(cat_frame, text=title, font=("Segoe UI", 13, "bold"), foreground=COLORS["accent"]).pack(anchor="w", pady=(12, 8), padx=12)
            for app in apps:
                var = self.debloat_vars[app["appid"]] = BooleanVar(value=app["selected"])
                text = f"{app['name']}  [{app['method']}: {app['appid']}]"
                cb = ttk.Checkbutton(cat_frame, text=text, variable=var, command=lambda a=app: self.status.configure(text=a["desc"][:160] or a["name"]))
                cb.pack(anchor="w", padx=16, pady=3)
                Tooltip(cb, app["desc"] or app["appid"])

        log_pane = ttk.Frame(vsplit)
        vsplit.add(log_pane, weight=1)
        self.debloat_log = self._logbox(log_pane)
        self.debloat_log.pack(fill=BOTH, expand=True)
        self._log_tools(log_pane, self.debloat_log)

    def _tweaks_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="Windows Tweaks")
        self._hero_banner(tab, "🛠️", "System Tweaks", "Safely customize Windows behavior, privacy, and performance.")
        
        top = ttk.Frame(tab, style="Panel.TFrame")
        top.pack(fill="x", pady=(0, 12), padx=10, ipady=6)
        
        dns_frame = ttk.Frame(top)
        dns_frame.pack(side=LEFT, padx=12)
        self.dns_name = StringVar(value="Default")
        ttk.Label(dns_frame, text="DNS Provider:").pack(side=LEFT, padx=(0, 8))
        ttk.Combobox(dns_frame, textvariable=self.dns_name, values=list(self.dns.keys()), state="readonly", width=24).pack(side=LEFT, padx=(0, 8))
        ttk.Button(dns_frame, text="Set DNS", command=self.set_dns).pack(side=LEFT)

        if self.tweak_presets:
            self.tweak_preset = StringVar(value=next(iter(self.tweak_presets)))
            ttk.Combobox(top, textvariable=self.tweak_preset, values=list(self.tweak_presets), state="readonly", width=12).pack(side=LEFT, padx=(12, 4))
            ttk.Button(top, text="Load Preset", command=self.select_tweak_preset).pack(side=LEFT)
        
        actions = ttk.Frame(top)
        actions.pack(side=RIGHT, padx=12)
        ttk.Button(actions, text="Create Restore Point", command=lambda: self.run_ps(f"Checkpoint-Computer -Description '{APP_NAME}' -RestorePointType MODIFY_SETTINGS", self.tweak_log)).pack(side=LEFT, padx=4)
        ttk.Button(actions, text="Clear Selected", command=self.clear_selected_tweaks).pack(side=LEFT, padx=4)
        ttk.Button(actions, text="Apply Selected Tweaks", style="Accent.TButton", command=self.apply_selected_tweaks).pack(side=LEFT, padx=4)

        vsplit = ttk.PanedWindow(tab, orient="vertical")
        vsplit.pack(fill=BOTH, expand=True, padx=10)
        panes = ttk.PanedWindow(vsplit, orient="horizontal")
        vsplit.add(panes, weight=3)
        left = ScrollFrame(panes)
        right = ScrollFrame(panes)
        panes.add(left, weight=3)
        panes.add(right, weight=2)
        
        for cat in sorted({t["category"] for t in self.tweaks if not t["toggle"]}):
            cat_frame = ttk.Frame(left.inner, style="Panel.TFrame")
            cat_frame.pack(fill="x", pady=(0, 12), padx=(0, 8))
            ttk.Label(cat_frame, text=cat, font=("Segoe UI", 13, "bold"), foreground=COLORS["accent"]).pack(anchor="w", pady=(12, 8), padx=12)
            
            for tw in [x for x in self.tweaks if x["category"] == cat and not x["toggle"]]:
                var = self.tweak_vars[tw["key"]] = BooleanVar(value=False)
                risky = self.high_risk(tw)
                label_text = ("⚠️ HIGH RISK - " if risky else "") + tw["name"]
                cb = ttk.Checkbutton(cat_frame, text=label_text, variable=var, style="Risk.TCheckbutton" if risky else "Panel.TCheckbutton", command=lambda t=tw: self.status.configure(text=t["desc"][:160]))
                cb.pack(anchor="w", padx=16, pady=4)
                Tooltip(cb, tw["desc"])
                
        for cat in sorted({t["category"] for t in self.tweaks if t["toggle"]}):
            cat_frame = ttk.Frame(right.inner, style="Panel.TFrame")
            cat_frame.pack(fill="x", pady=(0, 12), padx=(8, 0))
            ttk.Label(cat_frame, text=cat, font=("Segoe UI", 13, "bold"), foreground=COLORS["accent"]).pack(anchor="w", pady=(12, 8), padx=12)
            
            for tw in [x for x in self.tweaks if x["category"] == cat and x["toggle"]]:
                var = self.tweak_vars[tw["key"]] = BooleanVar(value=self.tweak_enabled(tw))
                row = ttk.Frame(cat_frame)
                row.pack(fill="x", pady=4, padx=16)
                
                lbl = ttk.Label(row, text=("HIGH RISK - " if self.high_risk(tw) else "") + tw["name"], style="Risk.TLabel" if self.high_risk(tw) else "Panel.TLabel")
                lbl.pack(side=LEFT, fill="x", expand=True)
                
                def make_toggle_cmd(t=tw, v=var):
                    if not messagebox.askyesno("Confirm Tweak", f"Are you sure you want to apply: {t['name']}?"):
                        v.set(not v.get()) # revert
                        return
                    self.thread(t["name"], self.apply_tweak, t, v.get(), self.tweak_log, False)
                
                switch = ToggleSwitch(row, variable=var, command=make_toggle_cmd)
                switch.pack(side=RIGHT, padx=(8, 0))
                self.toggle_widgets.append(switch)
                Tooltip(switch, tw["desc"])
                Tooltip(lbl, tw["desc"])
                
        log_pane = ttk.Frame(vsplit)
        vsplit.add(log_pane, weight=1)
        self.tweak_log = self._logbox(log_pane)
        self.tweak_log.pack(fill=BOTH, expand=True)
        self._log_tools(log_pane, self.tweak_log)

    def _features_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="Features")
        self._hero_banner(tab, "✨", "Windows Features", "Install or remove optional Windows components.")
        
        top = ttk.Frame(tab, style="Panel.TFrame")
        top.pack(fill="x", pady=(0, 12), padx=10, ipady=6)
        ttk.Button(top, text="Run Selected Features", style="Accent.TButton", command=self.run_selected_features).pack(side=RIGHT, padx=12)
        
        vsplit = ttk.PanedWindow(tab, orient="vertical")
        vsplit.pack(fill=BOTH, expand=True, padx=10)
        sf_frame = ttk.Frame(vsplit)
        vsplit.add(sf_frame, weight=3)
        sf = ScrollFrame(sf_frame)
        sf.pack(fill=BOTH, expand=True)
        
        for cat in sorted({f["category"] for f in self.features}):
            cat_frame = ttk.Frame(sf.inner, style="Panel.TFrame")
            cat_frame.pack(fill="x", pady=(0, 12), padx=4)
            ttk.Label(cat_frame, text=cat, font=("Segoe UI", 13, "bold"), foreground=COLORS["accent"]).pack(anchor="w", pady=(12, 8), padx=12)
            for feat in [x for x in self.features if x["category"] == cat]:
                var = self.feature_vars[feat["key"]] = BooleanVar(value=False)
                cb = ttk.Checkbutton(cat_frame, text=feat["name"], variable=var, command=lambda f=feat: self.status.configure(text=f["desc"][:160]))
                cb.pack(anchor="w", padx=16, pady=4)
                Tooltip(cb, feat["desc"])
                
        log_pane = ttk.Frame(vsplit)
        vsplit.add(log_pane, weight=1)
        self.feature_log = self._logbox(log_pane)
        self.feature_log.pack(fill=BOTH, expand=True)
        self._log_tools(log_pane, self.feature_log)

    def run_selected_features(self):
        items = [f for f in self.features if self.feature_vars.get(f["key"]) and self.feature_vars[f["key"]].get()]
        if not items:
            self.log(self.feature_log, "WARN Select at least one feature.")
            return
        if not messagebox.askyesno("Confirm Features", "Are you sure you want to install/run these features?"):
            return
        self.thread("Features", self.features_worker, items, self.feature_log)

    def features_worker(self, items, box):
        for i, feat in enumerate(items, 1):
            self.set_progress(i - 1, len(items))
            self.log(box, f"Running {i}/{len(items)}: {feat['name']}")
            for name in feat["features"]:
                if name:
                    self.run_cmd(["dism", "/Online", "/Enable-Feature", f"/FeatureName:{name}", "/All", "/NoRestart"], box)
            for script in feat["scripts"]:
                if script:
                    self.run_cmd(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", self.ps_prelude() + "\n" + script], box)
            self.set_progress(i, len(items))

    def _security_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="Security")
        section_row = ttk.Frame(tab, style="Panel.TFrame")
        section_row.pack(fill="x", pady=(0, 12), ipady=6)
        self.security_sections = {}
        self.security_section_buttons = {}
        for name in ("System", "VirusTotal", "C2 Collector"):
            section = ttk.Frame(tab, padding=12)
            self.security_sections[name] = section
            btn = ttk.Button(section_row, text=name, style="Secondary.TButton", command=lambda n=name: self.show_security_section(n))
            btn.pack(side=LEFT, padx=(12 if name == "System" else 4, 4))
            self.security_section_buttons[name] = btn

        system_tab = self.security_sections["System"]
        vt_tab = self.security_sections["VirusTotal"]
        c2_tab = self.security_sections["C2 Collector"]
        tab = system_tab
        
        # Windows Defender Inspired Hero Banner
        banner = ttk.Frame(tab)
        banner.pack(fill="x", pady=(0, 20))
        ttk.Label(banner, text="🛡️", font=("Segoe UI Emoji", 48)).pack(side=LEFT, padx=(10, 20))
        text_frame = ttk.Frame(banner)
        text_frame.pack(side=LEFT, fill="both", expand=True)
        ttk.Label(text_frame, text="Security at a glance", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(text_frame, text="Manage scans, signatures, and inspect active processes.", foreground=COLORS["green"], font=("Segoe UI", 11)).pack(anchor="w")
        
        cards = ttk.Frame(tab)
        cards.pack(fill="x")
        
        # Quick Actions Card
        quick = ttk.Frame(cards, style="Panel.TFrame")
        quick.pack(side=LEFT, fill="both", expand=True, padx=(0, 10))
        ttk.Label(quick, text="Quick Actions", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        b1 = ttk.Frame(quick); b1.pack(fill="x", padx=12, pady=4)
        ttk.Button(b1, text="Update Defender", width=18, command=lambda: self.run_ps("Update-MpSignature", self.security_log)).pack(side=LEFT)
        ttk.Label(b1, text="Download the latest antivirus signatures.", foreground=COLORS["muted"]).pack(side=LEFT, padx=10)
        b2 = ttk.Frame(quick); b2.pack(fill="x", padx=12, pady=4)
        ttk.Button(b2, text="Quick Scan", width=18, command=lambda: self.run_ps("Start-MpScan -ScanType QuickScan", self.security_log)).pack(side=LEFT)
        ttk.Label(b2, text="Scan common malware locations.", foreground=COLORS["muted"]).pack(side=LEFT, padx=10)
        b3 = ttk.Frame(quick); b3.pack(fill="x", padx=12, pady=(4, 12))
        ttk.Button(b3, text="Full Scan", width=18, command=lambda: self.run_ps("Start-MpScan -ScanType FullScan", self.security_log)).pack(side=LEFT)
        ttk.Label(b3, text="Comprehensive system-wide scan.", foreground=COLORS["muted"]).pack(side=LEFT, padx=10)

        # Diagnostics Card
        adv = ttk.Frame(cards, style="Panel.TFrame")
        adv.pack(side=LEFT, fill="both", expand=True, padx=(10, 0))
        ttk.Label(adv, text="Diagnostics", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        b4 = ttk.Frame(adv); b4.pack(fill="x", padx=12, pady=4)
        ttk.Button(b4, text="Hash File", width=22, command=self.hash_file).pack(side=LEFT)
        ttk.Button(b4, text="Hash Folder CSV", width=22, command=self.hash_folder).pack(side=LEFT, padx=8)
        b5 = ttk.Frame(adv); b5.pack(fill="x", padx=12, pady=4)
        ttk.Button(b5, text="Established Connections", width=22, command=self.netstat).pack(side=LEFT)
        ttk.Button(b5, text="Export Processes", width=22, command=self.processes).pack(side=LEFT, padx=8)

        self.security_log = self._logbox(tab, 12)
        self.security_log.pack(fill=BOTH, expand=True, pady=(20, 0))
        self._log_tools(tab, self.security_log)
        self._vt_tab(vt_tab)
        self._c2_tab(c2_tab)
        self.show_security_section("System")

    def show_security_section(self, name):
        for section in self.security_sections.values():
            section.pack_forget()
        for section_name, button in getattr(self, "security_section_buttons", {}).items():
            button.configure(style="Accent.TButton" if section_name == name else "Secondary.TButton")
        self.security_sections[name].pack(fill=BOTH, expand=True)

    def _vt_tab(self, tab=None):
        if tab is None:
            tab = ttk.Frame(self.tabs, padding=12)
            self.tabs.add(tab, text="VirusTotal")
        
        # VT Website Style Centered Hero
        hero = ttk.Frame(tab)
        hero.pack(fill="x", pady=(30, 20))
        ttk.Label(hero, text="VirusTotal", font=("Georgia", 32, "bold"), foreground="#0f4b99").pack(anchor="center")
        ttk.Label(hero, text="Analyze suspicious files, domains, IPs and URLs to detect malware and other breaches.", foreground=COLORS["muted"], font=("Segoe UI", 10)).pack(anchor="center", pady=(5, 20))
        
        search_frame = ttk.Frame(hero)
        search_frame.pack(anchor="center")
        
        self.vt_query = StringVar()
        ttk.Entry(search_frame, textvariable=self.vt_query, width=60, font=("Segoe UI", 12)).pack(side=LEFT, ipady=6, padx=(0, 8))
        ttk.Button(search_frame, text="🔍 Search", style="Accent.TButton", command=self.vt_lookup).pack(side=LEFT, ipady=3, padx=4)
        ttk.Button(search_frame, text="📁 Upload File", command=self.vt_upload).pack(side=LEFT, ipady=3, padx=4)
        
        self.vt_selected_file = StringVar(value="No file selected")
        ttk.Label(hero, textvariable=self.vt_selected_file, foreground=COLORS["muted"]).pack(anchor="center", pady=(8, 0))

        actions = ttk.Frame(tab)
        actions.pack(fill="x", pady=(0, 5))
        ttk.Button(actions, text="Export Report", command=self.vt_export).pack(side=RIGHT)
        
        self.last_vt = None
        self.last_vt_extra = {}
        self.vt_log = self._logbox(tab, 20)
        self.vt_log.pack(fill=BOTH, expand=True)
        self._log_tools(tab, self.vt_log)

    def _path_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="PATH")
        self._hero_banner(tab, "🗂️", "Environment Variables", "Easily manage your system and user PATH variables.")
        
        vsplit = ttk.PanedWindow(tab, orient="vertical")
        vsplit.pack(fill=BOTH, expand=True, padx=10)
        
        top = ttk.Frame(vsplit)
        vsplit.add(top, weight=3)
        
        panes = ttk.PanedWindow(top, orient="horizontal")
        panes.pack(fill=BOTH, expand=True)
        
        left = ttk.Frame(panes, style="Panel.TFrame")
        panes.add(left, weight=1)
        ttk.Label(left, text="Current PATH Entries", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 8))
        self.path_vars = []
        self.path_entries = ScrollFrame(left)
        self.path_entries.pack(fill=BOTH, expand=True, padx=12, pady=(0, 12))
            
        right = ttk.Frame(panes, style="Panel.TFrame")
        panes.add(right, weight=1)
        ttk.Label(right, text="PATH Controls", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 8))
        
        custom = ttk.Frame(right)
        custom.pack(fill="x", padx=16, pady=4)
        self.custom_path = StringVar()
        ttk.Entry(custom, textvariable=self.custom_path).pack(side=LEFT, fill="x", expand=True)
        ttk.Button(custom, text="Browse", command=lambda: self.custom_path.set(filedialog.askdirectory() or self.custom_path.get())).pack(side=LEFT, padx=4)
        
        scope = ttk.Frame(right)
        scope.pack(fill="x", padx=16, pady=(16, 4))
        self.path_scope = StringVar(value="User")
        ttk.Label(scope, text="Target Scope:").pack(side=LEFT)
        scope_box = ttk.Combobox(scope, textvariable=self.path_scope, values=["User", "System"], state="readonly", width=12)
        scope_box.pack(side=LEFT, padx=8)
        scope_box.bind("<<ComboboxSelected>>", lambda _e: self.load_path_entries())
        
        ttk.Label(right, text="Checked entries remain in PATH. Uncheck an entry and save to remove it.", foreground=COLORS["muted"], wraplength=360).pack(anchor="w", padx=16, pady=(12, 4))
        ttk.Button(right, text="Save PATH", style="Accent.TButton", command=self.add_paths).pack(anchor="w", padx=16, pady=(20, 4))
        ttk.Button(right, text="Reload", command=self.load_path_entries).pack(anchor="w", padx=16, pady=(4, 12))
        
        log_pane = ttk.Frame(vsplit)
        vsplit.add(log_pane, weight=1)
        self.path_log = self._logbox(log_pane)
        self.path_log.pack(fill=BOTH, expand=True)
        self._log_tools(log_pane, self.path_log)
        self.load_path_entries()

    def path_registry_target(self, scope):
        if scope == "System":
            return winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        return winreg.HKEY_CURRENT_USER, r"Environment"

    def get_path_entries(self, scope):
        if not winreg:
            return []
        root, subkey = self.path_registry_target(scope)
        try:
            with winreg.OpenKey(root, subkey) as key:
                value, _typ = winreg.QueryValueEx(key, "Path")
        except OSError:
            value = ""
        return [x.strip() for x in str(value).split(";") if x.strip()]

    def set_path_entries(self, scope, entries):
        if not winreg:
            return
        root, subkey = self.path_registry_target(scope)
        with winreg.CreateKeyEx(root, subkey, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, ";".join(entries))

    def load_path_entries(self):
        for child in self.path_entries.inner.winfo_children():
            child.destroy()
        self.path_vars = []
        for path in self.get_path_entries(self.path_scope.get()):
            var = BooleanVar(value=True)
            self.path_vars.append((var, path))
            ttk.Checkbutton(self.path_entries.inner, text=path, variable=var).pack(anchor="w", padx=4, pady=2)

    def _iso_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="ISO")
        self._hero_banner(tab, "💿", "ISO Creation & Patching", "Create custom Windows installers and bypass hardware checks.")
        refs = load_json("offline-references.json")["Iso"]
        self.iso_source, self.iso_out = StringVar(), StringVar()
        self.iso_edition = StringVar(value="Multi")
        self.iso_lang = StringVar(value="Default")
        self.iso_channel = StringVar(value="Retail")
        
        vsplit = ttk.PanedWindow(tab, orient="vertical")
        vsplit.pack(fill=BOTH, expand=True, padx=10)
        controls = ttk.Frame(vsplit)
        vsplit.add(controls, weight=2)
        cards = ttk.Frame(controls)
        cards.pack(fill="both", expand=True)
        
        # Step 1
        s1 = ttk.Frame(cards, style="Panel.TFrame")
        s1.pack(fill="x", pady=(0, 10), ipady=4)
        ttk.Label(s1, text="Step 1: Choose Files", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        for label, var, browse in [("Source ISO/folder", self.iso_source, self.pick_iso_source), ("Output ISO", self.iso_out, self.pick_iso_out)]:
            row = ttk.Frame(s1)
            row.pack(fill="x", pady=4, padx=16)
            ttk.Label(row, text=label, width=18).pack(side=LEFT)
            ttk.Entry(row, textvariable=var).pack(side=LEFT, fill="x", expand=True)
            ttk.Button(row, text="Browse", command=browse).pack(side=LEFT, padx=4)
            
        # Step 2
        s2 = ttk.Frame(cards, style="Panel.TFrame")
        s2.pack(fill="x", pady=(0, 10), ipady=4)
        ttk.Label(s2, text="Step 2: Configuration", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        row = ttk.Frame(s2)
        row.pack(fill="x", pady=4, padx=16)
        ttk.Label(row, text="Edition:").pack(side=LEFT)
        ttk.Combobox(row, textvariable=self.iso_edition, values=[x["Name"] for x in refs["Editions"]], state="readonly", width=30).pack(side=LEFT, padx=(4, 16))
        ttk.Label(row, text="Language:").pack(side=LEFT)
        ttk.Combobox(row, textvariable=self.iso_lang, values=[x["Name"] for x in refs["Languages"]], state="readonly", width=28).pack(side=LEFT, padx=(4, 16))
        ttk.Label(row, text="Channel:").pack(side=LEFT)
        ttk.Combobox(row, textvariable=self.iso_channel, values=[x["Name"] for x in refs["Channels"]], state="readonly", width=14).pack(side=LEFT, padx=4)
        
        # Step 3
        s3 = ttk.Frame(cards, style="Panel.TFrame")
        s3.pack(fill="x", pady=(0, 10), ipady=4)
        ttk.Label(s3, text="Step 3: Action", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        row2 = ttk.Frame(s3)
        row2.pack(fill="x", pady=4, padx=16)
        ttk.Button(row2, text="Show Available Editions", command=self.show_iso_editions).pack(side=LEFT, padx=4)
        ttk.Button(row2, text="Install ADK", command=lambda: self.thread("Install ADK", self.run_cmd, ["winget", "install", "Microsoft.WindowsADK", "--silent", "--accept-package-agreements", "--accept-source-agreements"], self.iso_log)).pack(side=LEFT, padx=4)
        ttk.Button(row2, text="Write ei.cfg (Patch Only)", command=self.write_eicfg).pack(side=RIGHT, padx=4)
        ttk.Button(row2, text="Create ISO", style="Accent.TButton", command=self.create_iso).pack(side=RIGHT, padx=4)

        self.iso_log = self._logbox(tab, 12)
        self.iso_log.pack(fill=BOTH, expand=True, padx=10, pady=(8, 0))
        self._log_tools(tab, self.iso_log)

    def _file_mover_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="File Mover")
        self._hero_banner(tab, "↔", "Bulk File Mover", "Move files in bulk by providing a text file of names.")
        
        vsplit = ttk.PanedWindow(tab, orient="vertical")
        vsplit.pack(fill=BOTH, expand=True, padx=10)
        controls = ttk.Frame(vsplit)
        vsplit.add(controls, weight=2)
        cards = ttk.Frame(controls)
        cards.pack(fill="both", expand=True)
        
        inputs = ttk.Frame(cards, style="Panel.TFrame")
        inputs.pack(fill="x", pady=(0, 10), ipady=4)
        ttk.Label(inputs, text="Locations", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        
        self.fm_src, self.fm_dst, self.fm_txt = StringVar(), StringVar(), StringVar()
        for label, var in [("Source Directory", self.fm_src), ("Destination Directory", self.fm_dst), ("Names Text File", self.fm_txt)]:
            row = ttk.Frame(inputs)
            row.pack(fill="x", pady=4, padx=16)
            ttk.Label(row, text=label, width=18).pack(side=LEFT)
            ttk.Entry(row, textvariable=var).pack(side=LEFT, fill="x", expand=True)
            cmd = (lambda v=var, l=label: v.set((filedialog.askopenfilename() if "File" in l else filedialog.askdirectory()) or v.get()))
            ttk.Button(row, text="Browse", command=cmd).pack(side=LEFT, padx=4)

        names = ttk.Frame(cards, style="Panel.TFrame")
        names.pack(fill="x", pady=(0, 10), ipady=4)
        ttk.Label(names, text="File Matches", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        mode_row = ttk.Frame(names)
        mode_row.pack(fill="x", padx=16, pady=(0, 6))
        self.fm_input_mode = StringVar(value="names")
        for value, label in [("names", "File names"), ("text", "Text file with names"), ("extensions", "Extensions")]:
            ttk.Radiobutton(mode_row, text=label, value=value, variable=self.fm_input_mode, command=self.fm_toggle_input_mode).pack(side=LEFT, padx=(0, 12))
        self.fm_manual_frame = ttk.Frame(names)
        self.fm_manual_frame.pack(fill="x", padx=16, pady=(0, 8))
        self.fm_entries_label = ttk.Label(self.fm_manual_frame, text="One filename per line.", foreground=COLORS["muted"])
        self.fm_entries_label.pack(anchor="w", pady=(0, 4))
        self.fm_names = Text(self.fm_manual_frame, height=6, relief="flat")
        self.fm_names.pack(fill="x")
        self.fm_txt_frame = ttk.Frame(names)
        self.fm_txt_preview = StringVar(value="")
        ttk.Button(self.fm_txt_frame, text="Preview TXT", command=self.fm_preview_txt).pack(anchor="w", pady=(0, 4))
        ttk.Label(self.fm_txt_frame, textvariable=self.fm_txt_preview, foreground=COLORS["muted"], justify="left").pack(anchor="w")
            
        settings = ttk.Frame(cards, style="Panel.TFrame")
        settings.pack(fill="x", pady=(0, 10), ipady=4)
        ttk.Label(settings, text="Options", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        
        opts = ttk.Frame(settings)
        opts.pack(fill="x", padx=16, pady=4)
        self.fm_overwrite, self.fm_case, self.fm_partial, self.fm_dry = BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar()
        for var, text in [(self.fm_overwrite, "Overwrite"), (self.fm_case, "Case sensitive"), (self.fm_partial, "Partial match"), (self.fm_dry, "Dry run")]:
            ttk.Checkbutton(opts, text=text, variable=var).pack(side=LEFT, padx=6)
        ttk.Button(opts, text="Clear Files", style="Danger.TButton", command=self.fm_clear_files).pack(side=RIGHT, padx=4)
        ttk.Button(opts, text="Move Files", style="Accent.TButton", command=self.file_mover_run).pack(side=RIGHT, padx=4)
        
        log_pane = ttk.Frame(vsplit)
        vsplit.add(log_pane, weight=1)
        self.fm_log = self._logbox(log_pane, 10)
        self.fm_log.pack(fill=BOTH, expand=True)
        self._log_tools(log_pane, self.fm_log)

    def _c2_tab(self, tab=None):
        if tab is None:
            tab = ttk.Frame(self.tabs, padding=12)
            self.tabs.add(tab, text="C2 Intelligence")
        head = ttk.Frame(tab, style="Panel.TFrame", padding=(12, 8))
        head.pack(fill="x", padx=10, pady=(0, 6))
        ttk.Label(head, text="C2 Collector", font=("Segoe UI Variable Display", 12, "bold"), style="Panel.TLabel").pack(side=LEFT, padx=(0, 10))
        ttk.Label(head, text="Collect, filter, and enrich Command & Control indicators.", foreground=COLORS["muted"], font=("Segoe UI Variable Text", 9)).pack(side=LEFT)
        
        cards = ttk.Frame(tab)
        cards.pack(fill="x", padx=10)
        
        cfg = ttk.Frame(cards, style="Panel.TFrame")
        cfg.pack(fill="x", pady=(0, 6), ipady=2)
        ttk.Label(cfg, text="Data Sources & Limits", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(8, 2))
        
        source_row = ttk.Frame(cfg, style="PanelInner.TFrame")
        source_row.pack(fill="x", padx=12, pady=2)
        for col in range(6):
            source_row.columnconfigure(col, weight=1, uniform="c2src")
        
        self.c2_source_vars, self.c2_limit_vars = {}, {}
        saved_sources = self.settings.get("c2_sources", {})
        saved_limits = self.settings.get("c2_limits", {})
        for i, name in enumerate(C2_SOURCES):
            self.c2_source_vars[name] = BooleanVar(value=bool(saved_sources.get(name, True)))
            self.c2_limit_vars[name] = StringVar(value=str(saved_limits.get(name, 100)))
            frame = ttk.Frame(source_row, style="PanelInner.TFrame")
            frame.grid(row=0, column=i, sticky="w", padx=(0, 6), pady=1)
            ttk.Checkbutton(frame, text=name, variable=self.c2_source_vars[name]).pack(side=LEFT)
            ttk.Entry(frame, textvariable=self.c2_limit_vars[name], width=5).pack(side=LEFT, padx=(4, 0))
            
        opts_row = ttk.Frame(cfg)
        opts_row.pack(fill="x", padx=12, pady=(4, 2))
        self.c2_days = StringVar(value=str(self.settings.get("c2_days", "7")))
        ttk.Label(opts_row, text="Lookback Days:").pack(side=LEFT)
        ttk.Entry(opts_row, textvariable=self.c2_days, width=5).pack(side=LEFT, padx=4)
        ttk.Button(opts_row, text="Save Config", command=self.save_c2_config).pack(side=LEFT, padx=(12, 0))

        folder_row = ttk.Frame(cfg)
        folder_row.pack(fill="x", padx=12, pady=(2, 6))
        self.c2_output_folder = StringVar(value=self.settings.get("c2_output_dir", "outputs"))
        ttk.Label(folder_row, text="Report Folder:").pack(side=LEFT)
        ttk.Entry(folder_row, textvariable=self.c2_output_folder).pack(side=LEFT, fill="x", expand=True, padx=4)
        ttk.Button(folder_row, text="Browse", command=self.pick_c2_output_folder).pack(side=LEFT)
        
        actions = ttk.Frame(cards, style="Panel.TFrame")
        actions.pack(fill="x", pady=(0, 6), ipady=2)
        top = ttk.Frame(actions)
        top.pack(fill="x", padx=12, pady=(8, 8))
        
        self.c2_kind = StringVar(value="IPs")
        self.c2_family = StringVar(value="Any")
        ttk.Label(top, text="Type:").pack(side=LEFT)
        ttk.Combobox(top, textvariable=self.c2_kind, values=["IPs", "Hashes"], state="readonly", width=8).pack(side=LEFT, padx=4)
        ttk.Label(top, text="Family:").pack(side=LEFT, padx=(8, 0))
        ttk.Combobox(top, textvariable=self.c2_family, values=["Any", "Stealer", "Ransomware", "Botnet", "Loader", "RAT"], state="readonly", width=14).pack(side=LEFT, padx=4)
        ttk.Button(top, text="Clear Dashboard", command=self.c2_clear_dashboard).pack(side=LEFT, padx=(12, 4))
        
        ttk.Button(top, text="Export CSV", command=self.c2_export_csv).pack(side=RIGHT, padx=4)
        ttk.Button(top, text="Export Excel", command=self.c2_export_excel).pack(side=RIGHT, padx=4)
        ttk.Button(top, text="Collect Data", style="Accent.TButton", command=self.c2_collect_selected).pack(side=RIGHT, padx=4)
        ttk.Button(top, text="Load TXT", command=self.c2_load_txt).pack(side=RIGHT, padx=4)

        self.c2_progress = ttk.Progressbar(tab, mode="determinate", style="Visible.Horizontal.TProgressbar")
        self.c2_progress.pack(fill="x", padx=10, pady=(0, 6))
        self.c2_text = Text(tab, height=2, relief="flat") # Hidden unless used for manual input

        log_pane = ttk.Frame(tab)
        log_pane.pack(side="bottom", fill="x", padx=10, pady=(6, 0))
        self.c2_log = self._logbox(log_pane, 6)
        self.c2_log.pack(fill=BOTH, expand=True)
        self._log_tools(log_pane, self.c2_log)

        cols = ("indicator", "type", "risk", "ratio", "country", "asn", "as_owner", "engines")
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill=BOTH, expand=True, padx=10)
        self.c2_tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        for c in cols:
            self.c2_tree.heading(c, text=c.replace("_", " ").title())
            self.c2_tree.column(c, width=130 if c != "engines" else 360)
        self.c2_tree.pack(fill=BOTH, expand=True)
        self.c2_tree.tag_configure("HIGH", foreground=COLORS["red"])
        self.c2_tree.tag_configure("MED", foreground="#d97706")
        self.c2_tree.tag_configure("LOW", foreground=COLORS["green"])
        self.c2_tree.tag_configure("CLEAN", foreground=COLORS["green"])
        self.c2_rows = []

    def _settings_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="Settings")
        self._hero_banner(tab, "⚙️", "Application Settings", "Configure theme, language, and API integrations.")
        
        cards = ttk.Frame(tab)
        cards.pack(fill="x", padx=10)
        
        # Appearance Card
        appc = ttk.Frame(cards, style="Panel.TFrame")
        appc.pack(fill="x", pady=(0, 10), ipady=4)
        ttk.Label(appc, text="Appearance", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        
        row = ttk.Frame(appc)
        row.pack(fill="x", padx=16, pady=4)
        ttk.Label(row, text="Theme:").pack(side=LEFT)
        self.theme_name = StringVar(value=self.settings.get("theme", "Light"))
        theme_box = ttk.Combobox(row, textvariable=self.theme_name, values=list(THEMES.keys()), state="readonly", width=18)
        theme_box.pack(side=LEFT, padx=(8, 24))
        theme_box.bind("<<ComboboxSelected>>", lambda _e: self.apply_theme(self.theme_name.get()))
        
        self.font_scale = StringVar(value=self.settings.get("font_scale", "100"))
        ttk.Label(row, text="Font Scale:").pack(side=LEFT)
        font_box = ttk.Combobox(row, textvariable=self.font_scale, values=["90", "100", "110", "125", "150"], state="readonly", width=8)
        font_box.pack(side=LEFT, padx=(8, 24))
        font_box.bind("<<ComboboxSelected>>", lambda _e: self.apply_font_scale())
        
        self.language = StringVar(value=self.settings.get("language", "English"))
        ttk.Label(row, text="Language:").pack(side=LEFT)
        lang_box = ttk.Combobox(row, textvariable=self.language, values=["English", "Spanish", "French", "Russian", "Hindi", "Punjabi"], state="readonly", width=14)
        lang_box.pack(side=LEFT, padx=8)
        lang_box.bind("<<ComboboxSelected>>", lambda _e: self.apply_language())
        
        # API Keys Card
        keysc = ttk.Frame(cards, style="Panel.TFrame")
        keysc.pack(fill="x", pady=(0, 10), ipady=4)
        ttk.Label(keysc, text="API Keys", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        
        self.vt_key = StringVar(value=self.api_keys.get("vt_key", ""))
        self.tf_key = StringVar(value=self.api_keys.get("tf_key", ""))
        self.otx_key = StringVar(value=self.api_keys.get("otx_key", ""))
        self.pd_key = StringVar(value=self.api_keys.get("pd_key", ""))
        self.ha_key = StringVar(value=self.api_keys.get("ha_key", ""))
        
        for label, var in [
            ("VirusTotal API Key", self.vt_key),
            ("ThreatFox / URLhaus / MalwareBazaar API Key", self.tf_key),
            ("AlienVault OTX API Key", self.otx_key),
            ("Pulsedive API Key", self.pd_key),
            ("Hybrid Analysis API Key", self.ha_key)
        ]:
            r = ttk.Frame(keysc)
            r.pack(fill="x", padx=16, pady=4)
            ttk.Label(r, text=label, width=40).pack(side=LEFT)
            ttk.Entry(r, textvariable=var, show="*").pack(side=LEFT, fill="x", expand=True)
            
        act_row = ttk.Frame(cards)
        act_row.pack(fill="x", pady=(10, 0))
        ttk.Button(act_row, text="Save Settings", style="Accent.TButton", command=self.save_settings).pack(side=LEFT)
        ttk.Button(act_row, text="Export Application Log", command=self.export_app_log).pack(side=LEFT, padx=8)
        ttk.Label(act_row, text="No Python packages required. Uses tkinter + Windows native tools.", foreground=COLORS["muted"]).pack(side=RIGHT)

    def _about_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="About")
        
        hero = ttk.Frame(tab)
        hero.pack(fill="x", pady=(40, 30))
        title_row = ttk.Frame(hero)
        title_row.pack(anchor="center")
        self.about_useful_label = ttk.Label(title_row, text="Useful", font=("Segoe UI Variable Display", 32, "bold"))
        self.about_windows_label = ttk.Label(title_row, text="Windows", font=("Segoe UI Variable Display", 32, "bold"), foreground=COLORS["primary"])
        self.about_utils_label = ttk.Label(title_row, text="Utils", font=("Segoe UI Variable Display", 32, "bold"))
        self.about_useful_label.pack(side=LEFT)
        self.about_windows_label.pack(side=LEFT)
        self.about_utils_label.pack(side=LEFT)
        ttk.Label(hero, text=f"Version {APP_VERSION}", font=("Segoe UI", 11), foreground=COLORS["muted"]).pack(anchor="center")
        
        cards = ttk.Frame(tab)
        cards.pack(fill="x", padx=10)
        
        auth = ttk.Frame(cards, style="Panel.TFrame")
        auth.pack(fill="x", pady=(0, 10), ipady=4)
        ttk.Label(auth, text="Author", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        ttk.Label(auth, text="Made by Kuljit Singh").pack(anchor="w", padx=16, pady=(4, 0))
        link = ttk.Label(auth, text="GitHub: https://github.com/therealkuljit", foreground="#3b82f6", cursor="hand2")
        link.pack(anchor="w", padx=16, pady=(4, 12))
        link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/therealkuljit"))
        
        cred = ttk.Frame(cards, style="Panel.TFrame")
        cred.pack(fill="x", pady=(0, 10), ipady=4)
        ttk.Label(cred, text="Credits & Acknowledgements", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        ttk.Label(cred, text="Inspired by and featuring code concepts from ChrisTitusTech WinUtils.").pack(anchor="w", padx=16, pady=(4, 0))
        ctt = ttk.Label(cred, text="https://github.com/ChrisTitusTech/winutil", foreground="#3b82f6", cursor="hand2")
        ctt.pack(anchor="w", padx=16, pady=(4, 12))
        ctt.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/ChrisTitusTech/winutil"))

        legal = ttk.Frame(cards, style="Panel.TFrame")
        legal.pack(fill="x", pady=(0, 10), ipady=4)
        ttk.Label(legal, text="Responsible Use & Compliance", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        legal_text = (
            "Use at your own risk. This tool changes Windows settings, registry values, services, optional features, "
            "package installations, PATH entries, ISO contents, and security-intelligence exports. The author is not "
            "responsible for data loss, system instability, account/API usage, third-party package behavior, malware "
            "handling, investigation outcomes, or policy violations. Create backups and restore points before applying "
            "tweaks. Only submit files, hashes, IPs, domains, and URLs that you are authorized to analyze. The C2 and "
            "VirusTotal features query provider APIs only and must not be used to contact malicious infrastructure. "
            "Follow local law, workplace policy, software licenses, API terms, export-control rules, privacy rules, "
            "and third-party font/license requirements."
        )
        ttk.Label(legal, text=legal_text, wraplength=980, justify="left", foreground=COLORS["muted"]).pack(anchor="w", padx=16, pady=(4, 12))

    def apply_font_scale(self):
        self.settings["font_scale"] = self.font_scale.get()
        self._style()
        save_json(SETTINGS_PATH, self.settings)

    def apply_language(self):
        self.settings["language"] = self.language.get()
        self._build_nav()
        if hasattr(self, "install_selected_button"):
            self.install_selected_button.configure(text="⬇ " + self._("Install Selected"))
        if hasattr(self, "upgrade_selected_button"):
            self.upgrade_selected_button.configure(text="↻ " + self._("Upgrade Selected"))
        self.status.configure(text=self._("Ready"))
        save_json(SETTINGS_PATH, self.settings)

    def apply_theme(self, theme, force=False):
        if not force and self.settings.get("theme") == theme:
            return
        self.settings["theme"] = theme
        old_colors = COLORS.copy()
        set_colors(theme)
        
        try:
            import sv_ttk
            sv_theme = theme.lower()
            if sv_theme not in ("light", "dark"):
                sv_theme = "dark"
            sv_ttk.set_theme(sv_theme)
        except ImportError:
            pass
            
        style = ttk.Style()
        
        bg = "#000000" if theme == "AMOLED" else COLORS["bg"]
        panel = "#000000" if theme == "AMOLED" else COLORS["panel"]
        
        # Safely override backgrounds; _style and _repaint_ttk_foregrounds handle text colors.
        style.configure("TFrame", background=bg)
        style.configure("Panel.TFrame", background=panel)
        style.configure("TLabel", background=bg)
        style.configure("TCheckbutton", background=bg)
        style.configure("TRadiobutton", background=bg)
        
        self.root.configure(bg=bg)
        self._style()
        self._recursive_panel_style(self.root)
        self._repaint_widget_backgrounds(self.root)
        self._repaint_ttk_foregrounds(self.root, old_colors)
        self.set_brand_logo(theme)
        self.update_brand_colors(theme)
        self._restyle_dynamic_widgets(self.root)


        # Update only Text widgets (tk, not ttk) — sv_ttk handles everything else
        self._repaint_text_widgets(self.root)
        save_json(SETTINGS_PATH, self.settings)

    def _repaint_ttk_foregrounds(self, widget, old_colors):
        replacements = {
            old_colors.get("text"): COLORS["text"],
            old_colors.get("muted"): COLORS["muted"],
            old_colors.get("accent"): COLORS["accent"],
            old_colors.get("green"): COLORS["green"],
            old_colors.get("red"): COLORS["red"],
            "#3b82f6": COLORS["accent"],
            "#0f4b99": COLORS["accent"],
            "#d97706": COLORS["accent"],
        }
        try:
            fg = widget.cget("foreground") if "foreground" in widget.keys() else ""
            if fg in replacements:
                widget.configure(foreground=replacements[fg])
        except Exception:
            pass
        for child in widget.winfo_children():
            self._repaint_ttk_foregrounds(child, old_colors)

    def _restyle_dynamic_widgets(self, widget):
        try:
            wtype = widget.winfo_class()
            current_style = widget.cget("style") if "style" in widget.keys() else ""
            text = str(widget.cget("text") if "text" in widget.keys() else "").lower()
            if (wtype == "TButton" or isinstance(widget, RoundedButton)) and current_style != "Nav.TButton":
                danger_words = ("uninstall", "remove", "delete", "reset", "debloat", "clear files", "clear dashboard", "overwrite")
                primary_words = ("install selected", "upgrade selected", "apply selected", "run selected", "create iso", "move files", "collect data", "save settings", "save path", "search", "confirm", "lookup")
                if any(word in text for word in danger_words):
                    widget.configure(style="Danger.TButton")
                elif current_style == "Accent.TButton" or any(word in text for word in primary_words):
                    widget.configure(style="Accent.TButton")
                elif isinstance(widget, RoundedButton):
                    widget._draw()
            elif wtype == "TScrollbar":
                widget.configure(style=("Vertical.TScrollbar" if widget.cget("orient") == "vertical" else "Horizontal.TScrollbar"))
        except Exception:
            pass
        for child in widget.winfo_children():
            self._restyle_dynamic_widgets(child)

    def _repaint_text_widgets(self, widget):
        if isinstance(widget, Text):
            if getattr(widget, "_uwu_logbox", False):
                widget.configure(bg=COLORS["log"], fg=COLORS["log_text"], insertbackground=COLORS["log_text"], highlightbackground=COLORS["line"], highlightcolor=COLORS["accent"])
            else:
                widget.configure(bg=COLORS["panel"], fg=COLORS["text"], insertbackground=COLORS["text"], highlightbackground=COLORS["line"], highlightcolor=COLORS["accent"])
        elif isinstance(widget, RoundedButton):
            widget._draw()
        elif isinstance(widget, ToggleSwitch):
            widget._draw()
        elif isinstance(widget, (ModernCheckbutton, ModernRadiobutton, RoundedInputShell)):
            widget._draw()
        elif isinstance(widget, ThemedProgressbar):
            widget._draw()
        elif isinstance(widget, ThemedScrollbar):
            widget._draw()
        elif isinstance(widget, Canvas):
            widget.configure(background=COLORS["panel"])
        for child in widget.winfo_children():
            self._repaint_text_widgets(child)

    def log(self, box, msg):
        self.q.put((box, msg))

    def _drain(self):
        while not self.q.empty():
            box, msg = self.q.get()
            self.app_log.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
            if box:
                box.insert(END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
                box.see(END)
            self.status.configure(text=msg[:120])
        self.root.after(100, self._drain)

    def thread(self, name, func, *args):
        self.progress.configure(mode="indeterminate")
        self.progress.start(10)
        def runner():
            try:
                func(*args)
            except Exception as e:
                box = next((x for x in reversed(args) if isinstance(x, Text)), None)
                self.log(box, f"ERROR {name}: {e}")
            finally:
                self.root.after(0, lambda: (self.progress.stop(), self.progress.configure(mode="determinate", value=0)))
        threading.Thread(target=runner, daemon=True).start()

    def set_progress(self, current, total):
        if not hasattr(self, "root") or not hasattr(self, "progress"):
            return
        self.root.after(0, lambda: (self.progress.stop(), self.progress.configure(mode="determinate", maximum=max(1, total), value=current)))

    @staticmethod
    def _cmd_summary(cmd):
        """Return a brief, user-friendly description of a command for log display."""
        if not cmd:
            return ""
        exe = Path(cmd[0]).name.lower()
        args = cmd[1:]
        if exe in ("powershell.exe", "powershell"):
            try:
                idx = next(i for i, a in enumerate(args) if a.lower() == "-command")
                script = args[idx + 1] if idx + 1 < len(args) else ""
                user_lines = [l.strip() for l in script.splitlines()
                              if l.strip() and not l.strip().startswith(("function ", "$env:", "#"))]
                label = user_lines[0][:120] if user_lines else "PowerShell script"
            except StopIteration:
                label = " ".join(args)[:120]
            return f"PS> {label}"
        return "$ " + " ".join(cmd)[:200]

    def run_cmd(self, cmd, box):
        self.log(box, self._cmd_summary(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace")
        for line in p.stdout or []:
            stripped = line.rstrip()
            if stripped:
                self.log(box, stripped)
        code = p.wait()
        self.log(box, f"Exit code: {code}")
        return code

    def run_cmd_collect(self, cmd, box):
        self.log(box, self._cmd_summary(cmd))
        lines = []
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace")
        except FileNotFoundError:
            self.log(box, f"Command not found: {cmd[0]}")
            return 127, ""
        for line in p.stdout or []:
            stripped = line.rstrip()
            if stripped:
                lines.append(stripped)
                self.log(box, stripped)
        code = p.wait()
        self.log(box, f"Exit code: {code}")
        return code, "\n".join(lines)

    def run_unelevated(self, cmd, box):
        exe = cmd[0].replace("'", "''")
        args = subprocess.list2cmdline(cmd[1:]).replace("'", "''")
        script = (
            "$shell = New-Object -ComObject Shell.Application; "
            f"$shell.ShellExecute('{exe}', '{args}', '', 'open', 1)"
        )
        self.log(box, "Retrying unelevated because Winget reported a user-scope package.")
        return self.run_cmd(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script], box)

    def run_ps(self, script, box):
        self.thread("PowerShell", self.run_cmd, ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", self.ps_prelude() + "\n" + script], box)

    def ps_prelude(self):
        return rf"""
$env:UWU_PY_ROOT = '{str(ROOT).replace("'", "''")}'
function Invoke-WinUtilExplorerUpdate {{ param([string]$action='refresh') if($action -eq 'restart'){{ Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue; Start-Process explorer.exe }} else {{ rundll32.exe user32.dll,UpdatePerUserSystemParameters 1, True }} }}
function Invoke-WPFFixesNetwork {{ ipconfig /flushdns; netsh winsock reset; netsh int ip reset }}
function Invoke-WPFFixesNTPPool {{ Set-Service w32time -StartupType Automatic; Start-Service w32time; w32tm /config /manualpeerlist:'pool.ntp.org time.nist.gov' /syncfromflags:manual /reliable:yes /update; Restart-Service w32time -Force; w32tm /resync /force }}
function Invoke-WPFFixesUpdate {{ 'bits','wuauserv','appidsvc','cryptsvc' | % {{ Stop-Service $_ -Force -ErrorAction SilentlyContinue }}; Rename-Item $env:SystemRoot\SoftwareDistribution SoftwareDistribution.bak -ErrorAction SilentlyContinue; Rename-Item $env:SystemRoot\System32\catroot2 catroot2.bak -ErrorAction SilentlyContinue; 'bits','wuauserv','appidsvc','cryptsvc' | % {{ Start-Service $_ -ErrorAction SilentlyContinue }} }}
function Invoke-WPFSystemRepair {{ dism /Online /Cleanup-Image /RestoreHealth; sfc /scannow }}
function Invoke-WPFFixesWinget {{ Get-AppxPackage Microsoft.DesktopAppInstaller -AllUsers | % {{ Add-AppxPackage -DisableDevelopmentMode -Register (Join-Path $_.InstallLocation AppxManifest.xml) }} }}
function Invoke-WPFPanelAutologin {{ Start-Process netplwiz.exe }}
function Invoke-WPFSSHServer {{ Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0; Set-Service sshd -StartupType Automatic; Start-Service sshd }}
function Invoke-WPFFeatureInstall {{ optionalfeatures.exe }}
function Invoke-WinUtilRemoveEdge {{ $p = Resolve-Path "$Env:ProgramFiles (x86)\Microsoft\Edge\Application\*\Installer\setup.exe" -ErrorAction SilentlyContinue | Select-Object -Last 1; if($p){{ Start-Process $p -ArgumentList '--uninstall --system-level --force-uninstall --delete-profile' -Wait }} }}
function Invoke-WinutilThemeChange {{ param([string]$theme='Auto') }}
function Invoke-WinUtilInstallPSProfile {{ $p = Join-Path $env:UWU_PY_ROOT 'tools\powershell-profile\setup.ps1'; if(Test-Path $p){{ & $p }} else {{ throw "Profile setup not bundled: $p" }} }}
function Invoke-WinUtilUninstallPSProfile {{ @($PROFILE.CurrentUserCurrentHost,$PROFILE.CurrentUserAllHosts) | ? {{ Test-Path $_ }} | % {{ Remove-Item $_ -Force }} }}
function Invoke-WinUtilClearStartPins {{ $template = Join-Path $env:UWU_PY_ROOT 'assets\start\start2.bin'; if(-not (Test-Path -LiteralPath $template)){{ throw "Blank Start menu template not bundled: $template" }}; $dir = Join-Path $env:LOCALAPPDATA 'Packages\Microsoft.Windows.StartMenuExperienceHost_cw5n1h2txyewy\LocalState'; New-Item -ItemType Directory -Path $dir -Force | Out-Null; $target = Join-Path $dir 'start2.bin'; if(Test-Path -LiteralPath $target){{ $backup = Join-Path $dir ('start2.bin.' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.bak'); Copy-Item -LiteralPath $target -Destination $backup -Force; Write-Host "Backed up current Start menu pins to $backup" }}; Stop-Process -Name StartMenuExperienceHost -Force -ErrorAction SilentlyContinue; Copy-Item -LiteralPath $template -Destination $target -Force; Write-Host "Cleared Start menu pinned apps for current user. Sign out and back in if Windows does not refresh immediately." }}
"""

    def selected_apps(self):
        return [a for a in self.apps if self.app_vars.get(a["key"]) and self.app_vars[a["key"]].get()]

    def install_winget_search(self):
        query = self.winget_search_text.get().strip()
        if not query:
            self.log(self.apps_log, "WARN enter an app name or package ID.")
            return
        self.thread("App search install", self.install_winget_search_worker, query, self.apps_log)

    @staticmethod
    def parse_winget_search(output):
        rows = []
        id_pattern = r"[A-Za-z][A-Za-z0-9_.+-]*\.[A-Za-z0-9_.+-]+|[A-Z0-9]{8,}"
        for line in output.splitlines():
            clean = re.sub(r"[\x00-\x1f]", "", line).strip()
            if not clean or clean.startswith(("-", "Name ", "No package", "The `msstore`")):
                continue
            parts = re.split(r"\s{2,}", clean)
            if len(parts) >= 2 and re.fullmatch(id_pattern, parts[1]):
                version = parts[2].strip() if len(parts) > 2 else ""
                source = parts[-1].strip() if len(parts) > 3 else ""
                if not source and version:
                    tokens = version.rsplit(" ", 1)
                    if len(tokens) == 2 and tokens[1].lower() in {"winget", "msstore"}:
                        version, source = tokens[0], tokens[1]
                rows.append({
                    "name": parts[0].strip(),
                    "id": parts[1].strip(),
                    "version": version,
                    "source": source,
                })
                continue
            match = re.search(rf"(?<!\S)({id_pattern})(?!\S)", clean)
            if match:
                tail = clean[match.end():].strip()
                bits = tail.split()
                source = bits[-1] if bits and bits[-1].lower() in {"winget", "msstore"} else ""
                version_bits = bits[:-1] if source else bits[:1]
                rows.append({
                    "name": clean[:match.start()].strip(),
                    "id": match.group(1).strip(),
                    "version": " ".join(version_bits),
                    "source": source,
                })
        return rows

    @staticmethod
    def parse_choco_search(output):
        rows = []
        for line in output.splitlines():
            clean = re.sub(r"[\x00-\x1f]", "", line).strip()
            if not clean or clean.startswith(("Chocolatey ", "Search ", "Did you know", "packages found", "-")):
                continue
            if "|" in clean:
                name, version = clean.split("|", 1)
                rows.append({"name": name.strip(), "id": name.strip(), "version": version.strip(), "source": "chocolatey"})
                continue
            parts = clean.split()
            if len(parts) >= 2 and re.match(r"^[A-Za-z0-9_.+-]+$", parts[0]):
                rows.append({"name": parts[0], "id": parts[0], "version": parts[1], "source": "chocolatey"})
        return rows

    def install_winget_search_worker(self, query, box):
        winget_code, winget_output = self.run_cmd_collect(["winget", "search", query, "--accept-source-agreements"], box)
        choco_code, choco_output = self.run_cmd_collect(["choco", "search", query, "--limit-output", "--no-color"], box)
        winget_rows = self.parse_winget_search(winget_output) if winget_code == 0 else []
        choco_rows = self.parse_choco_search(choco_output) if choco_code == 0 else []
        rows = [dict(r, provider="winget") for r in winget_rows] + [dict(r, provider="choco") for r in choco_rows]
        if not rows:
            self.log(box, f"No Winget or Chocolatey results found for: {query}")
            return
        q = query.lower()
        choice = next((r for r in rows if r["id"].lower() == q or r["name"].lower() == q), rows[0])
        self.log(box, "Package matches:")
        for r in rows[:10]:
            marker = "selected" if r is choice else "match"
            self.log(box, f"  {marker}: [{r['provider']}] {r['name']}  id={r['id']}  version={r.get('version') or 'unknown'}")
        if choice["provider"] == "choco":
            self.run_cmd(["choco", "install", choice["id"], "-y"], box)
            return
        cmd = ["winget", "install", "-e", "--id", choice["id"], "--silent", "--accept-source-agreements", "--accept-package-agreements"]
        if choice["source"].lower() in {"winget", "msstore"}:
            cmd += ["--source", choice["source"]]
        self.run_cmd(cmd, box)

    def select_recommended(self):
        names = {"Mozilla Firefox", "VLC (Video Player)", "Git", "NodeJS LTS", "Python3", "Notepad++", "VS Codium", "7-Zip"}
        for app in self.apps:
            self.app_vars[app["key"]].set(app["name"] in names)

    def set_app_checks(self, value):
        for var in self.app_vars.values():
            var.set(value)

    def select_tweak_preset(self):
        keys = set(self.tweak_presets.get(self.tweak_preset.get(), []))
        for key, var in self.tweak_vars.items():
            var.set(key in keys)
        self.log(self.tweak_log, f"Loaded tweak preset: {self.tweak_preset.get()} ({len(keys)} recommendations)")

    def clear_selected_tweaks(self):
        defaults = {t["key"]: t["default"] for t in self.tweaks if t["toggle"]}
        for key, var in self.tweak_vars.items():
            var.set(defaults.get(key, False))
        self.log(self.tweak_log, "Cleared selected tweaks.")

    def file_mover_names(self):
        if self.fm_input_mode.get() in {"names", "extensions"}:
            return [x.strip() for x in self.fm_names.get("1.0", END).splitlines() if x.strip()]
        txt = self.fm_txt.get().strip()
        if not txt or not Path(txt).exists():
            return []
        return [x.strip() for x in Path(txt).read_text(encoding="utf-8", errors="ignore").splitlines() if x.strip()]

    def fm_toggle_input_mode(self):
        mode = self.fm_input_mode.get()
        if mode == "text":
            self.fm_manual_frame.pack_forget()
            self.fm_txt_frame.pack(fill="x", padx=16, pady=(0, 8))
            return
        self.fm_txt_frame.pack_forget()
        self.fm_manual_frame.pack(fill="x", padx=16, pady=(0, 8))
        if mode == "extensions":
            self.fm_entries_label.configure(text="One extension per line, with or without a dot.")
        else:
            self.fm_entries_label.configure(text="One filename per line.")

    def fm_current_mode_label(self, mode=None):
        mode = mode or self.fm_input_mode.get()
        return {"names": "file names", "text": "text file with names", "extensions": "extensions"}.get(mode, "file names")

    def fm_preview_txt(self):
        txt = self.fm_txt.get().strip()
        if not txt or not Path(txt).exists():
            self.fm_txt_preview.set("File not found.")
            return
        lines = [x.strip() for x in Path(txt).read_text(encoding="utf-8", errors="ignore").splitlines() if x.strip()]
        preview = "\n".join(lines[:5])
        if len(lines) > 5:
            preview += f"\n... (+{len(lines) - 5} more)"
        self.fm_txt_preview.set(preview)

    def fm_clear_files(self):
        self.fm_names.delete("1.0", END)
        self.fm_txt.set("")
        self.fm_txt_preview.set("")

    def file_mover_run(self):
        src, dst, names = self.fm_src.get().strip(), self.fm_dst.get().strip(), self.file_mover_names()
        if not src or not dst or not names:
            self.log(self.fm_log, f"WARN choose source, destination, and at least one {self.fm_current_mode_label()} entry.")
            return
        self.thread("File mover", self.file_mover_worker, src, dst, names, self.fm_input_mode.get(), self.fm_case.get(), self.fm_partial.get(), self.fm_overwrite.get(), self.fm_dry.get(), self.fm_log)

    @staticmethod
    def file_mover_resolve(names, source_dir, mode, case_sensitive, match_partial):
        try:
            all_files = os.listdir(source_dir)
        except (FileNotFoundError, NotADirectoryError):
            return [(name, None, "src_missing") for name in names]

        if mode == "extensions":
            wanted = {name.strip().lstrip(".") for name in names if name.strip()}
            if not case_sensitive:
                wanted = {name.lower() for name in wanted}
            results, seen = [], set()
            for filename in all_files:
                suffix = Path(filename).suffix.lstrip(".")
                suffix = suffix if case_sensitive else suffix.lower()
                if suffix in wanted and filename not in seen:
                    seen.add(filename)
                    results.append((suffix, str(Path(source_dir) / filename), "found"))
            found_exts = {Path(path).suffix.lstrip(".") if case_sensitive else Path(path).suffix.lstrip(".").lower() for _name, path, status in results if status == "found"}
            for ext in wanted - found_exts:
                results.append((ext, None, "not_found"))
            return results

        results = []
        for name in names:
            name = name.strip()
            if not name:
                continue
            match = None
            for filename in all_files:
                hay, needle = (filename, name) if case_sensitive else (filename.lower(), name.lower())
                hit = needle in hay if match_partial else hay == needle
                if hit:
                    match = filename
                    break
            results.append((name, str(Path(source_dir) / match), "found") if match else (name, None, "not_found"))
        return results

    def file_mover_worker(self, src, dst, names, mode, case, partial, overwrite, dry, box):
        resolved = self.file_mover_resolve(names, src, mode, case, partial)
        moved = skipped = errors = 0
        self.log(box, f"Mode: {self.fm_current_mode_label(mode)}")
        self.log(box, f"Entries queued: {len(names)}")
        if dry:
            self.log(box, "Mode: dry run")
        for i, (name, src_path, status) in enumerate(resolved, 1):
            self.set_progress(i - 1, max(1, len(resolved)))
            if status != "found":
                skipped += 1
                self.log(box, f"SKIP not found: {name}")
                continue
            filename = Path(src_path).name
            dest = Path(dst) / filename
            if dest.exists() and not overwrite:
                skipped += 1
                self.log(box, f"SKIP exists: {filename}")
                continue
            try:
                if not dry:
                    Path(dst).mkdir(parents=True, exist_ok=True)
                    shutil.move(src_path, dest)
                moved += 1
                self.log(box, f"{'DRY-RUN' if dry else 'MOVED'}: {filename}")
            except OSError as e:
                errors += 1
                self.log(box, f"ERROR {filename}: {e}")
        self.set_progress(len(resolved), max(1, len(resolved)))
        self.log(box, f"Done. moved={moved} skipped={skipped} errors={errors}")

    def install_portable_zip(self, app, box):
        dest = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / app["install_dir"]
        tmp = Path(tempfile.mktemp(suffix=".zip"))
        self.log(box, f"Downloading {app['name']} portable zip...")
        try:
            with urllib.request.urlopen(urllib.request.Request(app["portable_zip"], headers={"User-Agent": APP_NAME}), timeout=30) as r, open(tmp, "wb") as f:
                total = int(r.headers.get("Content-Length") or 0)
                done = last_pct = 0
                while True:
                    chunk = r.read(1024 * 256)
                    if not chunk:
                        break
                    f.write(chunk)
                    done += len(chunk)
                    if total:
                        pct = int(done * 100 / total)
                        if pct >= last_pct + 10 or pct == 100:
                            last_pct = pct
                            self.log(box, f"Download progress: {pct}% ({done // 1024} KB / {total // 1024} KB)")
                    elif done // (1024 * 1024) > last_pct:
                        last_pct = done // (1024 * 1024)
                        self.log(box, f"Download progress: {last_pct} MB")
            dest.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(tmp) as zf:
                zf.extractall(dest)
            self.log(box, f"Installed portable app: {dest}")
        finally:
            tmp.unlink(missing_ok=True)

    @staticmethod
    def c2_normalize(value):
        value = str(value or "").strip()
        if re.fullmatch(r"[A-Fa-f0-9]{32}|[A-Fa-f0-9]{40}|[A-Fa-f0-9]{64}", value):
            return value.lower(), "hash"
        try:
            ip = ipaddress.ip_address(value.split(":")[0])
            if ip.version == 4 and not ip.is_private and not ip.is_loopback:
                return str(ip), "ip"
        except ValueError:
            return None, None
        return None, None

    def c2_indicators(self, kind=None):
        out = []
        for line in self.c2_text.get("1.0", END).splitlines():
            value, found_kind = self.c2_normalize(line)
            if value and (not kind or found_kind == kind):
                out.append(value)
        return list(dict.fromkeys(out))

    def c2_load_txt(self):
        path = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if path:
            self.c2_text.insert(END, "\n" + Path(path).read_text(encoding="utf-8", errors="ignore"))

    def c2_limit(self, source):
        try:
            return max(1, min(500, int(self.c2_limit_vars[source].get())))
        except Exception:
            return 100

    @staticmethod
    def c2_days_value(days):
        try:
            return max(1, min(30, int(days or 7)))
        except Exception:
            return 7

    @staticmethod
    def c2_report_stem():
        return "c2_intelligence_" + time.strftime("%Y%m%d_%H%M")

    def c2_output_dir(self):
        folder = self.c2_output_folder.get().strip() if hasattr(self, "c2_output_folder") else self.settings.get("c2_output_dir", "")
        out = bundled_path(folder)
        out.mkdir(parents=True, exist_ok=True)
        return out

    def pick_c2_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.c2_output_folder.set(folder)
            self.settings["c2_output_dir"] = folder
            save_json(SETTINGS_PATH, self.settings)

    def save_c2_config(self):
        self.settings["c2_sources"] = {name: var.get() for name, var in self.c2_source_vars.items()}
        self.settings["c2_limits"] = {name: self.c2_limit(name) for name in C2_SOURCES}
        self.settings["c2_days"] = self.c2_days.get()
        self.settings["c2_output_dir"] = self.c2_output_folder.get().strip() if hasattr(self, "c2_output_folder") else self.settings.get("c2_output_dir", "outputs")
        save_json(SETTINGS_PATH, self.settings)
        self.log(self.c2_log, "C2 config saved.")

    def c2_collect_selected(self):
        sources = [name for name in C2_SOURCES if self.c2_source_vars[name].get()]
        if not sources:
            self.log(self.c2_log, "WARN Select at least one C2 source.")
            return
        family, days = self.c2_family.get().lower(), self.c2_days.get()
        kind = "hash" if self.c2_kind.get() == "Hashes" else "ip"
        limits = {name: self.c2_limit(name) for name in sources}
        self.api_keys["tf_key"] = self.tf_key.get().strip() if hasattr(self, "tf_key") else self.api_keys.get("tf_key", "")
        if not self.api_keys["tf_key"]:
            self.log(self.c2_log, "ERROR Add ThreatFox / abuse.ch API key in Settings first.")
            messagebox.showerror(APP_NAME, "Add ThreatFox / abuse.ch API key in Settings first.")
            return
        self.api_keys["vt_key"] = self.vt_key.get().strip() if hasattr(self, "vt_key") else self.api_keys.get("vt_key", "")
        if not self.api_keys["vt_key"]:
            self.log(self.c2_log, "ERROR Add VirusTotal API key in Settings first.")
            messagebox.showerror(APP_NAME, "Add VirusTotal API key in Settings first.")
            return
        self.c2_rows.clear()
        self.c2_details.clear()
        self.c2_indicator_sources.clear()
        self.c2_indicator_meta.clear()
        self.c2_tree.delete(*self.c2_tree.get_children())
        self.c2_text.delete("1.0", END)
        self.c2_progress.configure(value=0, maximum=max(1, len(sources)))
        self.thread("C2 collect selected", self.c2_collect_selected_worker, sources, family, limits, days, kind, self.c2_log)

    def c2_collect_selected_worker(self, sources, family, limits, days, kind, box):
        all_indicators = []
        for i, source in enumerate(sources, 1):
            self.log(box, f"Collecting {source} {kind}s (limit {limits[source]})...")
            all_indicators += self.c2_collect_worker(source, family, limits[source], days, kind, box)
            self.root.after(0, lambda v=i: self.c2_progress.configure(value=v))
        all_indicators = list(dict.fromkeys(all_indicators))
        if not all_indicators:
            self.log(box, "Collection complete: no matching indicators.")
            return
        stem = self.c2_report_stem()
        out_dir = self.c2_output_dir()
        txt_path = out_dir / f"{stem}.txt"
        xlsx_path = out_dir / f"{stem}.xlsx"
        txt_path.write_text("\n".join(all_indicators) + "\n", encoding="utf-8")
        self.log(box, f"Raw C2 list saved: {txt_path}")
        self.log(box, "Safe enrichment: querying VirusTotal API only; not connecting to collected C2 indicators.")
        self.root.after(0, lambda n=len(all_indicators): self.c2_progress.configure(value=0, maximum=max(1, n)))
        self.c2_enrich_worker(all_indicators, box)
        self.c2_write_excel(xlsx_path)
        self.log(box, f"Enriched Excel report saved: {xlsx_path}")
        self.log(box, "Collection and enrichment complete.")

    @staticmethod
    def _ssl_ctx():
        """Return an SSL context that tolerates missing local CA chains (corporate proxies)."""
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def _urlopen(self, req, timeout=15):
        """urlopen wrapper that falls back to unverified SSL on certificate errors."""
        host = urllib.parse.urlparse(req.full_url).hostname
        if host not in {"threatfox-api.abuse.ch", "urlhaus-api.abuse.ch", "mb-api.abuse.ch"}:
            raise ValueError(f"Blocked non-provider lookup host: {host}")
        try:
            return urllib.request.urlopen(req, timeout=timeout)
        except urllib.error.URLError as exc:
            if "CERTIFICATE_VERIFY_FAILED" in str(exc) or "SSL" in str(exc).upper():
                return urllib.request.urlopen(req, timeout=timeout, context=self._ssl_ctx())
            raise

    def c2_collect_worker(self, source, family, limit, days, kind, box):
        key = self.api_keys.get("tf_key", "")
        found = []
        if source == "ThreatFox":
            payload = {"query": "get_iocs", "days": self.c2_days_value(days)}
            if kind == "ip":
                payload["threat_type"] = "botnet_cc"
            req = urllib.request.Request(
                "https://threatfox-api.abuse.ch/api/v1/",
                data=json.dumps(payload).encode(),
                headers={"Auth-Key": key, "Content-Type": "application/json", "User-Agent": APP_NAME},
                method="POST",
            )
            data = json.loads(self._urlopen(req, timeout=15).read().decode("utf-8", "replace"))
            for x in data.get("data", []):
                found.append((x.get("ioc", ""), {
                    "source": source,
                    "tags": [x.get("malware_printable") or x.get("malware") or ""],
                    "threat_type": x.get("threat_type", ""),
                    "first_seen": x.get("first_seen", ""),
                    "confidence": x.get("confidence_level", ""),
                    "references": [x.get("reference", "")],
                }))
        elif source == "URLhaus":
            req = urllib.request.Request("https://urlhaus-api.abuse.ch/v1/urls/recent/", headers={"Auth-Key": key, "User-Agent": APP_NAME})
            data = json.loads(self._urlopen(req, timeout=15).read().decode("utf-8", "replace"))
            for x in data.get("urls", []):
                refs = [x.get("urlhaus_reference", ""), x.get("url", "")]
                if kind == "hash":
                    for payload in x.get("payloads", []) or []:
                        found.append((payload.get("sha256_hash", ""), {"source": source, "tags": x.get("tags") or [], "first_seen": x.get("date_added", ""), "references": refs}))
                else:
                    found.append((x.get("host") or "", {"source": source, "tags": x.get("tags") or [], "first_seen": x.get("date_added", ""), "references": refs}))
        elif source == "MalwareBazaar":
            req = urllib.request.Request(
                "https://mb-api.abuse.ch/api/v1/",
                data="query=get_recent&selector=time".encode(),
                headers={"Auth-Key": key, "Content-Type": "application/x-www-form-urlencoded", "User-Agent": APP_NAME},
                method="POST",
            )
            data = json.loads(self._urlopen(req, timeout=15).read().decode("utf-8", "replace"))
            for sample in data.get("data", []):
                hay = " ".join([(sample.get("signature") or ""), (sample.get("file_type") or ""), " ".join(t for t in (sample.get("tags") or []) if t)]).lower()
                if family == "any" or family in hay:
                    h = sample.get("sha256_hash", "")
                    if h:
                        found.append((h, {
                            "source": source,
                            "tags": sample.get("tags") or [],
                            "threat_type": sample.get("signature", ""),
                            "first_seen": sample.get("first_seen") or sample.get("first_seen_utc", ""),
                            "references": [sample.get("reporter", "")],
                        }))
        else:
            self.log(box, f"{source}: provider collection is not implemented in this build.")
            return []
        indicators = []
        for item, meta in found:
            indicator, found_kind = self.c2_normalize(item)
            if not indicator or found_kind != kind:
                continue
            indicators.append(indicator)
            self.c2_indicator_sources.setdefault(indicator, set()).add(source)
            current = self.c2_indicator_meta.setdefault(indicator, {})
            for key in ("threat_type", "first_seen", "confidence"):
                if meta.get(key) and not current.get(key):
                    current[key] = str(meta[key])
            for key in ("tags", "references"):
                vals = [str(x) for x in self.as_list(meta.get(key)) if x]
                current[key] = list(dict.fromkeys(self.as_list(current.get(key)) + vals))
        indicators = list(dict.fromkeys(indicators))[:limit]
        self.root.after(0, lambda: self.c2_text.insert(END, "\n" + "\n".join(indicators)))
        self.log(box, f"{source}: collected {len(indicators)} {kind}s.")
        return indicators

    def c2_enrich(self):
        kind = "hash" if self.c2_kind.get() == "Hashes" else "ip"
        indicators = self.c2_indicators(kind)
        if not indicators:
            self.log(self.c2_log, f"WARN Add at least one {kind}.")
            return
        self.api_keys["vt_key"] = self.vt_key.get().strip() if hasattr(self, "vt_key") else self.api_keys.get("vt_key", "")
        if not self.api_keys["vt_key"]:
            self.log(self.c2_log, "ERROR Add VirusTotal API key in Settings first.")
            messagebox.showerror(APP_NAME, "Add VirusTotal API key in Settings first.")
            return
        self.c2_progress.configure(value=0, maximum=max(1, len(indicators)))
        self.thread("C2 VT enrichment", self.c2_enrich_worker, indicators, self.c2_log)

    def c2_clear_dashboard(self):
        self.c2_rows.clear()
        self.c2_details.clear()
        self.c2_indicator_sources.clear()
        self.c2_indicator_meta.clear()
        self.c2_tree.delete(*self.c2_tree.get_children())
        self.c2_text.delete("1.0", END)
        self.c2_progress.configure(value=0)
        self.log(self.c2_log, "C2 dashboard cleared.")

    def c2_enrich_worker(self, indicators, box):
        self.c2_rows.clear()
        self.root.after(0, lambda: self.c2_tree.delete(*self.c2_tree.get_children()))
        for i, indicator in enumerate(indicators, 1):
            is_hash = bool(re.fullmatch(r"[a-f0-9]{32}|[a-f0-9]{40}|[a-f0-9]{64}", indicator))
            data = self.vt_request(("files/" if is_hash else "ip_addresses/") + indicator)
            attr = data.get("data", {}).get("attributes", {})
            stats = attr.get("last_analysis_stats", {})
            mal, sus = stats.get("malicious", 0), stats.get("suspicious", 0)
            total = sum(stats.values()) or 0
            risk = "HIGH" if mal >= 10 else "MED" if mal >= 3 else "LOW" if mal or sus else "CLEAN"
            engines = ", ".join(k for k, v in attr.get("last_analysis_results", {}).items() if v.get("category") in {"malicious", "suspicious"})
            meta = self.c2_indicator_meta.get(indicator, {})
            sources = ", ".join(sorted(self.c2_indicator_sources.get(indicator, [])))
            classification = attr.get("popular_threat_classification") or {}
            tags = self.vt_text_list(meta.get("tags") or attr.get("tags"), 30)
            families = self.vt_text_list([
                classification.get("suggested_threat_label", ""),
                self.vt_text_list(classification.get("popular_threat_name"), 12),
                self.vt_text_list(attr.get("threat_names"), 12),
            ], 20)
            vt_kind = "file" if is_hash else "ip-address"
            self.c2_details[indicator] = {
                "sources": sources,
                "vt_link": f"https://www.virustotal.com/gui/{vt_kind}/{indicator}",
                "detections": mal,
                "ratio": f"{mal}/{total}",
                "suspicious": sus,
                "total": total,
                "engines": engines,
                "country": attr.get("country", ""),
                "asn": attr.get("asn", ""),
                "as_owner": attr.get("as_owner", ""),
                "reputation": attr.get("reputation", ""),
                "families": families,
                "tags": tags,
                "threat_type": meta.get("threat_type", ""),
                "first_seen": meta.get("first_seen") or self.vt_time(attr.get("first_submission_date", "")),
                "confidence": meta.get("confidence", ""),
                "references": "\n".join(self.as_list(meta.get("references"))),
                "last_analysis": self.vt_time(attr.get("last_analysis_date", "")),
            }
            row = [indicator, "hash" if is_hash else "ip", risk, f"{mal}/{total}", attr.get("country", ""), attr.get("asn", ""), attr.get("as_owner", ""), engines]
            self.c2_rows.append(row)
            self.root.after(0, lambda r=row: self.c2_tree.insert("", END, values=r, tags=(r[2],)))
            self.root.after(0, lambda v=i: self.c2_progress.configure(value=v))
            self.log(box, f"{i}/{len(indicators)} {indicator} {risk} {mal}/{total}")
        
        def risk_sort_key(row):
            risk_val = {"HIGH": 0, "MED": 1, "LOW": 2, "CLEAN": 3}.get(row[2], 4)
            try:
                mal = int(row[3].split("/")[0])
            except:
                mal = 0
            return (risk_val, -mal)
        
        self.c2_rows.sort(key=risk_sort_key)
        self.root.after(0, lambda: self.c2_tree.delete(*self.c2_tree.get_children()))
        for r in self.c2_rows:
            self.root.after(0, lambda r=r: self.c2_tree.insert("", END, values=r, tags=(r[2],)))

        self.log(box, "VT enrichment complete.")

    def c2_export_csv(self):
        if not self.c2_rows:
            self.log(self.c2_log, "No C2 results to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=self.c2_report_stem() + ".csv", filetypes=[("CSV", "*.csv")])
        if path:
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["indicator", "type", "risk", "ratio", "country", "asn", "as_owner", "detected_engines"])
                w.writerows(self.c2_rows)
            self.log(self.c2_log, f"Exported: {path}")

    def c2_export_excel(self):
        if not self.c2_rows:
            self.log(self.c2_log, "No C2 results to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=self.c2_report_stem() + ".xlsx", filetypes=[("Excel Workbook", "*.xlsx")])
        if not path:
            return
        self.c2_write_excel(Path(path))
        self.log(self.c2_log, f"Excel exported: {path}")

    def c2_write_excel(self, path):
        kind_label = "Hash" if self.c2_kind.get() == "Hashes" else "IP"
        headers = [
            f"{kind_label} Address" if kind_label == "IP" else "File Hash", "Sources", "VT Link", "VT Detections",
            "VT Detection Ratio", "VT Suspicious", "VT Total Engines", "Detected Engines", "Country", "ASN",
            "AS Owner", "VT Reputation", "Geo Country", "Region", "City", "ZIP", "Latitude", "Longitude",
            "ISP", "Geo Org", "Malware Families", "Tags", "Threat Type", "First Seen", "Confidence",
            "Reference Links", "VT Last Analysis",
        ]
        counts = {risk: sum(1 for r in self.c2_rows if r[2] == risk) for risk in ("HIGH", "MED", "LOW", "CLEAN")}
        summary = [
            [f"C2 {kind_label} Intelligence Report"],
            ["Generated: " + time.strftime("%Y-%m-%d %H:%M:%S")],
            ["Author: Kuljit Singh  |  UsefulWindowsUtils C2 Collector"],
            [],
            [f"Total Unique {kind_label}s", len(self.c2_rows)],
            ["High Risk (>=10 VT)", counts["HIGH"]],
            ["Medium Risk (3-9)", counts["MED"]],
            ["Low Risk (1-2)", counts["LOW"]],
            ["Clean / Undetected", counts["CLEAN"]],
        ]
        report = [headers]
        by_source = {}
        for row in self.c2_rows:
            indicator = row[0]
            d = self.c2_details.get(indicator, {})
            sources = d.get("sources") or ", ".join(sorted(self.c2_indicator_sources.get(indicator, []))) or "Manual"
            for source in [x.strip() for x in sources.split(",") if x.strip()]:
                by_source[source] = by_source.get(source, 0) + 1
            report.append([
                indicator, sources, d.get("vt_link", ""), d.get("detections", row[3].split("/")[0]), d.get("ratio", row[3]),
                d.get("suspicious", ""), d.get("total", ""), d.get("engines", row[7]), d.get("country", row[4]),
                d.get("asn", row[5]), d.get("as_owner", row[6]), d.get("reputation", ""), "", "", "", "", "", "",
                d.get("as_owner", row[6]), d.get("as_owner", row[6]), d.get("families", ""), d.get("tags", ""),
                d.get("threat_type", ""), d.get("first_seen", ""), d.get("confidence", ""), d.get("references", ""),
                d.get("last_analysis", ""),
            ])
        source_rows = [["Source", f"{kind_label} Count"]] + sorted(by_source.items(), key=lambda x: (-x[1], x[0]))
        self.write_xlsx(Path(path), {"Summary": summary, f"C2 {kind_label} Report": report, "By Source": source_rows})

    @staticmethod
    def xlsx_col(n):
        s = ""
        while n:
            n, r = divmod(n - 1, 26)
            s = chr(65 + r) + s
        return s

    def xlsx_style_for_cell(self, sheet_name, row, r, c):
        if sheet_name == "Summary":
            if r == 1:
                return ' s="1"'
            if r in (2, 3):
                return ' s="2"'
            if r >= 5:
                return ' s="6"' if r in (6, 8) and c == 1 else (' s="7"' if r in (6, 8) else (' s="4"' if c == 1 else ' s="5"'))
            return ""
        if sheet_name == "By Source":
            return ' s="20"' if r == 1 else ' s="21"'
        if r == 1:
            return ' s="8"'
        try:
            detections = int(str(row[3]).split("/")[0])
        except Exception:
            detections = 0
        if detections >= 10:
            return ' s="10"' if c == 3 else (' s="11"' if c == 4 else ' s="9"')
        if detections >= 3:
            return ' s="13"' if c == 3 else ' s="12"'
        if detections >= 1:
            return ' s="15"' if c == 3 else ' s="14"'
        return ' s="17"' if c == 3 else ' s="16"'

    def xlsx_sheet(self, sheet_name, rows):
        links = []
        cols = ""
        if sheet_name.startswith("C2 "):
            widths = [20, 16, 36, 14, 18, 14, 14, 42, 10, 9, 24, 14, 16, 16, 14, 8, 10, 10, 22, 22, 24, 24, 16, 20, 12, 34, 18]
            cols = "<cols>" + "".join(f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>' for i, w in enumerate(widths, 1)) + "</cols>"
        elif sheet_name in {"Summary", "By Source"}:
            widths = [30, 22] if sheet_name == "Summary" else [30, 18]
            cols = "<cols>" + "".join(f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>' for i, w in enumerate(widths, 1)) + "</cols>"
        sheet_view = '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>' if sheet_name.startswith("C2 ") or sheet_name == "By Source" else ""
        xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
               f'<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">{sheet_view}{cols}<sheetData>']
        for r, row in enumerate(rows, 1):
            row_attr = f' r="{r}"'
            if sheet_name.startswith("C2 "):
                row_attr += ' ht="24" customHeight="1"' if r == 1 else ' ht="30" customHeight="1"'
            elif sheet_name == "Summary" and r <= 3:
                row_attr += ' ht="22" customHeight="1"'
            xml.append(f"<row{row_attr}>")
            for c, value in enumerate(row, 1):
                cell = f"{self.xlsx_col(c)}{r}"
                style = self.xlsx_style_for_cell(sheet_name, row, r, c)
                if isinstance(value, str) and value.startswith(("http://", "https://")) and "\n" not in value:
                    links.append((cell, value))
                xml.append(f'<c r="{cell}" t="inlineStr"{style}><is><t>{escape(str(value))}</t></is></c>')
            xml.append("</row>")
        xml.append("</sheetData>")
        if sheet_name == "Summary":
            xml.append('<mergeCells count="3"><mergeCell ref="A1:B1"/><mergeCell ref="A2:B2"/><mergeCell ref="A3:B3"/></mergeCells>')
        if sheet_name.startswith("C2 ") and rows:
            xml.append(f'<autoFilter ref="A1:{self.xlsx_col(len(rows[0]))}{len(rows)}"/>')
        if links:
            xml.append("<hyperlinks>")
            for i, (cell, _url) in enumerate(links, 1):
                xml.append(f'<hyperlink ref="{cell}" r:id="rId{i}"/>')
            xml.append("</hyperlinks>")
        xml.append("</worksheet>")
        return "".join(xml)

    def xlsx_sheet_rels(self, rows):
        links = []
        for row in rows:
            for value in row:
                if isinstance(value, str) and value.startswith(("http://", "https://")) and "\n" not in value:
                    links.append(value)
        if not links:
            return ""
        rels = "".join(
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="{escape(url)}" TargetMode="External"/>'
            for i, url in enumerate(links, 1)
        )
        return f'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{rels}</Relationships>'

    def write_xlsx(self, path, sheets):
        names = list(sheets)
        workbook_sheets = "".join(f'<sheet name="{escape(name)}" sheetId="{i}" r:id="rId{i}"/>' for i, name in enumerate(names, 1))
        workbook_rels = "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(names) + 1))
        workbook_rels += f'<Relationship Id="rId{len(names)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        overrides = "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(names) + 1))
        overrides += '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        
        styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <fonts count="12">
        <font><sz val="11"/><color theme="1"/><name val="Arial"/></font>
        <font><b/><sz val="16"/><color rgb="00FFFFFF"/><name val="Arial"/></font>
        <font><sz val="10"/><color rgb="00555555"/><name val="Arial"/></font>
        <font><sz val="9"/><color rgb="00888888"/><name val="Arial"/></font>
        <font><b/><sz val="11"/><color theme="1"/><name val="Arial"/></font>
        <font><sz val="11"/><color theme="1"/><name val="Arial"/></font>
        <font><b/><sz val="10"/><color rgb="00FFFFFF"/><name val="Arial"/></font>
        <font><sz val="9"/><color theme="1"/><name val="Arial"/></font>
        <font><sz val="9"/><color rgb="000563C1"/><name val="Arial"/></font>
        <font><b/><sz val="9"/><color rgb="00CC0000"/><name val="Arial"/></font>
        <font><b/><color rgb="00FFFFFF"/><name val="Arial"/></font>
        <font><sz val="10"/><color theme="1"/><name val="Arial"/></font>
    </fonts>
    <fills count="10">
        <fill><patternFill patternType="none"/></fill>
        <fill><patternFill patternType="gray125"/></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="002E75B6"/><bgColor indexed="64"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="00F0F4FF"/><bgColor indexed="64"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="001F3864"/><bgColor indexed="64"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="00FFCCCC"/><bgColor indexed="64"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="00FFF2CC"/><bgColor indexed="64"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="00FFE8CC"/><bgColor indexed="64"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="00FFFFFF"/><bgColor indexed="64"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="00E2EFDA"/><bgColor indexed="64"/></patternFill></fill>
    </fills>
    <borders count="2">
        <border><left/><right/><top/><bottom/><diagonal/></border>
        <border><left style="thin"><color rgb="00D9E2F3"/></left><right style="thin"><color rgb="00D9E2F3"/></right><top style="thin"><color rgb="00D9E2F3"/></top><bottom style="thin"><color rgb="00D9E2F3"/></bottom><diagonal/></border>
    </borders>
    <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
    <cellXfs count="22">
        <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
        <xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment horizontal="center"/></xf>
        <xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1" applyAlignment="1"><alignment horizontal="center"/></xf>
        <xf numFmtId="0" fontId="3" fillId="0" borderId="0" xfId="0" applyFont="1" applyAlignment="1"><alignment horizontal="center"/></xf>
        <xf numFmtId="0" fontId="4" fillId="3" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
        <xf numFmtId="0" fontId="5" fillId="3" borderId="0" xfId="0" applyFill="1"/>
        <xf numFmtId="0" fontId="4" fillId="5" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
        <xf numFmtId="0" fontId="5" fillId="5" borderId="0" xfId="0" applyFill="1"/>
        <xf numFmtId="0" fontId="6" fillId="4" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
        <xf numFmtId="0" fontId="7" fillId="5" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
        <xf numFmtId="0" fontId="8" fillId="5" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
        <xf numFmtId="0" fontId="9" fillId="5" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
        <xf numFmtId="0" fontId="7" fillId="6" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
        <xf numFmtId="0" fontId="8" fillId="6" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
        <xf numFmtId="0" fontId="7" fillId="7" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
        <xf numFmtId="0" fontId="8" fillId="7" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
        <xf numFmtId="0" fontId="7" fillId="8" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
        <xf numFmtId="0" fontId="8" fillId="8" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
        <xf numFmtId="0" fontId="7" fillId="9" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
        <xf numFmtId="0" fontId="8" fillId="9" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
        <xf numFmtId="0" fontId="10" fillId="4" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment horizontal="center"/></xf>
        <xf numFmtId="0" fontId="11" fillId="0" borderId="0" xfId="0"/>
    </cellXfs>
</styleSheet>"""

        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", f'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>{overrides}</Types>')
            z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
            z.writestr("xl/workbook.xml", f'<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>{workbook_sheets}</sheets></workbook>')
            z.writestr("xl/_rels/workbook.xml.rels", f'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{workbook_rels}</Relationships>')
            z.writestr("xl/styles.xml", styles_xml)
            for i, name in enumerate(names, 1):
                z.writestr(f"xl/worksheets/sheet{i}.xml", self.xlsx_sheet(name, sheets[name]))
                rels = self.xlsx_sheet_rels(sheets[name])
                if rels:
                    z.writestr(f"xl/worksheets/_rels/sheet{i}.xml.rels", rels)

    def package_selected(self, action):
        apps = self.selected_apps()
        if not apps:
            self.log(self.apps_log, "WARN Select at least one app.")
            return
        self.thread(action, self.package_worker, apps, action, self.mode.get(), self.apps_log)

    def package_worker(self, apps, action, mode, box):
        for i, app in enumerate(apps, 1):
            self.set_progress(i - 1, len(apps))
            self.log(box, f"{action.title()} {i}/{len(apps)}: {app['name']}")
            self.log(box, f"Overall progress: {round((i - 1) * 100 / max(1, len(apps)))}%")
            ok = False
            if action == "install" and app.get("portable_zip"):
                self.install_portable_zip(app, box)
                self.set_progress(i, len(apps))
                self.log(box, f"Overall progress: {round(i * 100 / max(1, len(apps)))}%")
                continue
            if "Winget" in mode and app["winget"]:
                cmd = ["winget", action, "-e", "--id", app["winget"], "--silent", "--accept-source-agreements", "--accept-package-agreements"]
                if app.get("source"):
                    cmd += ["--source", app["source"]]
                ok = self.run_cmd(cmd, box) == 0
            if not ok and "Chocolatey" in mode and app["choco"]:
                verb = "install" if action == "install" else "upgrade"
                for pkg in [x.strip() for x in re.split(r"[;,]", app["choco"]) if norm_pkg(x)]:
                    ok = self.run_cmd(["choco", verb, pkg, "-y"], box) == 0 or ok
            self.set_progress(i, len(apps))
            self.log(box, f"Overall progress: {round(i * 100 / max(1, len(apps)))}%")

    def selected_debloat_apps(self):
        return [a for a in self.debloat_apps if self.debloat_vars.get(a["appid"]) and self.debloat_vars[a["appid"]].get()]

    def select_recommended_debloat(self):
        for app in self.debloat_apps:
            if self.debloat_vars.get(app["appid"]):
                self.debloat_vars[app["appid"]].set(app["selected"])

    def clear_debloat_apps(self):
        for var in self.debloat_vars.values():
            var.set(False)

    def remove_selected_debloat(self):
        apps = self.selected_debloat_apps()
        if not apps:
            self.log(self.debloat_log, "WARN Select at least one debloat app first.")
            return
        if messagebox.askyesno("Debloat Windows", f"Remove {len(apps)} selected Windows apps?"):
            self.thread("Debloat selected apps", self.debloat_remove_worker, apps, self.debloat_log)

    def run_ctt_debloat(self):
        if messagebox.askyesno("CTT Debloat", "Run the ChrisTitusTech unwanted pre-installed apps removal?"):
            self.thread("CTT Debloat", self.ctt_debloat_worker, self.debloat_log)

    @staticmethod
    def ps_quote(value):
        return "'" + str(value).replace("'", "''") + "'"

    def appx_remove_script(self, appid):
        app = self.ps_quote(appid)
        return f"""
$app = {app}
$pattern = '*' + $app + '*'
Write-Host "Removing Appx package: $app"
$packages = @(Get-AppxPackage -Name $pattern -AllUsers -ErrorAction SilentlyContinue)
foreach ($pkg in $packages) {{
  Write-Host "Removing installed package $($pkg.PackageFullName)"
  try {{
    Remove-AppxPackage -Package $pkg.PackageFullName -AllUsers -ErrorAction Continue
  }} catch {{
    Remove-AppxPackage -Package $pkg.PackageFullName -ErrorAction Continue
  }}
}}
$provisioned = @(Get-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue | Where-Object {{ $_.DisplayName -like $pattern -or $_.PackageName -like $pattern }})
foreach ($pkg in $provisioned) {{
  Write-Host "Removing provisioned package $($pkg.PackageName)"
  Remove-AppxProvisionedPackage -Online -PackageName $pkg.PackageName -ErrorAction Continue | Out-Host
}}
if (-not $packages -and -not $provisioned) {{
  Write-Host "No matching Appx package found for $app"
}}
"""

    def run_ps_block(self, script, box):
        return self.run_cmd(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", self.ps_prelude() + "\n" + script], box)

    def debloat_remove_worker(self, apps, box):
        for i, app in enumerate(apps, 1):
            self.set_progress(i - 1, len(apps))
            self.log(box, f"Debloat {i}/{len(apps)}: {app['name']} ({app['appid']})")
            if str(app.get("method", "")).lower() == "winget":
                cmd = ["winget", "uninstall", "--id", app["appid"], "--silent", "--accept-source-agreements", "--accept-package-agreements", "--disable-interactivity"]
                code, output = self.run_cmd_collect(cmd, box)
                if code and "user scope cannot be uninstalled when running with administrator privileges" in output.lower():
                    self.run_unelevated(cmd, box)
            else:
                self.run_ps_block(self.appx_remove_script(app["appid"]), box)
            self.set_progress(i, len(apps))

    def ctt_debloat_worker(self, box):
        tweak = load_json("tweaks.json").get("WPFTweaksDeBloat", {})
        apps = [str(x).strip() for x in self.as_list(tweak.get("appx")) if str(x).strip()]
        scripts = [str(x).strip() for x in self.as_list(tweak.get("InvokeScript")) if str(x).strip()]
        self.log(box, f"Running CTT app debloat list ({len(apps)} Appx entries).")
        for i, appid in enumerate(apps, 1):
            self.set_progress(i - 1, max(1, len(apps) + len(scripts)))
            self.log(box, f"CTT Appx {i}/{len(apps)}: {appid}")
            self.run_ps_block(self.appx_remove_script(appid), box)
        for script in scripts:
            self.log(box, "Running CTT cleanup script.")
            self.run_ps_block(script, box)
        self.set_progress(len(apps) + len(scripts), max(1, len(apps) + len(scripts)))

    def refresh_installed(self):
        self.thread("Installed apps", self.refresh_installed_worker, self.installed_log)

    def refresh_installed_worker(self, box):
        self.root.after(0, lambda rows=self.installed_registry_rows(): self.populate_installed(rows, box))

    def populate_installed(self, rows, box):
        self.installed_tree.delete(*self.installed_tree.get_children())
        self.installed_rows.clear()
        self.installed_selected.clear()
        seen = set()
        for row in rows:
            name = row["name"]
            version = row.get("version", "")
            key = name.lower()
            if key in seen:
                continue
            seen.add(key)
            iid = self.installed_tree.insert("", END, values=("☐", name, name, version))
            self.installed_rows[iid] = row
            self.installed_selected[iid] = False
        self.log(box, f"Loaded {len(self.installed_rows)} installed apps.")

    def installed_tree_click(self, event):
        if self.installed_tree.identify_region(event.x, event.y) != "cell":
            return
        iid = self.installed_tree.identify_row(event.y)
        if not iid:
            return "break"
        self.installed_tree.selection_set(iid)
        selected = not self.installed_selected.get(iid, False)
        self.installed_selected[iid] = selected
        values = list(self.installed_tree.item(iid, "values"))
        if values:
            values[0] = "☑" if selected else "☐"
            self.installed_tree.item(iid, values=values)
        return "break"

    def installed_registry_rows(self):
        if not winreg:
            return []
        paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        rows = []
        for root, path in paths:
            try:
                with winreg.OpenKey(root, path) as base:
                    for i in range(winreg.QueryInfoKey(base)[0]):
                        try:
                            with winreg.OpenKey(base, winreg.EnumKey(base, i)) as app:
                                name, _ = winreg.QueryValueEx(app, "DisplayName")
                                version = ""
                                uninstall = ""
                                quiet = ""
                                try:
                                    version, _ = winreg.QueryValueEx(app, "DisplayVersion")
                                except OSError:
                                    pass
                                try:
                                    uninstall, _ = winreg.QueryValueEx(app, "UninstallString")
                                except OSError:
                                    pass
                                try:
                                    quiet, _ = winreg.QueryValueEx(app, "QuietUninstallString")
                                except OSError:
                                    pass
                                if name:
                                    rows.append({
                                        "name": str(name),
                                        "id": str(name),
                                        "version": str(version),
                                        "uninstall": str(uninstall),
                                        "quiet": str(quiet),
                                        "key": winreg.EnumKey(base, i),
                                    })
                        except OSError:
                            pass
            except OSError:
                pass
        return sorted(rows, key=lambda x: x["name"].lower())

    def selected_installed_id(self):
        sel = self.installed_tree.selection()
        return self.installed_rows.get(sel[0], {}).get("id") if sel else None

    def selected_installed_row(self):
        sel = self.installed_tree.selection()
        return self.installed_rows.get(sel[0], {}) if sel else {}

    def selected_installed_rows(self):
        checked = [self.installed_rows[iid] for iid, selected in self.installed_selected.items() if selected and iid in self.installed_rows]
        return checked or ([self.selected_installed_row()] if self.selected_installed_row() else [])

    def upgrade_installed(self):
        pkg = self.selected_installed_id()
        if pkg:
            self.thread("Upgrade selected", self.run_cmd, ["winget", "upgrade", "--name", pkg, "--silent", "--accept-source-agreements", "--accept-package-agreements"], self.installed_log)
        else:
            self.log(self.installed_log, "WARN Select an installed app first.")

    def uninstall_installed(self):
        rows = self.selected_installed_rows()
        if rows:
            names = ", ".join(row["name"] for row in rows[:5])
            suffix = "" if len(rows) <= 5 else f" and {len(rows) - 5} more"
            if messagebox.askyesno("Uninstall", f"Uninstall {len(rows)} selected app(s)?\n\n{names}{suffix}"):
                self.thread("Uninstall selected", self.uninstall_installed_worker, rows, self.installed_log)
        else:
            self.log(self.installed_log, "WARN Select an installed app first.")

    def msi_uninstall_cmd(self, row):
        text = " ".join([row.get("key", ""), row.get("uninstall", ""), row.get("quiet", "")])
        match = re.search(r"\{[0-9A-Fa-f-]{36}\}", text)
        return ["msiexec.exe", "/x", match.group(0), "/qn", "/norestart"] if match else None

    @staticmethod
    def normalize_uninstall_string(command):
        return str(command or "").strip().replace(r"\"", '"')

    @staticmethod
    def split_windows_command(command):
        command = App.normalize_uninstall_string(command)
        if not command:
            return []
        argc = ctypes.c_int()
        ctypes.windll.shell32.CommandLineToArgvW.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_int)]
        ctypes.windll.shell32.CommandLineToArgvW.restype = ctypes.POINTER(ctypes.c_wchar_p)
        ctypes.windll.kernel32.LocalFree.argtypes = [ctypes.c_void_p]
        argv = ctypes.windll.shell32.CommandLineToArgvW(command, ctypes.byref(argc))
        if not argv:
            return []
        try:
            return [argv[i] for i in range(argc.value)]
        finally:
            ctypes.windll.kernel32.LocalFree(argv)

    def run_uninstall_string(self, command, box):
        command = self.normalize_uninstall_string(command)
        if not command:
            return 1, ""
        parts = self.split_windows_command(command)
        if parts and (Path(parts[0]).exists() or shutil.which(parts[0])):
            return self.run_cmd_collect(parts, box)
        return self.run_cmd_collect(["cmd.exe", "/s", "/c", command], box)

    def uninstall_installed_worker(self, row, box):
        if isinstance(row, list):
            for i, item in enumerate(row, 1):
                self.log(box, f"Uninstalling {i}/{len(row)}: {item['name']}")
                self.uninstall_installed_worker(item, box)
            self.root.after(0, self.refresh_installed)
            return
        name = row["name"]
        for label, command in [("quiet registry uninstall", row.get("quiet", "")), ("MSI uninstall", self.msi_uninstall_cmd(row)), ("registry uninstall", row.get("uninstall", ""))]:
            if not command:
                continue
            self.log(box, f"Trying {label}: {name}")
            code, _output = self.run_cmd_collect(command, box) if isinstance(command, list) else self.run_uninstall_string(command, box)
            if code == 0:
                self.log(box, f"Uninstall command completed: {name}")
                return

        cmd = ["winget", "uninstall", "--name", name, "--silent"]
        code, output = self.run_cmd_collect(cmd, box)
        if code == 0:
            return
        if "cannot be uninstalled when running with administrator privileges" in output.lower():
            self.run_unelevated(cmd, box)
            self.log(box, "Started unelevated Winget uninstall for this user-scope package.")
            return
        self.log(box, f"WARN uninstall did not complete: {name}")

    @staticmethod
    def high_risk(tweak):
        hay = (tweak["name"] + " " + tweak["key"] + " " + tweak["desc"]).lower()
        return tweak.get("category") == "Advanced" or any(x in hay for x in ["bitlocker", "edge - remove", "onedrive - remove", "ipv6 - disable", "xbox", "ai - disable", "reserved storage"])

    def apply_selected_tweaks(self):
        items = [t for t in self.tweaks if self.tweak_vars.get(t["key"]) and self.tweak_vars[t["key"]].get() and not t["toggle"]]
        if not items:
            self.log(self.tweak_log, "WARN Select at least one tweak.")
            return
        if not messagebox.askyesno("Confirm Tweaks", "Are you sure you want to apply these system tweaks?"):
            return
        self.thread("Apply tweaks", self.apply_tweaks_worker, items, self.tweak_log)

    def apply_tweaks_worker(self, items, box):
        for i, tw in enumerate(items, 1):
            self.set_progress(i - 1, len(items))
            self.log(box, f"Applying {i}/{len(items)}: {tw['name']}")
            self.apply_tweak(tw, True, box)
            self.set_progress(i, len(items))

    def apply_tweak(self, tw, enabled, box, run_scripts=True):
        for entry in tw["registry"]:
            self.set_registry(entry, enabled, box)
        for entry in tw["service"]:
            self.set_service(entry, enabled, box)
        if run_scripts:
            scripts = tw["invoke"] if enabled else tw["undo"]
            for script in scripts:
                if script and script.strip():
                    self.run_cmd(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", self.ps_prelude() + "\n" + script], box)
        self.log(box, f"OK {tw['name']}")

    def reg_root(self, path):
        roots = {"HKLM": winreg.HKEY_LOCAL_MACHINE, "HKCU": winreg.HKEY_CURRENT_USER, "HKU": winreg.HKEY_USERS}
        m = re.match(r"^(HKLM|HKCU|HKU):\\(.+)$", path, re.I)
        if not m:
            raise ValueError(f"Unsupported registry path: {path}")
        return roots[m.group(1).upper()], m.group(2)

    def reg_value(self, typ, value):
        if value == "<RemoveEntry>":
            return None, None
        typ = (typ or "String").lower()
        if typ == "dword":
            return winreg.REG_DWORD, int(str(value), 0)
        if typ == "qword":
            return winreg.REG_QWORD, int(str(value), 0)
        if typ == "multistring":
            return winreg.REG_MULTI_SZ, value if isinstance(value, list) else str(value).split("|")
        if typ == "expandstring":
            return winreg.REG_EXPAND_SZ, str(value)
        if typ == "binary":
            return winreg.REG_BINARY, bytes(value if isinstance(value, list) else [])
        return winreg.REG_SZ, str(value)

    def set_registry(self, entry, enabled, box):
        if not winreg or not entry:
            return
        value_key = "Value" if enabled else "OriginalValue"
        if value_key not in entry:
            return
        root, subkey = self.reg_root(entry["Path"])
        with winreg.CreateKeyEx(root, subkey, 0, winreg.KEY_SET_VALUE) as key:
            typ, value = self.reg_value(entry.get("Type"), entry.get(value_key))
            if value is None:
                try:
                    winreg.DeleteValue(key, entry["Name"])
                except FileNotFoundError:
                    pass
            else:
                winreg.SetValueEx(key, entry["Name"], 0, typ, value)
        self.log(box, f"Registry: {entry['Path']}\\{entry['Name']}")

    def set_service(self, entry, enabled, box):
        if not entry:
            return
        val = entry.get("StartupType" if enabled else "OriginalType", "")
        start = {"Disable": "disabled", "Disabled": "disabled", "Manual": "demand", "Automatic": "auto"}.get(val, val.lower())
        if start:
            self.run_cmd(["sc.exe", "config", entry["Name"], "start=", start], box)

    def registry_matches(self, entry):
        if not winreg or not entry or "Value" not in entry:
            return None
        root, subkey = self.reg_root(entry["Path"])
        try:
            with winreg.OpenKey(root, subkey) as key:
                current, _typ = winreg.QueryValueEx(key, entry["Name"])
        except OSError:
            current = None
        _typ, wanted = self.reg_value(entry.get("Type"), entry.get("Value"))
        return current == wanted

    def service_matches(self, entry):
        if not winreg or not entry or not entry.get("StartupType"):
            return None
        wanted = {"Disable": 4, "Disabled": 4, "Manual": 3, "Automatic": 2}.get(entry.get("StartupType"))
        if wanted is None:
            return None
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rf"SYSTEM\CurrentControlSet\Services\{entry['Name']}") as key:
                current, _typ = winreg.QueryValueEx(key, "Start")
        except OSError:
            return None
        return current == wanted

    def tweak_enabled(self, tw):
        checks = [self.registry_matches(entry) for entry in tw["registry"]]
        checks += [self.service_matches(entry) for entry in tw["service"]]
        checks = [x for x in checks if x is not None]
        return all(checks) if checks else bool(tw["default"])

    def set_dns(self):
        name = self.dns_name.get()
        data = self.dns.get(name, {})
        if name in {"Default", "DHCP"}:
            script = "Get-NetAdapter | ? Status -eq Up | % { Set-DnsClientServerAddress -InterfaceIndex $_.ifIndex -ResetServerAddresses }"
        else:
            ips = [x for x in data.get("v4", []) + data.get("v6", []) if x]
            quoted = ",".join(f"'{x}'" for x in ips)
            script = f"Get-NetAdapter | ? Status -eq Up | % {{ Set-DnsClientServerAddress -InterfaceIndex $_.ifIndex -ServerAddresses @({quoted}) }}"
        self.run_ps(script, self.tweak_log)

    def hash_file(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        h = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        self.log(self.security_log, f"SHA256 {path}: {h}")

    def hash_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return
        out = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not out:
            return
        out = Path(out)
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["path", "sha256"])
            for p in Path(folder).rglob("*"):
                if p.is_file():
                    try:
                        w.writerow([str(p), hashlib.sha256(p.read_bytes()).hexdigest()])
                    except OSError:
                        pass
        self.log(self.security_log, f"Hash CSV: {out}")

    def netstat(self):
        self.thread("Established connections", self.netstat_worker, self.security_log)

    def netstat_worker(self, box):
        result = run_capture(["netstat", "-ano", "-p", "tcp"])
        rows = [line.strip() for line in result.stdout.splitlines() if "ESTABLISHED" in line]
        self.log(box, f"Established TCP connections: {len(rows)}")
        for line in rows[:300]:
            self.log(box, line)
        if len(rows) > 300:
            self.log(box, f"Showing first 300 of {len(rows)} connections.")

    def processes(self):
        out = ROOT / f"processes-{int(time.time())}.csv"
        result = run_capture(["tasklist", "/v", "/fo", "csv"])
        out.write_text(result.stdout, encoding="utf-8", errors="replace")
        self.log(self.security_log, f"Processes exported: {out}")

    def vt_headers(self):
        key = self.api_keys.get("vt_key", "")
        if not key:
            raise ValueError("VirusTotal API key missing.")
        return {"x-apikey": key}

    def vt_request(self, path, method="GET", body=None, headers=None):
        cache_key = (method, path)
        if method == "GET" and cache_key in self.vt_cache:
            return self.vt_cache[cache_key]
        req = urllib.request.Request("https://www.virustotal.com/api/v3/" + path, data=body, method=method, headers={**self.vt_headers(), "Accept": "application/json", **(headers or {})})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode("utf-8", "replace"))
        if method == "GET":
            self.vt_cache[cache_key] = data
        return data

    def vt_wait_for_analysis_file(self, analysis, box):
        analysis_id = analysis.get("data", {}).get("id", "")
        if not analysis_id:
            return analysis, {}
        sha256 = analysis.get("meta", {}).get("file_info", {}).get("sha256")
        current = analysis
        for attempt in range(1, 16):
            current = self.vt_request("analyses/" + analysis_id)
            attr = current.get("data", {}).get("attributes", {})
            status = attr.get("status", "")
            self.log(box, f"VT analysis status: {status or 'unknown'} ({attempt}/15)")
            sha256 = current.get("meta", {}).get("file_info", {}).get("sha256") or sha256
            if sha256:
                try:
                    file_data = self.vt_request("files/" + sha256)
                    file_attr = file_data.get("data", {}).get("attributes", {})
                    if file_attr:
                        extra = self.vt_extra("files/" + sha256)
                        extra["_analysis_status"] = status
                        return file_data, extra
                except Exception as e:
                    self.log(box, f"VT file report pending for {sha256}: {e}")
            if status == "completed":
                break
            time.sleep(6)
        extra = self.vt_extra("analyses/" + analysis_id)
        extra["_analysis_status"] = current.get("data", {}).get("attributes", {}).get("status", "")
        return current, extra

    def vt_lookup(self):
        self.api_keys["vt_key"] = self.vt_key.get().strip()
        value = self.vt_query.get().strip()
        if not value:
            return
        if re.fullmatch(r"[A-Fa-f0-9]{32,64}", value):
            path = "files/" + value
        elif re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", value):
            path = "ip_addresses/" + value
        elif value.lower().startswith(("http://", "https://")):
            url_id = base64.urlsafe_b64encode(value.encode()).decode().rstrip("=")
            path = "urls/" + url_id
        else:
            path = "domains/" + value
        self.thread("VirusTotal lookup", self.vt_lookup_worker, path, self.vt_log)

    def vt_lookup_worker(self, path, box):
        self.log(box, "Safe lookup: querying VirusTotal API only; not connecting to the submitted IP/domain/URL.")
        self.last_vt = self.vt_request(path)
        self.last_vt_extra = self.vt_extra(path)
        self.log(box, self.vt_report(self.last_vt, self.last_vt_extra))

    def vt_upload(self):
        self.api_keys["vt_key"] = self.vt_key.get().strip()
        path = filedialog.askopenfilename()
        if path:
            if hasattr(self, "vt_selected_file"):
                self.vt_selected_file.set("Selected file: " + Path(path).name)
            self.thread("VirusTotal upload", self.vt_upload_worker, Path(path), self.vt_log)

    def vt_upload_worker(self, path, box):
        self.log(box, "Safe upload: sending selected file to VirusTotal API; no C2 indicator connections.")
        boundary = "----UWU" + hashlib.md5(str(time.time()).encode()).hexdigest()
        data = path.read_bytes()
        body = (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{path.name}\"\r\n"
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode() + data + f"\r\n--{boundary}--\r\n".encode()
        analysis = self.vt_request("files", "POST", body, {"Content-Type": f"multipart/form-data; boundary={boundary}"})
        self.last_vt, self.last_vt_extra = self.vt_wait_for_analysis_file(analysis, box)
        self.last_vt_extra["_upload_name"] = path.name
        self.last_vt_extra["_upload_size"] = path.stat().st_size
        self.log(box, self.vt_report(self.last_vt, self.last_vt_extra))

    def vt_extra(self, path):
        rels = []
        if path.startswith("files/"):
            rels = [
                "behaviours", "dropped_files", "contacted_ips", "contacted_domains",
                "contacted_urls", "execution_parents", "itw_urls", "submissions",
            ]
        elif path.startswith("ip_addresses/"):
            rels = ["communicating_files", "downloaded_files", "urls", "resolutions"]
        elif path.startswith("domains/"):
            rels = ["communicating_files", "downloaded_files", "urls", "resolutions", "subdomains"]
        elif path.startswith("urls/"):
            rels = ["communicating_files", "downloaded_files", "network_location"]
        base = path.split("?", 1)[0].rstrip("/")
        extra = {}
        for rel in rels:
            try:
                extra[rel] = self.vt_request(f"{base}/{rel}?limit=20")
            except Exception as e:
                extra[rel] = {"error": str(e)}
        return extra

    @staticmethod
    def vt_time(value):
        try:
            return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(int(value)))
        except Exception:
            return str(value or "")

    @staticmethod
    def vt_text_list(value, limit=20):
        if not value:
            return ""
        if isinstance(value, dict):
            value = list(value.values())
        if not isinstance(value, list):
            value = [value]
        out = []
        for item in value:
            if isinstance(item, dict):
                out.append(str(item.get("value") or item.get("name") or item.get("id") or item))
            else:
                out.append(str(item))
        return ", ".join(x for x in out[:limit] if x)

    def vt_related_lines(self, title, response, limit=12):
        if not response:
            return []
        if response.get("error"):
            return [f"{title}: unavailable ({response['error']})"]
        rows = response.get("data") or []
        if isinstance(rows, dict):
            rows = [rows]
        lines = [f"{title}: {len(rows)} returned"]
        for item in rows[:limit]:
            attr = item.get("attributes", {}) if isinstance(item, dict) else {}
            stats = attr.get("last_analysis_stats") or {}
            names = self.vt_text_list(attr.get("names") or attr.get("tags") or attr.get("threat_names"), 3)
            label = (
                attr.get("meaningful_name") or attr.get("last_final_url") or attr.get("url") or
                attr.get("ip_address") or attr.get("host_name") or item.get("id", "")
            )
            bits = [str(label)]
            if names:
                bits.append("names/tags: " + names)
            if stats:
                bits.append(f"detections: {stats.get('malicious', 0)}/{sum(stats.values())}")
            if attr.get("first_submission_date"):
                bits.append("first: " + self.vt_time(attr.get("first_submission_date")))
            lines.append("  - " + " | ".join(x for x in bits if x))
        return lines

    def vt_report(self, data, extra=None):
        extra = extra or {}
        obj = data.get("data", {})
        meta = data.get("meta", {})
        attr = obj.get("attributes", {})
        stats = attr.get("last_analysis_stats") or attr.get("stats") or {}
        results = attr.get("last_analysis_results", {})
        hits = [(k, v) for k, v in results.items() if v.get("category") in {"malicious", "suspicious"}]
        total = sum(stats.values()) if stats else len(results)
        lines = [
            "=" * 78,
            "VirusTotal report",
            f"Object: {obj.get('type', '')}  ID: {obj.get('id', '')}",
        ]
        if extra.get("_upload_name"):
            lines.append(f"Selected file: {extra['_upload_name']} ({extra.get('_upload_size', '')} bytes)")
        if extra.get("_analysis_status"):
            lines.append("Analysis status: " + str(extra["_analysis_status"]))
        if obj.get("type") == "analysis":
            lines.append("Analysis status: " + str(attr.get("status", "unknown")))
            file_info = meta.get("file_info") or {}
            for key in ("sha256", "sha1", "md5", "size"):
                if file_info.get(key):
                    lines.append(f"Uploaded file {key.upper()}: {file_info[key]}")
            if not file_info:
                lines.append("Uploaded-file metadata was not returned by VirusTotal yet.")
            lines.append("Detailed file report is pending until VirusTotal exposes the uploaded SHA256 as a file object.")

        names = self.vt_text_list(attr.get("names") or attr.get("meaningful_name") or attr.get("last_final_url"), 30)
        if names:
            lines.append("File / object names: " + names)
        for key in ("md5", "sha1", "sha256", "tlsh", "ssdeep", "vhash", "imphash"):
            if attr.get(key):
                lines.append(f"{key.upper()}: {attr[key]}")
        for key in ("type_description", "magic", "type_tag", "size"):
            if attr.get(key) not in (None, ""):
                lines.append(f"{key.replace('_', ' ').title()}: {attr[key]}")

        date_keys = ("first_submission_date", "first_seen_itw_date", "creation_date", "last_submission_date", "last_analysis_date", "last_modification_date")
        dates = [f"{k.replace('_', ' ').title()}: {self.vt_time(attr.get(k))}" for k in date_keys if attr.get(k)]
        if dates:
            lines += ["", "Dates"] + dates

        if stats:
            lines += [
                "",
                "Detections",
                "Stats: " + ", ".join(f"{k}={v}" for k, v in stats.items()),
                f"Detection ratio: {stats.get('malicious', 0) + stats.get('suspicious', 0)}/{total}",
            ]
        lines.append(f"Reputation: {attr.get('reputation', '')}")
        if hits:
            lines += ["", "Detected engines"]
            for engine, verdict in hits[:100]:
                lines.append(f"  - {engine}: {verdict.get('category')} / {verdict.get('result')}")
        else:
            lines += ["", "Detected engines", "No malicious/suspicious engines in returned analysis."]

        classification = attr.get("popular_threat_classification") or {}
        labels = [
            classification.get("suggested_threat_label", ""),
            self.vt_text_list(classification.get("popular_threat_name"), 20),
            self.vt_text_list(classification.get("popular_threat_category"), 20),
            self.vt_text_list(attr.get("threat_names"), 20),
            self.vt_text_list(attr.get("tags"), 30),
        ]
        labels = [x for x in labels if x]
        if labels:
            lines += ["", "Threat labels, families, and tags"] + labels

        network = []
        for key in ("country", "asn", "as_owner", "network", "registrar", "whois_date", "last_dns_records_date"):
            if attr.get(key) not in (None, ""):
                value = self.vt_time(attr[key]) if key.endswith("_date") else attr[key]
                network.append(f"{key.replace('_', ' ').title()}: {value}")
        if network:
            lines += ["", "Network / registration"] + network

        for title, key in [
            ("Crowdsourced YARA", "crowdsourced_yara_results"),
            ("Crowdsourced IDS", "crowdsourced_ids_results"),
            ("Crowdsourced Sigma", "crowdsourced_sigma_results"),
            ("Sigma analysis", "sigma_analysis_results"),
            ("Sandbox verdicts", "sandbox_verdicts"),
        ]:
            value = attr.get(key)
            if value:
                lines.append("")
                lines.append(title)
                rows = value.values() if isinstance(value, dict) else value
                for item in list(rows)[:20]:
                    if isinstance(item, dict):
                        lines.append("  - " + " | ".join(str(item.get(k, "")) for k in ("rule_name", "rule_title", "sandbox_name", "category", "severity", "malware_classification") if item.get(k)))
                    else:
                        lines.append("  - " + str(item))

        attack_lines = []
        for behavior in (extra.get("behaviours") or {}).get("data", []) if isinstance(extra.get("behaviours"), dict) else []:
            battr = behavior.get("attributes", {})
            for key in ("mitre_attack_techniques", "attack_techniques"):
                for item in battr.get(key, []) or []:
                    if isinstance(item, dict):
                        attack_lines.append("  - " + " | ".join(str(item.get(k, "")) for k in ("id", "signature_description", "technique", "tactic") if item.get(k)))
            if battr.get("sandbox_name"):
                attack_lines.append(f"  - Sandbox: {battr.get('sandbox_name')} | verdict: {battr.get('verdict', '')}")
        if attack_lines:
            lines += ["", "Attack patterns and behavior"] + attack_lines[:60]

        for rel, response in extra.items():
            if rel.startswith("_"):
                continue
            title = rel.replace("_", " ").title()
            lines += [""] + self.vt_related_lines(title, response)

        keys = ", ".join(sorted(attr)[:80])
        if keys:
            lines += ["", "Returned VT attribute keys", keys]
        return "\n".join(str(x) for x in lines if x is not None)

    def vt_export(self):
        if not self.last_vt:
            self.log(self.vt_log, "No VT response to export.")
            return
        out = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text report", "*.txt"), ("JSON", "*.json"), ("All", "*.*")])
        if not out:
            return
        text = self.vt_report(self.last_vt, self.last_vt_extra)
        if out.lower().endswith(".json"):
            Path(out).write_text(json.dumps(self.last_vt, indent=2), encoding="utf-8")
        else:
            Path(out).write_text(text + "\n\nFull VirusTotal JSON\n" + json.dumps(self.last_vt, indent=2), encoding="utf-8")
        self.log(self.vt_log, f"Exported: {out}")

    def add_paths(self):
        entries, seen = [], set()
        for var, path in self.path_vars:
            path = path.strip()
            if var.get() and path and path.lower() not in seen:
                entries.append(path)
                seen.add(path.lower())
        custom = self.custom_path.get().strip()
        if custom and custom.lower() not in seen:
            entries.append(custom)
        self.set_path_entries(self.path_scope.get(), entries)
        self.log(self.path_log, f"{self.path_scope.get()} PATH saved with {len(entries)} entries. Restart terminals/apps to see it.")
        self.custom_path.set("")
        self.load_path_entries()

    def pick_iso_source(self):
        p = filedialog.askopenfilename(filetypes=[("ISO", "*.iso"), ("All", "*.*")])
        if not p:
            p = filedialog.askdirectory()
        if p:
            self.iso_source.set(p)
            # Auto-fill destination
            src_path = Path(p)
            if src_path.is_file():
                self.iso_out.set(str(src_path.parent / f"{src_path.stem}_modified.iso"))
            else:
                self.iso_out.set(str(src_path.parent / f"{src_path.name}_modified.iso"))

    def pick_iso_out(self):
        p = filedialog.asksaveasfilename(defaultextension=".iso", filetypes=[("ISO", "*.iso")])
        if p:
            self.iso_out.set(p)

    def ps_quote(self, value):
        return "'" + str(value).replace("'", "''") + "'"

    def mount_iso(self, source, box):
        script = f"$img=Mount-DiskImage -ImagePath {self.ps_quote(source)} -PassThru; Start-Sleep -Milliseconds 500; ($img | Get-Volume | ? DriveLetter | Select-Object -First 1).DriveLetter"
        result = run_capture(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script])
        drive = result.stdout.strip().splitlines()[-1].strip() if result.stdout.strip() else ""
        if not drive:
            raise ValueError("ISO mounted but no drive letter was returned.")
        root = Path(f"{drive}:\\")
        self.log(box, f"Mounted ISO at {root}")
        return root

    def dismount_iso(self, source, box):
        run_capture(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", f"Dismount-DiskImage -ImagePath {self.ps_quote(source)}"])
        self.log(box, f"Dismounted ISO: {source}")

    def resolve_iso_source(self, source, box):
        src = Path(source)
        if src.is_file() and src.suffix.lower() == ".iso":
            return self.mount_iso(src, box), str(src)
        return src, None

    def iso_image(self, source):
        src = Path(source)
        for name in ("install.wim", "install.esd"):
            p = src / "sources" / name
            if p.exists():
                return p
        raise ValueError("Missing sources\\install.wim or sources\\install.esd")

    def show_iso_editions(self):
        self.thread("Show ISO editions", self.show_iso_editions_worker, self.iso_source.get(), self.iso_log)

    def show_iso_editions_worker(self, source_text, box):
        mounted = None
        try:
            src, mounted = self.resolve_iso_source(source_text, box)
            image = self.iso_image(src)
            self.run_cmd(["dism", "/English", "/Get-ImageInfo", f"/ImageFile:{image}"], box)
        finally:
            if mounted:
                self.dismount_iso(mounted, box)

    def create_iso(self):
        source = self.iso_source.get().strip()
        out = self.iso_out.get().strip()
        if not source:
            self.log(self.iso_log, "ERROR Choose a source ISO or folder first.")
            return
        if not out:
            self.log(self.iso_log, "ERROR Choose an output ISO path first.")
            return
        self.thread("Create ISO", self.create_iso_worker, source, out, self.iso_edition.get(), self.iso_channel.get(), self.iso_log)

    def write_eicfg(self):
        source = self.iso_source.get().strip()
        if not source:
            self.log(self.iso_log, "ERROR Choose a source ISO or folder first.")
            return
        self.thread("Write ei.cfg", self.write_eicfg_worker, source, self.iso_edition.get(), self.iso_channel.get(), self.iso_log)

    def _write_eicfg_to_dir(self, folder, edition, channel, box):
        """Write ei.cfg into a Windows source folder. Returns path written."""
        refs = load_json("offline-references.json")["Iso"]
        ed = next((x for x in refs["Editions"] if x["Name"] == edition), {})
        ch = next((x for x in refs["Channels"] if x["Name"] == channel), {"Channel": "Retail", "VL": 0})
        target = Path(folder) / "sources" / "ei.cfg"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            f"[EditionID]\n{ed.get('EditionID', '')}\n\n[Channel]\n{ch.get('Channel', 'Retail')}\n\n[VL]\n{ch.get('VL', 0)}\n",
            encoding="ascii",
        )
        self.log(box, f"Wrote ei.cfg  edition={ed.get('EditionID', edition)}  channel={ch.get('Channel', channel)}")
        return target

    def write_eicfg_worker(self, source_text, edition, channel, box):
        src = Path(source_text)
        mounted_iso = None
        extract_dir = None
        try:
            if src.is_file() and src.suffix.lower() == ".iso":
                # ISO file supplied – mount it, extract, write ei.cfg, then auto-create ISO
                self.log(box, "ISO file detected – mounting and extracting...")
                mounted_root = self.mount_iso(str(src), box)
                extract_dir = Path(tempfile.mkdtemp(prefix="uwu-eicfg-"))
                mounted_iso = str(src)
                self.log(box, f"Extracting ISO to {extract_dir} ...")
                subprocess.run(
                    ["robocopy", str(mounted_root), str(extract_dir), "/E", "/R:1", "/W:1", "/NFL", "/NDL", "/NJH", "/NJS", "/NP"],
                    stdout=subprocess.DEVNULL,
                )
                self.dismount_iso(mounted_iso, box)
                mounted_iso = None
                self._write_eicfg_to_dir(extract_dir, edition, channel, box)
                # Update source field to the extracted folder
                self.root.after(0, lambda d=extract_dir: self.iso_source.set(str(d)))
                # Auto-chain: if an output ISO path is already set, create the ISO now
                out_text = self.iso_out.get().strip()
                if out_text:
                    self.log(box, f"Auto-creating ISO → {out_text}")
                    self.create_iso_worker(str(extract_dir), out_text, edition, channel, box)
                else:
                    self.log(box, f"Source updated to: {extract_dir}")
                    self.log(box, "Set an output ISO path then click Create ISO.")
            elif src.is_dir():
                self._write_eicfg_to_dir(src, edition, channel, box)
            else:
                raise ValueError(f"Source not found: {source_text}")
        finally:
            if mounted_iso:
                try:
                    self.dismount_iso(mounted_iso, box)
                except Exception:
                    pass
            # Cleanup extract_dir if we did not auto-chain to create_iso. 
            # If we did chain, create_iso_worker takes the directory as its source and leaves it untouched.
            # We'll explicitly trigger cleanup for this directory using after() if it still exists later.
            if extract_dir and extract_dir.exists():
                self.root.after(30000, lambda d=extract_dir: shutil.rmtree(d, ignore_errors=True))

    def create_iso_worker(self, source_text, out_text, edition, channel, box):
        out = Path(out_text)
        src_path = Path(source_text)
        mounted_iso = None
        extract_dir = None
        oscdimg = shutil.which("oscdimg.exe")
        if not oscdimg:
            adk_paths = [
                Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "Windows Kits/10/Assessment and Deployment Kit/Deployment Tools/amd64/Oscdimg/oscdimg.exe",
                Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Windows Kits/10/Assessment and Deployment Kit/Deployment Tools/amd64/Oscdimg/oscdimg.exe"
            ]
            for p in adk_paths:
                if p.exists():
                    oscdimg = str(p)
                    break
        try:
            # ── Resolve source ────────────────────────────────────────────────
            if src_path.is_file() and src_path.suffix.lower() == ".iso":
                if not oscdimg:
                    raise ValueError(
                        "oscdimg.exe not found. Install the Windows ADK (Deployment Tools) "
                        "so that oscdimg.exe is on PATH, then try again."
                    )
                self.log(box, "ISO source detected – mounting and extracting automatically...")
                mounted_root = self.mount_iso(source_text, box)
                extract_dir = Path(tempfile.mkdtemp(prefix="uwu-iso-"))
                mounted_iso = source_text
                self.log(box, f"Copying ISO contents to {extract_dir} ...")
                subprocess.run(
                    ["robocopy", str(mounted_root), str(extract_dir), "/E", "/R:1", "/W:1", "/NFL", "/NDL", "/NJH", "/NJS", "/NP"],
                    stdout=subprocess.DEVNULL,
                )
                self.dismount_iso(mounted_iso, box)
                mounted_iso = None
                work = extract_dir
            elif src_path.is_dir():
                work = src_path
            else:
                raise ValueError(f"Source not found: {source_text}")

            if not oscdimg:
                # No ISO authoring tool – patch ei.cfg and report
                self._write_eicfg_to_dir(work, edition, channel, box)
                self.log(box, "oscdimg.exe not found – ISO not rebuilt. Source folder patched with ei.cfg only.")
                self.log(box, "Install the Windows ADK Deployment Tools to enable full ISO creation.")
                return

            # ── Write ei.cfg into working folder ─────────────────────────────
            self._write_eicfg_to_dir(work, edition, channel, box)

            # ── Build ISO ────────────────────────────────────────────────────
            boot = work / "boot" / "etfsboot.com"
            efi = work / "efi" / "microsoft" / "boot" / "efisys.bin"
            args = [oscdimg, "-m", "-o", "-u2", "-udfver102"]
            if boot.exists() and efi.exists():
                args.append(f"-bootdata:2#p0,e,b{boot}#pEF,e,b{efi}")
            elif boot.exists():
                args.append(f"-b{boot}")
            args += ["-lUWU_WINISO", str(work), str(out)]
            self.log(box, f"Building ISO → {out}")
            self.run_cmd(args, box)
            if out.exists():
                size_mb = out.stat().st_size / 1_048_576
                self.log(box, f"ISO created: {out}  ({size_mb:.0f} MB)")
        finally:
            if mounted_iso:
                try:
                    self.dismount_iso(mounted_iso, box)
                except Exception:
                    pass
            if extract_dir and extract_dir.exists():
                self.log(box, f"Cleaning up temp folder: {extract_dir}")
                shutil.rmtree(extract_dir, ignore_errors=True)

    def save_settings(self):
        self.api_keys["vt_key"] = self.vt_key.get().strip()
        self.api_keys["tf_key"] = self.tf_key.get().strip() if hasattr(self, "tf_key") else self.api_keys.get("tf_key", "")
        self.api_keys["otx_key"] = self.otx_key.get().strip() if hasattr(self, "otx_key") else self.api_keys.get("otx_key", "")
        self.api_keys["pd_key"] = self.pd_key.get().strip() if hasattr(self, "pd_key") else self.api_keys.get("pd_key", "")
        self.api_keys["ha_key"] = self.ha_key.get().strip() if hasattr(self, "ha_key") else self.api_keys.get("ha_key", "")
        self.settings["package_mode"] = self.mode.get() if hasattr(self, "mode") else self.settings.get("package_mode")
        self.settings["theme"] = self.theme_name.get() if hasattr(self, "theme_name") else self.settings.get("theme", "Light")
        self.settings["font_scale"] = self.font_scale.get() if hasattr(self, "font_scale") else self.settings.get("font_scale", "100")
        self.settings["language"] = self.language.get() if hasattr(self, "language") else self.settings.get("language", "English")
        if hasattr(self, "c2_source_vars"):
            self.settings["c2_sources"] = {name: var.get() for name, var in self.c2_source_vars.items()}
            self.settings["c2_limits"] = {name: self.c2_limit(name) for name in C2_SOURCES}
            self.settings["c2_days"] = self.c2_days.get()
            self.settings["c2_output_dir"] = self.c2_output_folder.get().strip() if hasattr(self, "c2_output_folder") else self.settings.get("c2_output_dir", "outputs")
        save_json(SETTINGS_PATH, self.settings)
        save_json(API_KEYS_PATH, self.api_keys)
        messagebox.showinfo(APP_NAME, "Settings saved.")

    def run(self):
        self.root.mainloop()


def self_test():
    check_bundled_files()
    assert brand_logo_path("Light").name == "logo_light.png"
    assert brand_logo_path("Dark").name == "logo_dark.png"
    assert brand_logo_path("AMOLED").name == "logo_amoled.png"
    assert brand_logo_path("Cyberpunk").name == "logo_cyberpunk.png"
    def contrast(fg, bg):
        def lum(color):
            h = color.lstrip("#")
            vals = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
            vals = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in vals]
            return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]
        a, b = lum(fg), lum(bg)
        return (max(a, b) + 0.05) / (min(a, b) + 0.05)
    for theme in THEMES.values():
        assert contrast(theme["text"], theme["panel"]) >= 4.5
        assert contrast(theme["muted"], theme["panel"]) >= 4.5
        assert contrast(theme["log_text"], theme["log"]) >= 4.5
    apps = App.__new__(App)
    apps.settings = {}
    apps.q = queue.Queue()
    apps.apps = App.load_apps(apps)
    apps.tweaks = App.load_tweaks(apps)
    apps.debloat_apps = App.load_debloat_apps(apps)
    assert apps.apps and apps.tweaks and apps.debloat_apps
    assert len({a["winget"].lower() for a in apps.apps if a["winget"]}) == len([a for a in apps.apps if a["winget"]])
    assert any(t["name"] == "Disk Cleanup - Run" for t in apps.tweaks)
    assert any(t["name"] == "Start Menu Pinned Apps - Clear" for t in apps.tweaks)
    assert all(t["category"] != "Advanced" for t in apps.tweaks)
    assert not any(t["key"] == "WPFTweaksDeBloat" for t in apps.tweaks)
    assert any(a["method"] == "WinGet" for a in apps.debloat_apps)
    with tempfile.TemporaryDirectory() as td:
        src, dst = Path(td) / "src", Path(td) / "dst"
        src.mkdir()
        (src / "sample.bin").write_text("x")
        (src / "other.txt").write_text("x")
        assert App.file_mover_resolve(["sample.bin"], str(src), "names", False, False)[0][2] == "found"
        assert App.file_mover_resolve(["sample"], str(src), "names", False, True)[0][2] == "found"
        assert len([x for x in App.file_mover_resolve(["txt"], str(src), "extensions", False, False) if x[2] == "found"]) == 1
        App.file_mover_worker(apps, str(src), str(dst), ["sample.bin"], "names", False, False, False, True, None)
        assert (src / "sample.bin").exists()
        iso = Path(td) / "iso"
        iso.mkdir()
        App.write_eicfg_worker(apps, str(iso), "Pro", "Retail", None)
        assert (iso / "sources" / "ei.cfg").exists()
        xlsx = Path(td) / "c2.xlsx"
        App.write_xlsx(apps, xlsx, {"Summary": [["Total", 1]], "Indicators": [["IP"], ["1.1.1.1"]]})
        with zipfile.ZipFile(xlsx) as z:
            assert "xl/workbook.xml" in z.namelist()
        assert App.c2_days_value("bad") == 7
    print("self-test ok")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        App().run()

