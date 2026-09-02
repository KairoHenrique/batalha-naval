"""Estatísticas persistidas de desempenho (RF12).

Agrega partidas, vitórias, tiros e acertos por apelido da sessão.
Não grava dado pessoal além do nome informado no menu (LGPD: minimização).
"""

from __future__ import annotations

import json
from pathlib import Path

from utils import DIRETORIO_DADOS, limpar_tela

ARQUIVO_ESTATISTICAS = "estatisticas.json"
LARGURA = 50


def caminho_estatisticas(pasta: Path | None = None) -> Path:
    destino = pasta if pasta is not None else DIRETORIO_DADOS
    return destino / ARQUIVO_ESTATISTICAS


def carregar_estatisticas(pasta: Path | None = None) -> dict:
    """Lê o JSON; arquivo ausente ou corrompido vira dicionário vazio."""
    arquivo = caminho_estatisticas(pasta)
    if not arquivo.is_file():
        return {"jogadores": {}}
    try:
        with arquivo.open(encoding="utf-8") as fluxo:
            dados = json.load(fluxo)
    except (OSError, json.JSONDecodeError):
        return {"jogadores": {}}
    if not isinstance(dados, dict) or "jogadores" not in dados:
        return {"jogadores": {}}
    return dados


def registrar_desempenho(
    nome: str,
    acertos: int,
    tiros: int,
    venceu: bool,
    pasta: Path | None = None,
) -> None:
    """Soma mais uma partida encerrada para o apelido (RF12)."""
    apelido = nome.strip()[:40] or "Jogador"
    dados = carregar_estatisticas(pasta)
    ficha = dados["jogadores"].setdefault(
        apelido,
        {"partidas": 0, "vitorias": 0, "tiros": 0, "acertos": 0},
    )
    ficha["partidas"] += 1
    ficha["vitorias"] += 1 if venceu else 0
    ficha["tiros"] += max(0, tiros)
    ficha["acertos"] += max(0, acertos)
    _salvar_estatisticas(dados, pasta)


def calcular_aproveitamento(acertos: int, tiros: int) -> float:
    """Percentual de acertos; 0 se ainda não atirou."""
    if tiros <= 0:
        return 0.0
    return (acertos / tiros) * 100.0


def exibir_estatisticas(pasta: Path | None = None) -> None:
    """Tela do menu (opção 2): partidas, acertos e aproveitamento."""
    limpar_tela()
    print("=" * LARGURA)
    print("ESTATISTICAS")
    print("=" * LARGURA)
    print()
    dados = carregar_estatisticas(pasta)
    jogadores = dados.get("jogadores", {})
    if not jogadores:
        print("Ainda nao ha partidas registradas.")
        input("\n[ENTER] Voltar ao menu")
        return
    print(f"{'Jogador':<16} {'Part.':>6} {'Vit.':>6} {'Tiros':>7} {'Acertos':>8} {'Aprov.':>8}")
    print("-" * LARGURA)
    for nome, ficha in sorted(jogadores.items()):
        aproveitamento = calcular_aproveitamento(
            ficha.get("acertos", 0),
            ficha.get("tiros", 0),
        )
        print(
            f"{nome[:16]:<16} {ficha.get('partidas', 0):>6} "
            f"{ficha.get('vitorias', 0):>6} {ficha.get('tiros', 0):>7} "
            f"{ficha.get('acertos', 0):>8} {aproveitamento:>7.1f}%"
        )
    input("\n[ENTER] Voltar ao menu")


def _salvar_estatisticas(dados: dict, pasta: Path | None = None) -> None:
    arquivo = caminho_estatisticas(pasta)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    temporario = arquivo.with_suffix(".json.tmp")
    with temporario.open("w", encoding="utf-8") as fluxo:
        json.dump(dados, fluxo, ensure_ascii=True, indent=2)
    temporario.replace(arquivo)
