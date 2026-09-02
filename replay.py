"""Histórico da última partida e modo replay (RF11, RF13)."""

from __future__ import annotations

import json
from pathlib import Path

from utils import DIRETORIO_DADOS, formatar_tempo, limpar_tela

ARQUIVO_REPLAY = "ultima_partida.json"
LARGURA = 50
ROTULOS = {
    "agua": "Agua",
    "acerto": "Acerto",
    "afundado": "Afundado",
}


def caminho_replay(pasta: Path | None = None) -> Path:
    destino = pasta if pasta is not None else DIRETORIO_DADOS
    return destino / ARQUIVO_REPLAY


def salvar_ultima_partida(registro: dict, pasta: Path | None = None) -> None:
    """Grava o JSON da última partida encerrada (RF11)."""
    arquivo = caminho_replay(pasta)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    temporario = arquivo.with_suffix(".json.tmp")
    with temporario.open("w", encoding="utf-8") as fluxo:
        json.dump(registro, fluxo, ensure_ascii=True, indent=2)
    temporario.replace(arquivo)


def carregar_ultima_partida(pasta: Path | None = None) -> dict | None:
    """Devolve o replay salvo ou None se não houver arquivo válido."""
    arquivo = caminho_replay(pasta)
    if not arquivo.is_file():
        return None
    try:
        with arquivo.open(encoding="utf-8") as fluxo:
            dados = json.load(fluxo)
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(dados, dict) or "jogadas" not in dados:
        return None
    return dados


def montar_registro_partida(partida: object) -> dict:
    """Serializa o estado final da Partida para JSON (sem PII extra)."""
    duracao = getattr(partida, "duracao_segundos", 0.0) or 0.0
    jogadores = [lado.nome for lado in partida.jogadores]
    return {
        "modo": partida.modo,
        "dificuldade": partida.dificuldade,
        "jogadores": jogadores,
        "vencedor": partida.vencedor,
        "total_jogadas": partida.total_jogadas,
        "duracao_segundos": round(float(duracao), 2),
        "jogadas": list(partida.historico),
    }


def reproduzir_ultima_partida(pasta: Path | None = None) -> None:
    """RF13 / mockup 6.6: Enter avança, Q sai."""
    registro = carregar_ultima_partida(pasta)
    limpar_tela()
    print("=" * LARGURA)
    print("REPLAY")
    print("=" * LARGURA)
    print()
    if registro is None:
        print("Nenhuma partida gravada para reproduzir.")
        input("\n[ENTER] Voltar")
        return
    _rodar_passos(registro)


def formatar_linha_jogada(jogada: dict, total: int) -> str:
    numero = int(jogada.get("numero", 0))
    rotulo = ROTULOS.get(str(jogada.get("resultado", "")), "Jogada")
    return (
        f"Jogada {numero:02d}/{total:02d} - "
        f"{jogada.get('jogador', '?')} - "
        f"{jogada.get('coordenada', '?')} - {rotulo}"
    )


def _rodar_passos(registro: dict) -> None:
    jogadas = list(registro.get("jogadas", []))
    total = len(jogadas) or int(registro.get("total_jogadas", 0))
    print("Reproduzindo replay da ultima partida...")
    print(
        f"Vencedor: {registro.get('vencedor', '?')} | "
        f"Tempo: {formatar_tempo(registro.get('duracao_segundos', 0))}"
    )
    print()
    print("[ENTER] Proxima jogada  [Q] Sair do replay")
    print("-" * LARGURA)
    for jogada in jogadas:
        print(formatar_linha_jogada(jogada, total))
        comando = input().strip().upper()
        if comando == "Q":
            return
    print()
    print("Fim do replay.")
    input("[ENTER] Voltar")
