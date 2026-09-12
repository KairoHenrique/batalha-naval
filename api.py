"""API HTTP da mesma lógica do Batalha Naval (T9).

Roda em http://127.0.0.1:8000. O menu texto (python main.py) nao muda.
Nao commitar ate o professor aceitar a GUI web.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from estatisticas import listar_estatisticas
from jogador import criar_jogador
from navios import (
    frota_esta_completa,
    frota_vazia,
    gerar_frota,
    listar_restantes,
    resumo_frota,
    retirar_navio_na_casa,
    tentar_posicionar,
)
from partida import (
    Partida,
    aplicar_tiro,
    criar_partida,
    executar_turno_computador,
    persistir_partida_encerrada,
)
from replay import carregar_ultima_partida, formatar_linha_jogada
from tabuleiro import ocultar_navios
from utils import COLUNAS, formatar_tempo, parse_coordenada

app = FastAPI(title="Batalha Naval API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@dataclass
class SessaoWeb:
    modo: str
    dificuldade: str
    nome_j1: str
    nome_j2: str
    fase: str
    frota_j1: tuple | None = None
    frota_j2: tuple | None = None
    partida: Partida | None = None
    mensagem: str = ""
    jogadas_turno: list[dict] = field(default_factory=list)
    aguardando_troca: bool = False


_sessao: SessaoWeb | None = None


class NovaPartidaIn(BaseModel):
    modo: Literal["pvc", "pvp"]
    dificuldade: Literal["facil", "medio", "dificil"] = "medio"
    nome_j1: str = Field(default="Jogador 1", max_length=40)
    nome_j2: str = Field(default="Jogador 2", max_length=40)


class JogadaIn(BaseModel):
    coordenada: str = Field(min_length=2, max_length=3)


class PosicionarIn(BaseModel):
    coordenada: str = Field(min_length=2, max_length=3)
    horizontal: bool = True
    tipo: Literal["grande", "pequeno"]


class CoordenadaIn(BaseModel):
    coordenada: str = Field(min_length=2, max_length=3)


def _sessao_atual() -> SessaoWeb:
    if _sessao is None:
        raise HTTPException(status_code=404, detail="Nenhuma partida em andamento.")
    return _sessao


def _apelido(texto: str, padrao: str) -> str:
    limpo = texto.strip()[:40]
    return limpo or padrao


def _resultado_para_dict(resultado: Any) -> dict:
    return {
        "valida": resultado.valida,
        "coordenada": resultado.coordenada,
        "mensagem": resultado.mensagem,
        "jogador": resultado.jogador,
        "resultado": resultado.resultado,
        "tipo_navio": resultado.tipo_navio,
        "jogo_acabou": resultado.jogo_acabou,
        "vencedor": resultado.vencedor,
    }


def _serializar_tabuleiro(tabuleiro: list[list[str]], ocultar: bool) -> list[list[str]]:
    visivel = ocultar_navios(tabuleiro) if ocultar else tabuleiro
    return [list(linha) for linha in visivel]


def _estado_publico() -> dict:
    sessao = _sessao_atual()
    colunas = list(COLUNAS)
    base = {
        "fase": sessao.fase,
        "modo": sessao.modo,
        "dificuldade": sessao.dificuldade,
        "nome_j1": sessao.nome_j1,
        "nome_j2": sessao.nome_j2,
        "mensagem": sessao.mensagem,
        "jogadas_turno": sessao.jogadas_turno,
        "aguardando_troca": sessao.aguardando_troca,
        "colunas": colunas,
        "tabuleiro_proprio": None,
        "tabuleiro_tiros": None,
        "resumo_frota": None,
        "vez": None,
        "vencedor": None,
        "total_jogadas": 0,
        "tempo": "00:00:00",
        "pode_atirar": False,
        "restantes": [],
        "frota_completa": False,
        "pode_confirmar": False,
    }
    if sessao.fase == "conferencia_j1" and sessao.frota_j1:
        tab, navios = sessao.frota_j1
        return _estado_conferencia(base, tab, navios, sessao.nome_j1)
    if sessao.fase == "conferencia_j2" and sessao.frota_j2:
        tab, navios = sessao.frota_j2
        return _estado_conferencia(base, tab, navios, sessao.nome_j2)
    partida = sessao.partida
    if partida is None:
        return base
    visao = partida.atacante()
    if visao.eh_computador:
        visao = partida.jogadores[0]
    if sessao.aguardando_troca:
        base["tabuleiro_proprio"] = None
        base["tabuleiro_tiros"] = None
        base["vez"] = visao.nome
        base["vencedor"] = partida.vencedor
        base["total_jogadas"] = partida.total_jogadas
        base["tempo"] = formatar_tempo(partida.duracao_segundos)
        base["pode_atirar"] = False
        return base
    base["tabuleiro_proprio"] = _serializar_tabuleiro(visao.tabuleiro, False)
    base["tabuleiro_tiros"] = _serializar_tabuleiro(visao.tabuleiro_tiros, False)
    base["vez"] = visao.nome
    base["vencedor"] = partida.vencedor
    base["total_jogadas"] = partida.total_jogadas
    base["tempo"] = formatar_tempo(partida.duracao_segundos)
    base["pode_atirar"] = (
        sessao.fase == "em_jogo"
        and not partida.encerrada()
        and not visao.eh_computador
        and not sessao.aguardando_troca
    )
    if sessao.fase == "fim":
        base["tempo"] = formatar_tempo(partida.duracao_segundos)
        base["mensagem"] = sessao.mensagem or f"Vencedor: {partida.vencedor}"
    return base


@app.get("/")
def saude() -> dict:
    return {"ok": True, "servico": "batalha-naval"}


@app.post("/partidas")
def nova_partida(dados: NovaPartidaIn) -> dict:
    global _sessao
    nome_j1 = _apelido(dados.nome_j1, "Jogador 1")
    nome_j2 = "Computador" if dados.modo == "pvc" else _apelido(dados.nome_j2, "Jogador 2")
    frota_j1 = frota_vazia()
    frota_j2 = gerar_frota() if dados.modo == "pvc" else frota_vazia()
    _sessao = SessaoWeb(
        modo=dados.modo,
        dificuldade=dados.dificuldade,
        nome_j1=nome_j1,
        nome_j2=nome_j2,
        fase="conferencia_j1",
        frota_j1=frota_j1,
        frota_j2=frota_j2,
        mensagem=f"Arraste os navios para o tabuleiro de {nome_j1}.",
    )
    return _estado_publico()


@app.get("/partidas")
def obter_partida() -> dict:
    return _estado_publico()


@app.post("/partidas/reposicionar")
def reposicionar() -> dict:
    sessao = _sessao_atual()
    if sessao.fase == "conferencia_j1":
        sessao.frota_j1 = gerar_frota()
        sessao.mensagem = f"Frota sorteada para {sessao.nome_j1}. Confirme ou arraste de novo."
        return _estado_publico()
    if sessao.fase == "conferencia_j2":
        sessao.frota_j2 = gerar_frota()
        sessao.mensagem = f"Frota sorteada para {sessao.nome_j2}. Confirme ou arraste de novo."
        return _estado_publico()
    raise HTTPException(status_code=409, detail="Nao ha frota para reposicionar agora.")


@app.post("/partidas/limpar")
def limpar_frota() -> dict:
    sessao = _sessao_atual()
    tab, navios = frota_vazia()
    _salvar_frota(sessao, tab, navios)
    sessao.mensagem = "Tabuleiro limpo. Arraste os navios de novo."
    return _estado_publico()


@app.post("/partidas/posicionar")
def posicionar(dados: PosicionarIn) -> dict:
    sessao = _sessao_atual()
    _tabuleiro, navios = _obter_frota(sessao)
    try:
        origem = parse_coordenada(dados.coordenada)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro
    tabuleiro, navios, recusa = tentar_posicionar(
        navios,
        dados.tipo,
        origem,
        dados.horizontal,
    )
    if recusa:
        raise HTTPException(status_code=409, detail=recusa)
    _salvar_frota(sessao, tabuleiro, navios)
    if frota_esta_completa(navios):
        sessao.mensagem = "Frota completa. Confirme para comecar."
    else:
        sessao.mensagem = "Navio posicionado. Arraste os que faltam."
    return _estado_publico()


@app.post("/partidas/retirar")
def retirar(dados: CoordenadaIn) -> dict:
    sessao = _sessao_atual()
    _tabuleiro, navios = _obter_frota(sessao)
    try:
        posicao = parse_coordenada(dados.coordenada)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro
    tabuleiro, navios, recusa = retirar_navio_na_casa(navios, posicao)
    if recusa:
        raise HTTPException(status_code=409, detail=recusa)
    _salvar_frota(sessao, tabuleiro, navios)
    sessao.mensagem = "Navio devolvido. Arraste para reposicionar."
    return _estado_publico()


@app.post("/partidas/confirmar")
def confirmar() -> dict:
    sessao = _sessao_atual()
    if sessao.fase == "conferencia_j1":
        _exigir_frota_completa(sessao.frota_j1)
        if sessao.modo == "pvc":
            _iniciar_jogo(sessao)
            return _estado_publico()
        sessao.fase = "conferencia_j2"
        sessao.frota_j2 = frota_vazia()
        sessao.mensagem = (
            f"Passe o computador para {sessao.nome_j2} e posicione a frota."
        )
        return _estado_publico()
    if sessao.fase == "conferencia_j2":
        _exigir_frota_completa(sessao.frota_j2)
        _iniciar_jogo(sessao)
        return _estado_publico()
    raise HTTPException(status_code=409, detail="Nada para confirmar nesta fase.")


@app.post("/partidas/pronto")
def pronto_para_jogar() -> dict:
    sessao = _sessao_atual()
    sessao.aguardando_troca = False
    sessao.mensagem = f"Vez de {sessao.partida.atacante().nome}." if sessao.partida else ""
    return _estado_publico()


@app.post("/partidas/jogadas")
def jogar(dados: JogadaIn) -> dict:
    sessao = _sessao_atual()
    if sessao.partida is None or sessao.fase != "em_jogo":
        raise HTTPException(status_code=409, detail="A partida ainda nao comecou.")
    if sessao.aguardando_troca:
        raise HTTPException(status_code=409, detail="Passe o computador e confirme a vez.")
    partida = sessao.partida
    if partida.atacante().eh_computador:
        raise HTTPException(status_code=409, detail="Aguarde o computador.")
    resultado = aplicar_tiro(partida, dados.coordenada)
    sessao.jogadas_turno = [_resultado_para_dict(resultado)]
    sessao.mensagem = resultado.mensagem
    if not resultado.valida:
        return _estado_publico()
    if partida.encerrada():
        _encerrar(sessao)
        return _estado_publico()
    if partida.atacante().eh_computador:
        cpu = executar_turno_computador(partida)
        sessao.jogadas_turno.append(_resultado_para_dict(cpu))
        sessao.mensagem = (
            f"{resultado.mensagem} Computador: {cpu.coordenada} — {cpu.mensagem}"
        )
        if partida.encerrada():
            _encerrar(sessao)
            return _estado_publico()
        return _estado_publico()
    if sessao.modo == "pvp":
        sessao.aguardando_troca = True
        sessao.mensagem = (
            f"{resultado.mensagem} Passe o computador para {partida.atacante().nome}."
        )
    return _estado_publico()


@app.get("/estatisticas")
def estatisticas() -> dict:
    return {"jogadores": listar_estatisticas()}


@app.get("/replay")
def replay() -> dict:
    registro = carregar_ultima_partida()
    if registro is None:
        return {"existe": False, "jogadas": [], "linhas": []}
    total = int(registro.get("total_jogadas", len(registro.get("jogadas", []))))
    linhas = [
        formatar_linha_jogada(jogada, total)
        for jogada in registro.get("jogadas", [])
    ]
    return {"existe": True, **registro, "linhas": linhas}


def _estado_conferencia(base: dict, tabuleiro: list, navios: list, nome: str) -> dict:
    completa = frota_esta_completa(navios)
    base["tabuleiro_proprio"] = _serializar_tabuleiro(tabuleiro, False)
    base["resumo_frota"] = resumo_frota(navios) if navios else None
    base["vez"] = nome
    base["restantes"] = listar_restantes(navios)
    base["frota_completa"] = completa
    base["pode_confirmar"] = completa
    return base


def _obter_frota(sessao: SessaoWeb) -> tuple:
    if sessao.fase == "conferencia_j1" and sessao.frota_j1 is not None:
        return sessao.frota_j1
    if sessao.fase == "conferencia_j2" and sessao.frota_j2 is not None:
        return sessao.frota_j2
    raise HTTPException(status_code=409, detail="Nao e hora de posicionar navios.")


def _salvar_frota(sessao: SessaoWeb, tabuleiro: list, navios: list) -> None:
    if sessao.fase == "conferencia_j1":
        sessao.frota_j1 = (tabuleiro, navios)
        return
    if sessao.fase == "conferencia_j2":
        sessao.frota_j2 = (tabuleiro, navios)
        return
    raise HTTPException(status_code=409, detail="Nao e hora de posicionar navios.")


def _exigir_frota_completa(frota: tuple | None) -> None:
    if frota is None:
        raise HTTPException(status_code=409, detail="Frotas incompletas.")
    _tabuleiro, navios = frota
    if not frota_esta_completa(navios):
        raise HTTPException(
            status_code=409,
            detail="Posicione todos os navios antes de confirmar.",
        )


def _iniciar_jogo(sessao: SessaoWeb) -> None:
    if sessao.frota_j1 is None or sessao.frota_j2 is None:
        raise HTTPException(status_code=409, detail="Frotas incompletas.")
    tab_j1, navios_j1 = sessao.frota_j1
    tab_j2, navios_j2 = sessao.frota_j2
    jogador_1 = criar_jogador(sessao.nome_j1, tab_j1, navios_j1)
    eh_cpu = sessao.modo == "pvc"
    jogador_2 = criar_jogador(sessao.nome_j2, tab_j2, navios_j2, eh_computador=eh_cpu)
    sessao.partida = criar_partida(
        sessao.modo,
        sessao.dificuldade,
        jogador_1,
        jogador_2,
    )
    sessao.fase = "em_jogo"
    sessao.aguardando_troca = False
    sessao.mensagem = f"Partida iniciada. Vez de {sessao.nome_j1}."


def _encerrar(sessao: SessaoWeb) -> None:
    if sessao.partida is None:
        return
    persistir_partida_encerrada(sessao.partida)
    sessao.fase = "fim"
    sessao.aguardando_troca = False
    sessao.mensagem = (
        f"FIM DE JOGO. Vencedor: {sessao.partida.vencedor}. "
        f"Jogadas: {sessao.partida.total_jogadas}."
    )
