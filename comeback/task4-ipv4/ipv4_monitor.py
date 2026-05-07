"""
Task 4: Visualización de IPv4 en Tiempo Real (netstat)
Reads active IPv4 connections from netstat, displays them in a tkinter table,
and highlights invalid/blocked IPs in red.
"""
import re
import subprocess
import threading
import time
import tkinter as tk
from tkinter import ttk

# Basic IPv4 validation: four octets, each 0-255
IPV4_RE = re.compile(
    r'\b((?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}'
    r'(?:25[0-5]|2[0-4]\d|[01]?\d\d?))\b'
)

# Reserved / non-routable ranges that are always "valid" (private, loopback, etc.)
PRIVATE_RANGES = [
    re.compile(r'^10\.'),
    re.compile(r'^172\.(1[6-9]|2\d|3[01])\.'),
    re.compile(r'^192\.168\.'),
    re.compile(r'^127\.'),
    re.compile(r'^169\.254\.'),
    re.compile(r'^0\.0\.0\.0$'),
]


def is_private(ip: str) -> bool:
    return any(p.match(ip) for p in PRIVATE_RANGES)


def parse_netstat() -> list[tuple[str, str, str, str]]:
    """Return list of (proto, local_addr, foreign_addr, state)."""
    try:
        result = subprocess.run(
            ['netstat', '-n'],
            capture_output=True, text=True, timeout=5
        )
        rows = []
        for line in result.stdout.splitlines():
            parts = line.split()
            # Typical netstat output: Proto Recv-Q Send-Q Local Foreign State
            if len(parts) >= 5 and parts[0] in ('tcp', 'tcp6', 'udp', 'udp6'):
                proto = parts[0]
                local = parts[3]
                foreign = parts[4]
                state = parts[5] if len(parts) > 5 else '—'
                rows.append((proto, local, foreign, state))
        return rows
    except Exception:
        return []


def extract_ip(addr: str) -> str:
    """Extract IP from 'ip:port' or '[ipv6]:port' notation."""
    m = IPV4_RE.search(addr)
    return m.group(1) if m else ''


class App(tk.Tk):
    REFRESH_MS = 2000

    def __init__(self):
        super().__init__()
        self.title("Monitor IPv4 en Tiempo Real")
        self.geometry("850x450")
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=4)
        tk.Label(top, text="Monitor IPv4 — netstat", font=("Helvetica", 13, "bold")).pack(side=tk.LEFT)
        self.lbl_status = tk.Label(top, text="", fg="gray")
        self.lbl_status.pack(side=tk.RIGHT)

        cols = ("Proto", "Local", "Foreign", "IP Foránea", "Estado", "¿Válida?")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        widths = (70, 200, 200, 130, 110, 80)
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor=tk.CENTER)

        self.tree.tag_configure("invalid", foreground="red")
        self.tree.tag_configure("private", foreground="gray")
        self.tree.tag_configure("valid", foreground="green")

        sb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        sb.pack(side=tk.RIGHT, fill=tk.Y, pady=8)

    def _refresh(self):
        threading.Thread(target=self._fetch, daemon=True).start()
        self.after(self.REFRESH_MS, self._refresh)

    def _fetch(self):
        rows = parse_netstat()
        self.after(0, self._update_table, rows)

    def _update_table(self, rows):
        self.tree.delete(*self.tree.get_children())
        for proto, local, foreign, state in rows:
            ip = extract_ip(foreign)
            if not ip:
                tag, valid = "private", "—"
            elif is_private(ip):
                tag, valid = "private", "Privada"
            elif IPV4_RE.match(ip):
                tag, valid = "valid", "Sí"
            else:
                tag, valid = "invalid", "No ❌"
            self.tree.insert("", tk.END, values=(proto, local, foreign, ip, state, valid), tags=(tag,))
        self.lbl_status.config(text=f"Actualizado: {time.strftime('%H:%M:%S')} — {len(rows)} conexiones")


if __name__ == "__main__":
    App().mainloop()
