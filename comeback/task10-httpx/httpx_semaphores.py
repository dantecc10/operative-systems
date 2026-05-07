"""
Task 10: Exploración concurrente de URLs con httpx y asyncio.Semaphore.
Lee las URLs de 'urls.txt' y las consulta de forma concurrente,
controlando el máximo de peticiones simultáneas con un semáforo.
"""
import asyncio
import httpx

MAX_CONCURRENT = 3
TIMEOUT = 10.0
URL_FILE = "urls.txt"

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
RESET  = "\033[0m"


async def fetch(client: httpx.AsyncClient, sem: asyncio.Semaphore, url: str) -> None:
    async with sem:                          # sección crítica: máx MAX_CONCURRENT
        try:
            r = await client.get(url, timeout=TIMEOUT, follow_redirects=True)
            color = GREEN if r.status_code < 400 else YELLOW
            print(f"{color}[{r.status_code}] {url}{RESET}")
        except Exception as e:
            print(f"{RED}[ERR] {url} — {e}{RESET}")


async def main() -> None:
    with open(URL_FILE) as f:
        urls = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    sem = asyncio.Semaphore(MAX_CONCURRENT)
    async with httpx.AsyncClient() as client:
        await asyncio.gather(*[fetch(client, sem, url) for url in urls])


if __name__ == "__main__":
    asyncio.run(main())
