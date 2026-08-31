"""IA do computador (RN05 + bônus T7).

Níveis:
- facil: casa livre ao acaso
- medio: hunt-and-target (após acerto, atira nos vizinhos)
- dificil: hunt-and-target + parity (caça em casas intercaladas)
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from utils import TAMANHO_TABULEIRO, Posicao, posicao_dentro_do_tabuleiro

NIVEIS_VALIDOS = ("facil", "medio", "dificil")


@dataclass
class EstadoIA:
    """Memória de caça da IA entre um tiro e outro."""

    nivel: str
    fila: list[Posicao] = field(default_factory=list)
    acertos_abertos: list[Posicao] = field(default_factory=list)


def criar_estado_ia(nivel: str) -> EstadoIA:
    escolhido = nivel if nivel in NIVEIS_VALIDOS else "medio"
    return EstadoIA(nivel=escolhido)


def casas_disponiveis(tiros_feitos: set[Posicao]) -> list[Posicao]:
    """Todas as casas 10x10 que este jogador ainda não atirou."""
    return [
        (linha, coluna)
        for linha in range(TAMANHO_TABULEIRO)
        for coluna in range(TAMANHO_TABULEIRO)
        if (linha, coluna) not in tiros_feitos
    ]


def escolher_jogada(livres: list[Posicao], estado: EstadoIA) -> Posicao:
    """Escolhe a próxima casa válida. A lógica de cada nível está aqui."""
    if not livres:
        raise RuntimeError("Computador sem casas livres para atirar.")
    if estado.nivel == "facil":
        return random.choice(livres)
    return _escolher_hunt_target(livres, estado)


def registrar_resultado_ia(
    estado: EstadoIA,
    posicao: Posicao,
    resultado: str,
) -> None:
    """Atualiza a fila de alvos depois de água, acerto ou afundado."""
    if estado.nivel == "facil":
        return
    if resultado == "agua":
        return
    if resultado == "afundado":
        estado.fila.clear()
        estado.acertos_abertos.clear()
        return
    _enfileirar_apos_acerto(estado, posicao)


def _escolher_hunt_target(livres: list[Posicao], estado: EstadoIA) -> Posicao:
    livres_set = set(livres)
    while estado.fila:
        alvo = estado.fila.pop(0)
        if alvo in livres_set:
            return alvo
    candidatos = livres
    if estado.nivel == "dificil":
        paridade = [
            casa for casa in livres if (casa[0] + casa[1]) % 2 == 0
        ]
        if paridade:
            candidatos = paridade
    return random.choice(candidatos)


def _enfileirar_apos_acerto(estado: EstadoIA, posicao: Posicao) -> None:
    estado.acertos_abertos.append(posicao)
    vizinhos = _vizinhos_ortogonais(posicao)
    if len(estado.acertos_abertos) >= 2:
        alinhados = _vizinhos_no_eixo(estado.acertos_abertos)
        if alinhados:
            vizinhos = alinhados
    for vizinho in vizinhos:
        if vizinho not in estado.fila:
            estado.fila.append(vizinho)


def _vizinhos_ortogonais(posicao: Posicao) -> list[Posicao]:
    linha, coluna = posicao
    candidatos = (
        (linha - 1, coluna),
        (linha + 1, coluna),
        (linha, coluna - 1),
        (linha, coluna + 1),
    )
    return [casa for casa in candidatos if posicao_dentro_do_tabuleiro(*casa)]


def _vizinhos_no_eixo(acertos: list[Posicao]) -> list[Posicao]:
    """Se os acertos estão na mesma linha ou coluna, estende só esse eixo."""
    linhas = {casa[0] for casa in acertos}
    colunas = {casa[1] for casa in acertos}
    extra: list[Posicao] = []
    if len(linhas) == 1:
        linha = next(iter(linhas))
        colunas_ord = sorted(casa[1] for casa in acertos)
        extra.append((linha, colunas_ord[0] - 1))
        extra.append((linha, colunas_ord[-1] + 1))
    elif len(colunas) == 1:
        coluna = next(iter(colunas))
        linhas_ord = sorted(casa[0] for casa in acertos)
        extra.append((linhas_ord[0] - 1, coluna))
        extra.append((linhas_ord[-1] + 1, coluna))
    return [casa for casa in extra if posicao_dentro_do_tabuleiro(*casa)]
