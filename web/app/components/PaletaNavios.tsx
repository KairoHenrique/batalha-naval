"use client";

import type { PointerEvent } from "react";
import type { NavioPendente } from "@/lib/api";

type Props = {
  restantes: NavioPendente[];
  orientacoes: Record<string, boolean>;
  onGirarPeca: (id: string) => void;
  onInicioArraste: (
    navio: NavioPendente,
    horizontal: boolean,
    evento: PointerEvent,
  ) => void;
};

export default function PaletaNavios({
  restantes,
  orientacoes,
  onGirarPeca,
  onInicioArraste,
}: Props) {
  const grandes = restantes.filter((navio) => navio.tipo === "grande");
  const pequenos = restantes.filter((navio) => navio.tipo === "pequeno");

  return (
    <div className="paletas" aria-label="Caixas de navios">
      <CaixaNavios
        titulo="Navios grandes"
        nota="4 casas · 2 na frota"
        navios={grandes}
        orientacoes={orientacoes}
        onGirarPeca={onGirarPeca}
        onInicioArraste={onInicioArraste}
      />
      <CaixaNavios
        titulo="Navios pequenos"
        nota="2 casas · 3 na frota"
        navios={pequenos}
        orientacoes={orientacoes}
        onGirarPeca={onGirarPeca}
        onInicioArraste={onInicioArraste}
      />
    </div>
  );
}

function CaixaNavios({
  titulo,
  nota,
  navios,
  orientacoes,
  onGirarPeca,
  onInicioArraste,
}: {
  titulo: string;
  nota: string;
  navios: NavioPendente[];
  orientacoes: Record<string, boolean>;
  onGirarPeca: (id: string) => void;
  onInicioArraste: (
    navio: NavioPendente,
    horizontal: boolean,
    evento: PointerEvent,
  ) => void;
}) {
  return (
    <aside className="paleta">
      <h2>{titulo}</h2>
      <p className="paleta-ajuda">{nota}. Gire a peça e arraste para o tabuleiro.</p>
      <div className="paleta-lista">
        {navios.length === 0 ? (
          <p className="vazio">Todos posicionados.</p>
        ) : (
          navios.map((navio) => {
            const horizontal = orientacoes[navio.id] ?? true;
            return (
              <div key={navio.id} className="peca-linha">
                <button
                  type="button"
                  className={`peca peca-${navio.tipo} ${horizontal ? "peca-h" : "peca-v"}`}
                  aria-label={`${navio.tipo}, ${horizontal ? "deitado" : "em pe"}`}
                  onPointerDown={(evento) => {
                    evento.preventDefault();
                    onInicioArraste(navio, horizontal, evento);
                  }}
                >
                  {Array.from({ length: navio.tamanho }, (_, indice) => (
                    <i key={indice} className="peca-casa" />
                  ))}
                </button>
                <button
                  type="button"
                  className="botao-girar"
                  onPointerDown={(evento) => evento.stopPropagation()}
                  onClick={() => onGirarPeca(navio.id)}
                >
                  Girar
                </button>
              </div>
            );
          })
        )}
      </div>
    </aside>
  );
}
