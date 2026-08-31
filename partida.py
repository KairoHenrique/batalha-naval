"""Sessão de partida: tiros, mensagens e loop Jogador x Computador (T5)."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass, field

from jogador import Jogador, criar_jogador
from navios import conferir_posicionamento, encontrar_navio, gerar_frota
from tabuleiro import imprimir_tabuleiro, marcar_celula, renderizar_tabuleiro
from utils import (
    SIMBOLO_ACERTO,
    SIMBOLO_AGUA_JOGADA,
    TAMANHO_TABULEIRO,
    Posicao,
    formatar_coordenada,
    formatar_tempo,
    limpar_tela,
    mensagem_jogada_repetida,
    parse_coordenada,
    posicao_ja_jogada,
)

LARGURA = 50


@dataclass
class ResultadoJogada:
    """Retorno de um disparo (RF05 / RF06)."""

    valida: bool
    coordenada: str
    mensagem: str
    jogador: str
    resultado: str = "invalida"
    tipo_navio: str | None = None
    jogo_acabou: bool = False
    vencedor: str | None = None


@dataclass
class Partida:
    modo: str
    dificuldade: str
    jogadores: list[Jogador]
    turno: int = 0
    historico: list[dict] = field(default_factory=list)
    inicio: float = field(default_factory=time.perf_counter)
    vencedor: str | None = None
    total_jogadas: int = 0

    def encerrada(self) -> bool:
        return self.vencedor is not None

    def atacante(self) -> Jogador:
        return self.jogadores[self.turno]

    def defensor(self) -> Jogador:
        return self.jogadores[1 - self.turno]


def montar_partida_pvc(
    nome_humano: str,
    dificuldade: str,
) -> Partida:
    """RF09/RF10: humano confere a frota; o computador posiciona oculto."""
    tab_humano, navios_humano = conferir_posicionamento(nome_humano)
    tab_cpu, navios_cpu = gerar_frota()
    humano = criar_jogador(nome_humano, tab_humano, navios_humano)
    computador = criar_jogador(
        "Computador",
        tab_cpu,
        navios_cpu,
        eh_computador=True,
    )
    print()
    print("Computador posicionou a frota em segredo.")
    input("ENTER para comecar... ")
    return Partida(
        modo="pvc",
        dificuldade=dificuldade,
        jogadores=[humano, computador],
    )


def montar_partida_pvp(nome_j1: str, nome_j2: str) -> Partida:
    """RF09/RF10: cada humano confere a própria frota (hotseat)."""
    tab_j1, navios_j1 = conferir_posicionamento(nome_j1)
    limpar_tela()
    input(f"Passe o computador para {nome_j2}. ENTER...")
    tab_j2, navios_j2 = conferir_posicionamento(nome_j2)
    jogador_1 = criar_jogador(nome_j1, tab_j1, navios_j1)
    jogador_2 = criar_jogador(nome_j2, tab_j2, navios_j2)
    limpar_tela()
    input("Frotas confirmadas. ENTER para o primeiro turno... ")
    return Partida(
        modo="pvp",
        dificuldade="facil",
        jogadores=[jogador_1, jogador_2],
    )


def jogar(partida: Partida) -> None:
    """Loop de tiros PvC ou PvP até alguém afundar a frota inimiga."""
    while not partida.encerrada():
        atacante = partida.atacante()
        if atacante.eh_computador:
            resultado_cpu = _turno_computador_aleatorio(partida)
            print()
            print(f"Computador jogou {resultado_cpu.coordenada}.")
            print(resultado_cpu.mensagem)
            if partida.encerrada():
                return
            input("ENTER para o seu turno... ")
            continue

        if partida.modo == "pvp":
            _aguardar_troca_de_jogador(atacante.nome)
        _exibir_tabuleiros(partida, atacante)
        coordenada = _pedir_coordenada_humana()
        if coordenada is None:
            continue
        resultado = aplicar_tiro(partida, coordenada)
        print()
        print(f">> {resultado.coordenada}")
        print(resultado.mensagem)
        if not resultado.valida:
            input("ENTER para tentar de novo... ")
            continue
        if partida.encerrada():
            return
        if partida.atacante().eh_computador:
            input("ENTER para o turno do computador... ")


def jogar_pvc(partida: Partida) -> None:
    """Compatível com o T5: mesmo loop unificado."""
    jogar(partida)


def exibir_fim_de_jogo(partida: Partida) -> str:
    """RF07 / mockup 6.5. Devolve 'nova' ou 'menu'."""
    duracao = time.perf_counter() - partida.inicio
    while True:
        limpar_tela()
        print("=" * LARGURA)
        print("FIM DE JOGO")
        print("=" * LARGURA)
        print(f"Vencedor: {partida.vencedor}")
        print(f"Total de jogadas: {partida.total_jogadas}")
        print(f"Tempo de partida: {formatar_tempo(duracao)}")
        print("-" * LARGURA)
        print("[1] Ver replay  [2] Nova partida  [3] Menu principal")
        escolha = input("Escolha uma opcao: ").strip()
        if escolha == "1":
            print()
            print("Replay da ultima partida entra no T8.")
            input("ENTER...")
            continue
        if escolha == "2":
            return "nova"
        if escolha == "3":
            return "menu"
        print("Opcao invalida. Tente novamente.")
        input("ENTER...")


def aplicar_tiro(partida: Partida, texto_coordenada: str) -> ResultadoJogada:
    """Aplica um disparo. Jogada inválida ou repetida não consome a rodada."""
    atacante = partida.atacante()
    try:
        posicao = parse_coordenada(texto_coordenada)
    except ValueError as erro:
        return ResultadoJogada(
            valida=False,
            coordenada=texto_coordenada.strip(),
            mensagem=str(erro),
            jogador=atacante.nome,
        )

    coordenada = formatar_coordenada(*posicao)
    if posicao_ja_jogada(atacante.tiros_feitos, posicao):
        return ResultadoJogada(
            valida=False,
            coordenada=coordenada,
            mensagem=mensagem_jogada_repetida(coordenada),
            jogador=atacante.nome,
        )

    return _resolver_disparo(partida, atacante, posicao, coordenada)


def _resolver_disparo(
    partida: Partida,
    atacante: Jogador,
    posicao: Posicao,
    coordenada: str,
) -> ResultadoJogada:
    defensor = partida.defensor()
    atacante.tiros_feitos.add(posicao)
    partida.total_jogadas += 1
    navio = encontrar_navio(defensor.navios, posicao)

    if navio is None:
        _marcar_tiro(atacante, defensor, posicao, SIMBOLO_AGUA_JOGADA)
        resultado = "agua"
        mensagem = "Agua! Nenhum navio atingido nessa posicao."
        tipo = None
    else:
        navio.acertos.add(posicao)
        atacante.acertos += 1
        _marcar_tiro(atacante, defensor, posicao, SIMBOLO_ACERTO)
        tipo = navio.tipo
        if navio.esta_afundado():
            resultado = "afundado"
            mensagem = (
                "Navio afundado! Voce destruiu um navio "
                f"{navio.tipo} do adversario."
            )
        else:
            resultado = "acerto"
            mensagem = "Acerto! Voce atingiu um navio inimigo."

    vencedor = None
    acabou = False
    if defensor.frota_destruida():
        acabou = True
        vencedor = atacante.nome
        partida.vencedor = vencedor

    registro = {
        "numero": partida.total_jogadas,
        "jogador": atacante.nome,
        "coordenada": coordenada,
        "resultado": resultado,
        "mensagem": mensagem,
    }
    partida.historico.append(registro)
    if not acabou:
        partida.turno = 1 - partida.turno

    return ResultadoJogada(
        valida=True,
        coordenada=coordenada,
        mensagem=mensagem,
        jogador=atacante.nome,
        resultado=resultado,
        tipo_navio=tipo,
        jogo_acabou=acabou,
        vencedor=vencedor,
    )


def _marcar_tiro(
    atacante: Jogador,
    defensor: Jogador,
    posicao: Posicao,
    simbolo: str,
) -> None:
    linha, coluna = posicao
    marcar_celula(atacante.tabuleiro_tiros, linha, coluna, simbolo)
    marcar_celula(defensor.tabuleiro, linha, coluna, simbolo)


def _turno_computador_aleatorio(partida: Partida) -> ResultadoJogada:
    """RN05 (T5): o computador escolhe uma casa ainda livre, ao acaso."""
    livres = _casas_livres(partida.atacante().tiros_feitos)
    linha, coluna = random.choice(livres)
    return aplicar_tiro(partida, formatar_coordenada(linha, coluna))


def _casas_livres(tiros: set[Posicao]) -> list[Posicao]:
    return [
        (linha, coluna)
        for linha in range(TAMANHO_TABULEIRO)
        for coluna in range(TAMANHO_TABULEIRO)
        if (linha, coluna) not in tiros
    ]


def _pedir_coordenada_humana() -> str | None:
    bruto = input("Sua jogada (ex.: C5): ").strip()
    if not bruto:
        print("Informe uma coordenada no formato Letra+Numero.")
        return None
    return bruto


def _aguardar_troca_de_jogador(nome: str) -> None:
    limpar_tela()
    print("=" * LARGURA)
    print(f"Vez de {nome}")
    print("=" * LARGURA)
    print()
    print("Passe o computador para este jogador.")
    print("Nao olhe o tabuleiro do oponente.")
    input("ENTER para ver os tabuleiros... ")


def _exibir_tabuleiros(partida: Partida, visao: Jogador) -> None:
    oponente = partida.jogadores[0]
    if oponente is visao:
        oponente = partida.jogadores[1]
    limpar_tela()
    print("=" * LARGURA)
    print(f"{visao.nome} vs {oponente.nome}")
    print("=" * LARGURA)
    print()
    print("Seu tabuleiro")
    imprimir_tabuleiro(visao.tabuleiro)
    print()
    print("Tabuleiro inimigo")
    print(renderizar_tabuleiro(visao.tabuleiro_tiros))
    print()
    print("Legenda: ~ agua nao jogada | N navio | X acerto | O agua jogada")
    print()
