"use client";

import { useEffect, useMemo, useState } from "react";
import Botao from "@/app/components/Botao";
import LegendaTabuleiro from "@/app/components/LegendaTabuleiro";
import PaletaNavios from "@/app/components/PaletaNavios";
import Tabuleiro from "@/app/components/Tabuleiro";
import type { EstadoPartida, NavioPendente } from "@/lib/api";
import { coordenadaSobPonteiro, mapaDePreview } from "@/lib/posicionamento";

type Arraste = NavioPendente & { horizontal: boolean };

type Props = {
  estado: EstadoPartida;
  ocupado: boolean;
  onConfirmar: () => void;
  onReposicionar: () => void;
  onLimpar: () => void;
  onPosicionar: (navio: NavioPendente, coordenada: string, horizontal: boolean) => void;
  onRetirar: (coordenada: string) => void;
};

export default function PainelPosicionamento({
  estado,
  ocupado,
  onConfirmar,
  onReposicionar,
  onLimpar,
  onPosicionar,
  onRetirar,
}: Props) {
  const [orientacoes, setOrientacoes] = useState<Record<string, boolean>>({});
  const [arraste, setArraste] = useState<Arraste | null>(null);
  const [hover, setHover] = useState<string | null>(null);
  const [cursor, setCursor] = useState({ x: 0, y: 0 });
  const grade = estado.tabuleiro_proprio ?? [];
  const restantes = estado.restantes ?? [];

  const destaques = useMemo(() => {
    if (!arraste || !hover) {
      return {};
    }
    return mapaDePreview(hover, arraste.tamanho, arraste.horizontal, grade);
  }, [arraste, hover, grade]);

  useEffect(() => {
    document.body.classList.toggle("arrastando", arraste !== null);
    return () => document.body.classList.remove("arrastando");
  }, [arraste]);

  useEffect(() => {
    if (!arraste) {
      return undefined;
    }
    function mover(evento: PointerEvent) {
      setCursor({ x: evento.clientX, y: evento.clientY });
      setHover(coordenadaSobPonteiro(evento.clientX, evento.clientY));
    }
    function soltar(evento: PointerEvent) {
      const coordenada = coordenadaSobPonteiro(evento.clientX, evento.clientY);
      if (coordenada && arraste) {
        onPosicionar(arraste, coordenada, arraste.horizontal);
      }
      setArraste(null);
      setHover(null);
    }
    function girarComRoda(evento: WheelEvent) {
      evento.preventDefault();
      setArraste((atual) =>
        atual ? { ...atual, horizontal: !atual.horizontal } : atual,
      );
    }
    function girarComBotaoDireito(evento: MouseEvent) {
      evento.preventDefault();
      setArraste((atual) =>
        atual ? { ...atual, horizontal: !atual.horizontal } : atual,
      );
    }
    window.addEventListener("pointermove", mover);
    window.addEventListener("pointerup", soltar);
    window.addEventListener("wheel", girarComRoda, { passive: false });
    window.addEventListener("contextmenu", girarComBotaoDireito);
    return () => {
      window.removeEventListener("pointermove", mover);
      window.removeEventListener("pointerup", soltar);
      window.removeEventListener("wheel", girarComRoda);
      window.removeEventListener("contextmenu", girarComBotaoDireito);
    };
  }, [arraste, onPosicionar]);

  function girarPeca(id: string) {
    setOrientacoes((atual) => ({
      ...atual,
      [id]: !(atual[id] ?? true),
    }));
  }

  return (
    <section className="posicionamento">
      <PaletaNavios
        restantes={restantes}
        orientacoes={orientacoes}
        onGirarPeca={girarPeca}
        onInicioArraste={(navio, horizontal, evento) => {
          setArraste({ ...navio, horizontal });
          setCursor({ x: evento.clientX, y: evento.clientY });
          setHover(coordenadaSobPonteiro(evento.clientX, evento.clientY));
        }}
      />
      <div className="painel">
        <h2>Tabuleiro — {estado.vez}</h2>
        <Tabuleiro
          grade={grade}
          clicavel={!ocupado}
          destaques={destaques}
          onClique={(coordenada) => {
            if (arraste) {
              return;
            }
            const ponto = parseIndice(coordenada);
            if (ponto && grade[ponto.linha][ponto.coluna] === "N") {
              onRetirar(coordenada);
            }
          }}
        />
        <LegendaTabuleiro />
        <div className="acoes">
          <Botao
            variante="ouro"
            disabled={ocupado || !estado.pode_confirmar}
            onClick={onConfirmar}
          >
            Confirmar
          </Botao>
          <Botao disabled={ocupado} onClick={onReposicionar}>
            Reposicionar
          </Botao>
          <Botao disabled={ocupado} onClick={onLimpar}>
            Limpar
          </Botao>
        </div>
      </div>
      {arraste ? (
        <div
          className={`fantasma-arraste peca peca-${arraste.tipo} ${arraste.horizontal ? "peca-h" : "peca-v"}`}
          style={{ left: cursor.x, top: cursor.y }}
          aria-hidden="true"
        >
          {Array.from({ length: arraste.tamanho }, (_, indice) => (
            <i key={indice} className="peca-casa" />
          ))}
        </div>
      ) : null}
    </section>
  );
}

function parseIndice(coordenada: string): { linha: number; coluna: number } | null {
  const letra = coordenada[0];
  const numero = Number(coordenada.slice(1));
  const coluna = "ABCDEFGHIJ".indexOf(letra);
  if (coluna < 0 || numero < 1 || numero > 10) {
    return null;
  }
  return { linha: numero - 1, coluna };
}
