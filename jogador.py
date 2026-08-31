"""Jogador humano ou computador (tabuleiro próprio, tiros e frota)."""

from __future__ import annotations

from dataclasses import dataclass, field

from navios import Navio, frota_afundada
from tabuleiro import Tabuleiro, criar_tabuleiro
from utils import Posicao


@dataclass
class Jogador:
    """Um lado da partida: frota visível só para o dono."""

    nome: str
    tabuleiro: Tabuleiro
    navios: list[Navio]
    tabuleiro_tiros: Tabuleiro = field(default_factory=criar_tabuleiro)
    tiros_feitos: set[Posicao] = field(default_factory=set)
    eh_computador: bool = False
    acertos: int = 0

    def frota_destruida(self) -> bool:
        """RN04: perdeu quando todos os navios próprios afundaram."""
        return frota_afundada(self.navios)


def criar_jogador(
    nome: str,
    tabuleiro: Tabuleiro,
    navios: list[Navio],
    eh_computador: bool = False,
) -> Jogador:
    """Monta o jogador a partir da frota já posicionada (RF10)."""
    return Jogador(
        nome=nome,
        tabuleiro=tabuleiro,
        navios=navios,
        eh_computador=eh_computador,
    )
