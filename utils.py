"""Funções utilitárias do Batalha Naval (RF05, RN01, RN02).

Toda conversão de coordenada (ex.: C5) e validação de entrada
humana passa por este módulo.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

TAMANHO_TABULEIRO = 10
COLUNAS = "ABCDEFGHIJ"
LINHA_MINIMA = 1
LINHA_MAXIMA = 10

SIMBOLO_AGUA = "~"
SIMBOLO_NAVIO = "N"
SIMBOLO_ACERTO = "X"
SIMBOLO_AGUA_JOGADA = "O"

DIRETORIO_DADOS = Path(__file__).resolve().parent / "data"

Posicao = tuple[int, int]


def limpar_tela() -> None:
    """Limpa o terminal no Windows (cls) ou no Linux/macOS (clear)."""
    comando = "cls" if os.name == "nt" else "clear"
    os.system(comando)


def formatar_tempo(total_segundos: float) -> str:
    """Converte segundos em HH:MM:SS (RF07)."""
    segundos_inteiros = max(0, int(total_segundos))
    horas, resto = divmod(segundos_inteiros, 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def formatar_coordenada(linha: int, coluna: int) -> str:
    """Converte índices 0-based em coordenada de jogo (ex.: 2,2 -> C3)."""
    if not posicao_dentro_do_tabuleiro(linha, coluna):
        raise ValueError("Posicao fora do tabuleiro 10x10.")
    letra = COLUNAS[coluna]
    numero = linha + 1
    return f"{letra}{numero}"


def posicao_dentro_do_tabuleiro(linha: int, coluna: int) -> bool:
    """Indica se a casa (linha, coluna) existe no tabuleiro 10x10."""
    return 0 <= linha < TAMANHO_TABULEIRO and 0 <= coluna < TAMANHO_TABULEIRO


def parse_coordenada(texto: str) -> Posicao:
    """Interpreta Letra+Numero (RN01) e devolve (linha, coluna) 0-based.

    Aceita espaços e minúsculas (ex.: ' c5 ', 'C10').
    Levanta ValueError com mensagem clara se a entrada for inválida.
    """
    bruto = texto.strip().upper().replace(" ", "")
    if len(bruto) < 2 or len(bruto) > 3:
        raise ValueError("Use o formato Letra+Numero (ex.: C5).")

    letra = bruto[0]
    trecho_numero = bruto[1:]

    if letra not in COLUNAS:
        raise ValueError("Coluna invalida. Use letras de A a J.")
    if not trecho_numero.isdigit():
        raise ValueError("Linha invalida. Use numeros de 1 a 10.")

    numero_linha = int(trecho_numero)
    if numero_linha < LINHA_MINIMA or numero_linha > LINHA_MAXIMA:
        raise ValueError("Linha invalida. Use numeros de 1 a 10.")

    linha = numero_linha - 1
    coluna = COLUNAS.index(letra)
    return linha, coluna


def posicao_ja_jogada(tiros: Iterable[Posicao], posicao: Posicao) -> bool:
    """RN02: casa já disparada não pode ser jogada de novo."""
    return posicao in set(tiros)


def mensagem_jogada_repetida(coordenada: str) -> str:
    """Texto exibido quando a jogada não consome a rodada (RN02)."""
    return (
        f"Posicao {coordenada} ja foi jogada. "
        "Informe outra coordenada (a rodada nao foi consumida)."
    )
