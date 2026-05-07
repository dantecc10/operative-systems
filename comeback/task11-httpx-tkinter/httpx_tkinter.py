"""
Task 11: httpx + asyncio.Semaphore + interfaz Tkinter.
Muestra el progreso en tiempo real de las consultas concurrentes a las URLs de 'urls.txt'.
"""
import asyncio
import threading
import tkinter as tk
from tkinter import ttk
import httpx

MAX_CONCURRENT = 3
TIMEOUT = 10.0
URL_FILE = "urls.txt"


async def fetch(client: httpx.AsyncClient, sem: asyncio.Semaphore,
                url: str, tree: ttk.Treeview, row_id: str) -> None:
    async with sem:
        tree.after(0, lambda: tree.item(row_id, values=(url, "⏳ En curso…", "—"), tags=("running",)))
        try:
            r = await client.get(url, timeout=TIMEOUT, follow_redirects=True)
            tag = "ok" if r.status_code < 400 else "warn"
            icon = "✅" if r.status_code < 400 else "⚠️"
            tree.after(0, lambda: tree.item(row_id, values=(url, f"{icon} {r.status_code}", str(r.status_code)), tags=(tag,)))
        except Exception as e:
            tree.after(0, lambda: tree.item(row_id, values=(url, "❌ Error", str(e)[:70]), tags=("error",)))


async def run_all(urls: list[str], tree: ttk.Treeview, row_ids: list[str]) -> None:
    sem = asyncio.Semaphore(MAX_CONCURRENT)
    async with httpx.AsyncClient() as client:
        await asyncio.gather(*[fetch(client, sem, u, tree, r) for u, r in zip(urls, row_ids)])


def start_scan(urls: list[str], tree: ttk.Treeview,
               row_ids: list[str], btn: tk.Button) -> None:
    # Resetear filas
    for url, row_id in zip(urls, row_ids):
        tree.item(row_id, values=(url, "⏸ Pendiente", "—"), tags=("pending",))

    btn.config(state=tk.DISABLED, text="Escaneando…")

    def worker():
        asyncio.run(run_all(urls, tree, row_ids))
        btn.after(0, lambda: btn.config(state=tk.NORMAL, text="▶ Escanear"))

    threading.Thread(target=worker, daemon=True).start()


def main() -> None:
    with open(URL_FILE) as f:
        urls = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    root = tk.Tk()
    root.title("httpx — Monitor de URLs con Semáforos")
    root.geometry("860x360")

    cols = ("URL", "Estado", "Código / Error")
    tree = ttk.Treeview(root, columns=cols, show="headings")
    for col, w in zip(cols, (440, 160, 220)):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor=tk.W)

    tree.tag_configure("ok",      foreground="green")
    tree.tag_configure("warn",    foreground="orange")
    tree.tag_configure("error",   foreground="red")
    tree.tag_configure("running", foreground="blue")
    tree.tag_configure("pending", foreground="gray")

    row_ids = [tree.insert("", tk.END, values=(u, "⏸ Pendiente", "—"), tags=("pending",)) for u in urls]

    sb = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
    sb.pack(side=tk.RIGHT, fill=tk.Y, pady=8)

    btn = tk.Button(
        root, text="▶ Escanear",
        command=lambda: start_scan(urls, tree, row_ids, btn),
        bg="#1a73e8", fg="white", font=("Helvetica", 11, "bold"), padx=12
    )
    btn.pack(pady=(0, 10))

    root.mainloop()


if __name__ == "__main__":
    main()
