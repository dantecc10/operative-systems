"""
Task 6: Ejecución de Comandos Bash vía aiohttp
Servidor web asíncrono que ejecuta comandos de bash recibidos vía POST.
Librería base: os / subprocess  |  Framework: aiohttp
"""
import subprocess
from aiohttp import web


async def index(request: web.Request) -> web.Response:
    html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Bash Remoto — aiohttp</title>
  <style>
    body { font-family: monospace; background: #1e1e1e; color: #d4d4d4; padding: 2rem; }
    h2   { color: #569cd6; }
    input[type=text] { width: 60%; padding: 6px; background:#252526; color:#d4d4d4; border:1px solid #555; }
    button { padding: 6px 14px; background:#0e639c; color:#fff; border:none; cursor:pointer; }
    button:hover { background:#1177bb; }
  </style>
</head>
<body>
  <h2>🖥️ Ejecutar Comando Bash</h2>
  <form method="post" action="/run">
    <input type="text" name="cmd" placeholder="ls -la" autofocus />
    <button type="submit">Ejecutar</button>
  </form>
</body>
</html>"""
    return web.Response(text=html, content_type="text/html")


async def run_command(request: web.Request) -> web.Response:
    data = await request.post()
    cmd = data.get("cmd", "").strip()

    if not cmd:
        raise web.HTTPBadRequest(reason="Comando vacío")

    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        output = result.stdout or result.stderr or "(sin salida)"
    except subprocess.TimeoutExpired:
        output = "Error: tiempo de espera agotado (10 s)"
    except Exception as e:
        output = f"Error: {e}"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Resultado</title>
  <style>
    body {{ font-family: monospace; background:#1e1e1e; color:#d4d4d4; padding:2rem; }}
    h2   {{ color:#569cd6; }}
    pre  {{ background:#111; color:#4ec9b0; padding:1rem; white-space:pre-wrap; word-break:break-all; }}
    a    {{ color:#ce9178; }}
  </style>
</head>
<body>
  <h2>$ {cmd}</h2>
  <pre>{output}</pre>
  <a href="/">← Nuevo comando</a>
</body>
</html>"""
    return web.Response(text=html, content_type="text/html")


app = web.Application()
app.router.add_get("/", index)
app.router.add_post("/run", run_command)

if __name__ == "__main__":
    print("Servidor iniciado en http://127.0.0.1:8080")
    web.run_app(app, host="127.0.0.1", port=8080)
