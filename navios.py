"""Navios e posicionamento automático (RF03, RF04, RF10).

Frota interpretada do enunciado: 2 grandes (4 casas) + 3 pequenos (2 casas).
O posicionamento é aleatório, horizontal ou vertical, sem sair do 10x10
e sem sobrepor outro navio. A conferência permite confirmar ou gerar de novo.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from tabuleiro import (
    Tabuleiro,
    criar_tabuleiro,
    imprimir_tabuleiro,
    marcar_celula,
    obter_celula,
)
from utils import (
    SIMBOLO_AGUA,
    SIMBOLO_NAVIO,
    TAMANHO_TABULEIRO,
    Posicao,
    formatar_coordenada,
    limpar_tela,
)

TIPO_PEQUENO = "pequeno"
TIPO_GRANDE = "grande"
TAMANHO_PEQUENO = 2
TAMANHO_GRANDE = 4

COMPOSICAO_FROTA: tuple[tuple[str, int], ...] = (
    (TIPO_GRANDE, TAMANHO_GRANDE),
    (TIPO_GRANDE, TAMANHO_GRANDE),
    (TIPO_PEQUENO, TAMANHO_PEQUENO),
    (TIPO_PEQUENO, TAMANHO_PEQUENO),
    (TIPO_PEQUENO, TAMANHO_PEQUENO),
)

MAX_TENTATIVAS_POR_NAVIO = 200
MAX_TENTATIVAS_FROTA = 80


@dataclass
class Navio:
    """Um navio no tabuleiro; afunda quando todas as casas forem atingidas."""

    tipo: str
    tamanho: int
    posicoes: list[Posicao]
    acertos: set[Posicao] = field(default_factory=set)

    def esta_afundado(self) -> bool:
        """RN03: afundado só com todas as posições atingidas."""
        return all(casa in self.acertos for casa in self.posicoes)


def calcular_casas_da_frota() -> int:
    """Total de casas ocupadas pela frota completa (14)."""
    return sum(tamanho for _tipo, tamanho in COMPOSICAO_FROTA)


def gerar_frota() -> tuple[Tabuleiro, list[Navio]]:
    """RF04: cria tabuleiro novo e posiciona a frota sem sobreposição."""
    for _ in range(MAX_TENTATIVAS_FROTA):
        tabuleiro = criar_tabuleiro()
        navios: list[Navio] = []
        posicionou_todos = True
        for tipo, tamanho in COMPOSICAO_FROTA:
            navio = _encaixar_navio(tabuleiro, tipo, tamanho)
            if navio is None:
                posicionou_todos = False
                break
            desenhar_navio(tabuleiro, navio)
            navios.append(navio)
        if posicionou_todos:
            return tabuleiro, navios
    raise RuntimeError("Nao foi possivel posicionar a frota sem sobreposicao.")


def reposicionar_frota() -> tuple[Tabuleiro, list[Navio]]:
    """Gera outra disposição aleatória (opção R da conferência)."""
    return gerar_frota()


def conferir_posicionamento(nome_jogador: str) -> tuple[Tabuleiro, list[Navio]]:
    """RF10: mostra a frota e pede confirmar (C) ou reposicionar (R)."""
    while True:
        tabuleiro, navios = gerar_frota()
        _exibir_conferencia(nome_jogador, tabuleiro, navios)
        if _jogador_confirmou():
            return tabuleiro, navios


def desenhar_navio(tabuleiro: Tabuleiro, navio: Navio) -> None:
    """Marca as casas do navio com N no tabuleiro."""
    for linha, coluna in navio.posicoes:
        marcar_celula(tabuleiro, linha, coluna, SIMBOLO_NAVIO)


def encontrar_navio(navios: list[Navio], posicao: Posicao) -> Navio | None:
    """Devolve o navio que ocupa a casa, ou None (água)."""
    for navio in navios:
        if posicao in navio.posicoes:
            return navio
    return None


def frota_afundada(navios: list[Navio]) -> bool:
    """True quando todos os navios da lista estão afundados."""
    return all(navio.esta_afundado() for navio in navios)


def resumo_frota(navios: list[Navio]) -> str:
    """Texto com tipo e coordenadas de cada navio."""
    linhas = [
        f"Frota ({len(navios)} navios, {calcular_casas_da_frota()} casas):"
    ]
    for indice, navio in enumerate(navios, start=1):
        casas = " ".join(
            formatar_coordenada(linha, coluna)
            for linha, coluna in navio.posicoes
        )
        linhas.append(f"  {indice}. {navio.tipo:<8} {casas}")
    return "\n".join(linhas)


def _encaixar_navio(
    tabuleiro: Tabuleiro,
    tipo: str,
    tamanho: int,
) -> Navio | None:
    """Tenta achar um segmento livre; None se esgotar as tentativas."""
    for _ in range(MAX_TENTATIVAS_POR_NAVIO):
        horizontal = random.choice((True, False))
        posicoes = _sortear_segmento(tamanho, horizontal)
        if _casas_estao_livres(tabuleiro, posicoes):
            return Navio(tipo=tipo, tamanho=tamanho, posicoes=posicoes)
    return None


def _sortear_segmento(tamanho: int, horizontal: bool) -> list[Posicao]:
    """Sorteia um segmento que já cabe inteiro no tabuleiro."""
    limite = TAMANHO_TABULEIRO - tamanho
    if horizontal:
        linha = random.randint(0, TAMANHO_TABULEIRO - 1)
        coluna = random.randint(0, limite)
        return [(linha, coluna + deslocamento) for deslocamento in range(tamanho)]
    linha = random.randint(0, limite)
    coluna = random.randint(0, TAMANHO_TABULEIRO - 1)
    return [(linha + deslocamento, coluna) for deslocamento in range(tamanho)]


def _casas_estao_livres(tabuleiro: Tabuleiro, posicoes: list[Posicao]) -> bool:
    """RF04: recusa o encaixe se alguma casa já tiver navio."""
    return all(
        obter_celula(tabuleiro, linha, coluna) == SIMBOLO_AGUA
        for linha, coluna in posicoes
    )


def _exibir_conferencia(
    nome_jogador: str,
    tabuleiro: Tabuleiro,
    navios: list[Navio],
) -> None:
    limpar_tela()
    print("=" * 50)
    print(f"CONFERENCIA DOS NAVIOS - {nome_jogador}")
    print("=" * 50)
    print()
    imprimir_tabuleiro(tabuleiro)
    print()
    print(resumo_frota(navios))
    print()
    print("[C] Confirmar posicionamento")
    print("[R] Reposicionar (gerar frota nova)")
    print("-" * 50)


def _jogador_confirmou() -> bool:
    """Lê C ou R; entrada inválida não troca a frota nem confirma."""
    while True:
        escolha = input(">> ").strip().upper()
        if escolha in {"C", "CONFIRMAR"}:
            return True
        if escolha in {"R", "REPOSICIONAR"}:
            return False
        print("Opcao invalida. Digite C para confirmar ou R para reposicionar.")


def _frota_sem_sobreposicao(navios: list[Navio]) -> bool:
    ocupadas: set[Posicao] = set()
    for navio in navios:
        for casa in navio.posicoes:
            if casa in ocupadas:
                return False
            ocupadas.add(casa)
    return len(ocupadas) == calcular_casas_da_frota()


if __name__ == "__main__":
    for _ in range(40):
        tabuleiro_teste, navios_teste = gerar_frota()
        if not _frota_sem_sobreposicao(navios_teste):
            raise SystemExit("Falha: houve sobreposicao na frota gerada.")
        casas_n = sum(
            1
            for linha in tabuleiro_teste
            for simbolo in linha
            if simbolo == SIMBOLO_NAVIO
        )
        if casas_n != calcular_casas_da_frota():
            raise SystemExit("Falha: quantidade de N diferente da frota.")

    print("Validacao automatica (40 frotas sem overlap): ok")
    print()
    print("Iniciando conferencia. C confirma, R gera outra frota.")
    input("ENTER para continuar... ")
    conferir_posicionamento("Jogador 1")
    print()
    print("Frota confirmada. Proximo passo do plano: T4 (menu).")
