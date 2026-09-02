"""Menu principal do Batalha Naval (RF01, RF08).

Nova partida no modo PvC ou PvP (T5/T6).
"""

from __future__ import annotations

from estatisticas import exibir_estatisticas
from partida import (
    exibir_fim_de_jogo,
    jogar,
    montar_partida_pvc,
    montar_partida_pvp,
)
from replay import reproduzir_ultima_partida
from utils import limpar_tela

NIVEIS_IA = ("facil", "medio", "dificil")
LARGURA = 50


def iniciar_menu() -> None:
    """RF01: laço do menu até o usuário sair. RF08: nova partida sempre disponível."""
    while True:
        _exibir_menu_principal()
        opcao = _ler_opcao({"1", "2", "3", "4", "5"})
        if opcao == "1":
            iniciar_nova_partida()
        elif opcao == "2":
            exibir_estatisticas()
        elif opcao == "3":
            reproduzir_ultima_partida()
        elif opcao == "4":
            exibir_creditos()
        elif opcao == "5":
            print("Ate logo.")
            return


def iniciar_nova_partida() -> None:
    """RF08: começa uma partida a partir do menu (modo + conferência RF10)."""
    modo = _selecionar_modo()
    if modo is None:
        return

    dificuldade = "medio"
    if modo == "pvc":
        escolhida = _selecionar_dificuldade()
        if escolhida is None:
            return
        dificuldade = escolhida

    nome_j1, nome_j2 = _perguntar_nomes(modo)
    if modo == "pvc":
        partida = montar_partida_pvc(nome_j1, dificuldade)
    else:
        partida = montar_partida_pvp(nome_j1, nome_j2)
    jogar(partida)
    if exibir_fim_de_jogo(partida) == "nova":
        iniciar_nova_partida()


def exibir_creditos() -> None:
    """Tela de créditos do mockup (opção 4)."""
    limpar_tela()
    _imprimir_faixa("CREDITOS")
    print("GPTech Games — linha de tabuleiros classicos em modo texto")
    print("Projeto: Batalha Naval")
    print()
    print("Desenvolvedor: Kairo Henrique Ferreira Martins")
    print("Disciplina: Programacao em Python — CEFET-MG Divinopolis")
    print("Product Owner / professor: Guido Pantuza")
    print("Repositorio: https://github.com/KairoHenrique/batalha-naval")
    print()
    print("Trabalho individual. Entrega: 29/09/2026 (SIGAA).")
    _pausar()


def _exibir_menu_principal() -> None:
    limpar_tela()
    print("=" * LARGURA)
    print("BATALHA NAVAL - GPTECH GAMES")
    print("=" * LARGURA)
    print("1. Nova partida")
    print("2. Ver estatisticas")
    print("3. Assistir replay da ultima partida")
    print("4. Creditos")
    print("5. Sair")
    print("-" * LARGURA)


def _selecionar_modo() -> str | None:
    """Mockup 6.2. None = voltar ao menu."""
    limpar_tela()
    print("Selecione o modo de jogo:")
    print("[1] Jogador vs Computador")
    print("[2] Dois Jogadores")
    print("[0] Voltar ao menu")
    print()
    opcao = _ler_opcao({"0", "1", "2"}, prompt=">> ")
    if opcao == "0":
        return None
    return "pvc" if opcao == "1" else "pvp"


def _selecionar_dificuldade() -> str | None:
    """Níveis da IA (T7); a escolha já fica gravada na sessão."""
    limpar_tela()
    print("Selecione a dificuldade da IA:")
    print("[1] Facil")
    print("[2] Medio")
    print("[3] Dificil")
    print("[0] Voltar ao menu")
    print()
    opcao = _ler_opcao({"0", "1", "2", "3"}, prompt=">> ")
    if opcao == "0":
        return None
    return NIVEIS_IA[int(opcao) - 1]


def _perguntar_nomes(modo: str) -> tuple[str, str]:
    print()
    nome_j1 = _ler_nome("Nome do Jogador 1", "Jogador 1")
    if modo == "pvc":
        return nome_j1, "Computador"
    nome_j2 = _ler_nome("Nome do Jogador 2", "Jogador 2")
    return nome_j1, nome_j2


def _imprimir_faixa(titulo: str) -> None:
    print("=" * LARGURA)
    print(titulo)
    print("=" * LARGURA)
    print()


def _ler_opcao(permitidas: set[str], prompt: str = "Escolha uma opcao: ") -> str:
    """RNF05: rejeita vazio e valores fora da lista, sem quebrar o menu."""
    while True:
        bruto = input(prompt).strip()
        if bruto in permitidas:
            return bruto
        print("Opcao invalida. Tente novamente.")


def _ler_nome(rotulo: str, padrao: str) -> str:
    bruto = input(f"{rotulo} [{padrao}]: ").strip()
    if not bruto:
        return padrao
    return bruto[:40]


def _pausar() -> None:
    input("\n[ENTER] Voltar ao menu")
