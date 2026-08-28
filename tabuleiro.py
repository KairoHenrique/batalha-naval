"""Tabuleiro 10x10 do Batalha Naval (RF02).

A matriz usa os símbolos do enunciado:
~ agua nao jogada | N navio | X acerto | O agua jogada
"""

from __future__ import annotations

from copy import deepcopy

from utils import (
    COLUNAS,
    SIMBOLO_AGUA,
    SIMBOLO_NAVIO,
    TAMANHO_TABULEIRO,
    formatar_coordenada,
    posicao_dentro_do_tabuleiro,
)

Tabuleiro = list[list[str]]


def criar_tabuleiro() -> Tabuleiro:
    """Gera uma matriz 10x10 preenchida com água (~)."""
    return [
        [SIMBOLO_AGUA for _ in range(TAMANHO_TABULEIRO)]
        for _ in range(TAMANHO_TABULEIRO)
    ]


def copiar_tabuleiro(tabuleiro: Tabuleiro) -> Tabuleiro:
    """Devolve uma cópia independente da matriz."""
    return deepcopy(tabuleiro)


def obter_celula(tabuleiro: Tabuleiro, linha: int, coluna: int) -> str:
    """Lê o símbolo da casa; falha se a coordenada estiver fora."""
    _garantir_limites(linha, coluna)
    return tabuleiro[linha][coluna]


def marcar_celula(
    tabuleiro: Tabuleiro,
    linha: int,
    coluna: int,
    simbolo: str,
) -> None:
    """Altera o símbolo de uma casa válida."""
    _garantir_limites(linha, coluna)
    tabuleiro[linha][coluna] = simbolo


def ocultar_navios(tabuleiro: Tabuleiro) -> Tabuleiro:
    """Cópia do tabuleiro sem revelar N — usada para o lado inimigo."""
    copia = copiar_tabuleiro(tabuleiro)
    for linha in range(TAMANHO_TABULEIRO):
        for coluna in range(TAMANHO_TABULEIRO):
            if copia[linha][coluna] == SIMBOLO_NAVIO:
                copia[linha][coluna] = SIMBOLO_AGUA
    return copia


def montar_linha_de_letras() -> str:
    """Cabeçalho A..J alinhado com as casas."""
    letras = " ".join(COLUNAS)
    return f"    {letras}"


def montar_linha_do_tabuleiro(tabuleiro: Tabuleiro, linha: int) -> str:
    """Uma linha numerada no formato do mockup 6.3."""
    numero = linha + 1
    casas = " ".join(tabuleiro[linha])
    return f"{numero:>2}  {casas}"


def renderizar_tabuleiro(
    tabuleiro: Tabuleiro,
    ocultar: bool = False,
) -> str:
    """Texto completo do tabuleiro 10x10 (RF02 / mockup 6.3)."""
    visivel = ocultar_navios(tabuleiro) if ocultar else tabuleiro
    linhas = [montar_linha_de_letras()]
    for indice_linha in range(TAMANHO_TABULEIRO):
        linhas.append(montar_linha_do_tabuleiro(visivel, indice_linha))
    return "\n".join(linhas)


def imprimir_tabuleiro(tabuleiro: Tabuleiro, ocultar: bool = False) -> None:
    """Imprime o tabuleiro e a legenda do enunciado."""
    print(renderizar_tabuleiro(tabuleiro, ocultar=ocultar))
    print()
    print("Legenda: ~ agua nao jogada | N navio | X acerto | O agua jogada")


def _garantir_limites(linha: int, coluna: int) -> None:
    if not posicao_dentro_do_tabuleiro(linha, coluna):
        tentativa = f"{linha},{coluna}"
        raise ValueError(
            f"Casa ({tentativa}) fora do tabuleiro. "
            f"Valido: {formatar_coordenada(0, 0)} a "
            f"{formatar_coordenada(TAMANHO_TABULEIRO - 1, TAMANHO_TABULEIRO - 1)}."
        )


if __name__ == "__main__":
    from utils import SIMBOLO_ACERTO, SIMBOLO_AGUA_JOGADA

    demonstracao = criar_tabuleiro()
    marcar_celula(demonstracao, 1, 1, SIMBOLO_ACERTO)
    marcar_celula(demonstracao, 2, 3, SIMBOLO_NAVIO)
    marcar_celula(demonstracao, 2, 4, SIMBOLO_NAVIO)
    marcar_celula(demonstracao, 2, 5, SIMBOLO_NAVIO)
    marcar_celula(demonstracao, 2, 6, SIMBOLO_NAVIO)
    marcar_celula(demonstracao, 3, 7, SIMBOLO_AGUA_JOGADA)
    marcar_celula(demonstracao, 5, 2, SIMBOLO_NAVIO)
    marcar_celula(demonstracao, 5, 3, SIMBOLO_NAVIO)

    print("Demonstracao RF02 (python tabuleiro.py)")
    print()
    imprimir_tabuleiro(demonstracao)
