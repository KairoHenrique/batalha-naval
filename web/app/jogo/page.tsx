"use client";

import Tabuleiro from "@/app/components/Tabuleiro";
import Botao from "@/app/components/Botao";
import LegendaTabuleiro from "@/app/components/LegendaTabuleiro";
import NavVoltar from "@/app/components/NavVoltar";
import PainelPosicionamento from "@/app/components/PainelPosicionamento";
import { usePartida } from "@/app/hooks/usePartida";
import {
  atirar,
  confirmarFrota,
  confirmarVez,
  limparFrota,
  posicionarNavio,
  reposicionarFrota,
  retirarNavio,
  type EstadoPartida,
} from "@/lib/api";

export default function PaginaJogo() {
  const { estado, erro, ocupado, executar } = usePartida();

  if (!estado && !erro) {
    return <p className="vazio">Carregando tabuleiro...</p>;
  }

  if (!estado) {
    return (
      <>
        <NavVoltar />
        <p className="erro" role="alert">
          {erro}
        </p>
      </>
    );
  }

  const emConferencia =
    estado.fase === "conferencia_j1" || estado.fase === "conferencia_j2";
  const contexto =
    estado.modo === "pvc" ? "Jogador × Computador" : "Dois jogadores";

  return (
    <>
      <NavVoltar contexto={`${contexto}${estado.vez ? ` · ${estado.vez}` : ""}`} />
      <h1>{estado.fase === "fim" ? "Fim de jogo" : "Partida"}</h1>
      <p className="mensagem">{estado.mensagem}</p>
      {erro ? (
        <p className="erro" role="alert">
          {erro}
        </p>
      ) : null}

      {emConferencia && estado.tabuleiro_proprio ? (
        <PainelPosicionamento
          estado={estado}
          ocupado={ocupado}
          onConfirmar={() => void executar(confirmarFrota)}
          onReposicionar={() => void executar(reposicionarFrota)}
          onLimpar={() => void executar(limparFrota)}
          onPosicionar={(navio, coordenada, horizontal) =>
            void executar(() =>
              posicionarNavio({
                coordenada,
                horizontal,
                tipo: navio.tipo,
              }),
            )
          }
          onRetirar={(coordenada) => void executar(() => retirarNavio(coordenada))}
        />
      ) : null}

      {!emConferencia && !estado.aguardando_troca ? (
        <PainelBatalha
          estado={estado}
          podeAtirar={estado.pode_atirar && !ocupado}
          onTiro={(coordenada) => void executar(() => atirar(coordenada))}
        />
      ) : null}

      {estado.aguardando_troca ? (
        <section className="console troca">
          <p>Passe o computador para o próximo jogador.</p>
          <Botao
            variante="ouro"
            disabled={ocupado}
            onClick={() => void executar(confirmarVez)}
          >
            Pronto, é a minha vez
          </Botao>
        </section>
      ) : null}

      {estado.fase === "fim" ? (
        <p className="vazio">
          Vencedor: {estado.vencedor} · Jogadas: {estado.total_jogadas} · Tempo:{" "}
          {estado.tempo}
        </p>
      ) : null}

      {estado.jogadas_turno.length > 0 ? (
        <ul className="replay" style={{ marginTop: 16 }}>
          {estado.jogadas_turno.map((jogada, indice) => (
            <li key={`${jogada.coordenada}-${indice}`}>
              {jogada.jogador} — {jogada.coordenada} — {jogada.mensagem}
            </li>
          ))}
        </ul>
      ) : null}
    </>
  );
}

function PainelBatalha({
  estado,
  podeAtirar,
  onTiro,
}: {
  estado: EstadoPartida;
  podeAtirar: boolean;
  onTiro: (coordenada: string) => void;
}) {
  return (
    <div className="tabuleiros">
      {estado.tabuleiro_tiros ? (
        <section className="painel">
          <h2>Tiros no inimigo</h2>
          <Tabuleiro
            grade={estado.tabuleiro_tiros}
            clicavel={podeAtirar}
            onClique={onTiro}
          />
          <LegendaTabuleiro />
        </section>
      ) : null}
      {estado.tabuleiro_proprio ? (
        <section className="painel">
          <h2>Seu tabuleiro</h2>
          <Tabuleiro grade={estado.tabuleiro_proprio} />
        </section>
      ) : null}
    </div>
  );
}
