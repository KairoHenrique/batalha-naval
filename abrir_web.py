"""Sobe a API e o Next.js e abre o navegador em localhost (GUI extra).

Não substitui o modo texto. Só entra no GitHub depois do aceite do professor.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from utils import limpar_tela

URL_API = "http://127.0.0.1:8000/"
URL_FRONT = "http://127.0.0.1:3000/"
PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_WEB = PASTA_PROJETO / "web"
ESPERA_MAXIMA_SEGUNDOS = 90.0


def abrir_interface_web() -> None:
    """Opção Abrir: garante localhost e abre o navegador sozinho."""
    limpar_tela()
    print("=" * 50)
    print("ABRIR INTERFACE WEB")
    print("=" * 50)
    print()

    if not _preparar_servicos():
        input("\n[ENTER] Voltar ao menu")
        return

    webbrowser.open(URL_FRONT)
    print(f"Navegador aberto em {URL_FRONT}")
    print("O menu texto continua aqui; a partida web e na outra janela.")
    input("\n[ENTER] Voltar ao menu")


def _preparar_servicos() -> bool:
    if not _responder(URL_API):
        if not _iniciar_api():
            return False
    if not _responder(URL_FRONT):
        if not _iniciar_front():
            return False
    print("Aguardando localhost (na primeira vez pode demorar)...", end="", flush=True)
    if not _esperar(URL_API) or not _esperar(URL_FRONT):
        print(" falhou.")
        print("Nao foi possivel subir http://127.0.0.1:3000")
        print("Confira: pip install -r requirements.txt e npm install em web/")
        return False
    print(" ok.")
    return True


def _iniciar_api() -> bool:
    try:
        import fastapi  # noqa: F401
        import uvicorn  # noqa: F401
    except ImportError:
        print("Falta FastAPI/uvicorn. Rode: python -m pip install -r requirements.txt")
        return False
    comando = [
        sys.executable,
        "-m",
        "uvicorn",
        "api:app",
        "--reload",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
    ]
    _disparar(comando, PASTA_PROJETO)
    print("API iniciada na porta 8000.")
    return True


def _iniciar_front() -> bool:
    npm = shutil.which("npm.cmd") or shutil.which("npm")
    if npm is None:
        print("Node.js/npm nao encontrado. Instale o Node para a interface web.")
        return False
    if not (PASTA_WEB / "node_modules").is_dir():
        print("Dependencias do front ausentes. Rode: npm install  (pasta web/)")
        return False
    _disparar([npm, "run", "dev"], PASTA_WEB)
    print("Interface iniciada na porta 3000.")
    return True


def _disparar(comando: list[str], pasta: Path) -> None:
    opcoes: dict = {
        "cwd": str(pasta),
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "stdin": subprocess.DEVNULL,
    }
    if sys.platform == "win32":
        opcoes["creationflags"] = (
            subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.CREATE_NO_WINDOW
            | subprocess.DETACHED_PROCESS
        )
        opcoes["close_fds"] = True
    else:
        opcoes["start_new_session"] = True
    subprocess.Popen(comando, **opcoes)


def _esperar(url: str) -> bool:
    limite = time.monotonic() + ESPERA_MAXIMA_SEGUNDOS
    while time.monotonic() < limite:
        if _responder(url):
            return True
        print(".", end="", flush=True)
        time.sleep(0.5)
    return False


def _responder(url: str) -> bool:
    try:
        with urlopen(url, timeout=1.5):
            return True
    except HTTPError:
        return True
    except (URLError, OSError, TimeoutError):
        return False
