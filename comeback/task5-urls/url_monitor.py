"""
Task 5: Visualización de URLs en Tiempo Real (netstat)
Lee conexiones activas con netstat, resuelve IPs a hostnames,
y resalta en rojo aquellas que estén en la blacklist.
"""
import re
import subprocess
import threading
import time
import tkinter as tk
from tkinter import ttk
import socket

IPV4_RE = re.compile(
    r'\b((?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}'
    r'(?:25[0-5]|2[0-4]\d|[01]?\d\d?))\b'
)

# Subconjunto representativo de dominios bloqueados
# (referencia: github.com/fabriziosalmi/blacklists)
BLACKLIST = {
    "doubleclick.net", "googlesyndication.com", "adnxs.com",
    "scorecardresearch.com", "outbrain.com", "taboola.com",
    "tracking.com", "malware-test.com", "ads.yahoo.com",
}


def resolve_ip(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return ip


def parse_netstat() -> list[tuple[str, str, str, str]]:
    try:
        result = subprocess.run(
            ["netstat", "-n"], capture_output=True, text=True, timeout=5
        )
        rows = []
        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 5 and parts[0] in ("tcp", "tcp6", "udp", "udp6"):
                proto = parts[0]
                local = parts[3]
                foreign = parts[4]
                state = parts[5] if len(parts) > 5 else "—"
                rows.append((proto, local, foreign, state))
        return rows
    except Exception:
        return []


def extract_ip(addr: str) -> str:
    m = IPV4_RE.search(addr)
    return m.group(1) if m else ""


def is_blocked(hostname: str) -> bool:
    domain = hostname.rstrip(".")
    return any(domain == b or domain.endswith("." + b) for b in BLACKLIST)


class App(tk.Tk):
    REFRESH_MS = 3000

    def __init__(self):
        super().__init__()
        self.title("Monitor de URLs en Tiempo Real")
        self.geometry("1020x490")
        self._cache: dict[str, str] = {}
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=4)
        tk.Label(top, text="Monitor de URLs — netstat", font=("Helvetica", 13, "bold")).pack(side=tk.LEFT)
        self.lbl_status = tk.Label(top, text="", fg="gray")
        self.lbl_status.pack(side=tk.RIGHT)

        cols = ("Proto", "Local", "IP Foránea", "URL / Hostname", "Estado", "¿Bloqueada?")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        widths = (70, 180, 140, 270, 110, 100)
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor=tk.CENTER)

        self.tree.tag_configure("blocked", foreground="red")
        self.tree.tag_configure("ok", foreground="green")
        self.tree.tag_configure("unknown", foreground="gray")

        sb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        sb.pack(side=tk.RIGHT, fill=tk.Y, pady=8)

    def _refresh(self):
        threading.Thread(target=self._fetch, daemon=True).start()
        self.after(self.REFRESH_MS, self._refresh)

    def _fetch(self):
        rows = parse_netstat()
        enriched = []
        for proto, local, foreign, state in rows:
            ip = extract_ip(foreign)
            if ip and ip not in self._cache:
                self._cache[ip] = resolve_ip(ip)
            url = self._cache.get(ip, ip) if ip else "—"
            enriched.append((proto, local, ip or "—", url, state))
        self.after(0, self._update_table, enriched)

    def _update_table(self, rows):
        self.tree.delete(*self.tree.get_children())
        for proto, local, ip, url, state in rows:
            blocked = is_blocked(url)
            tag = "blocked" if blocked else ("ok" if ip != "—" else "unknown")
            bl_label = "SÍ ❌" if blocked else "No"
            self.tree.insert("", tk.END,
                             values=(proto, local, ip, url, state, bl_label),
                             tags=(tag,))
        self.lbl_status.config(
            text=f"Actualizado: {time.strftime('%H:%M:%S')} — {len(rows)} conexiones"
        )


if __name__ == "__main__":
    App().mainloop()
