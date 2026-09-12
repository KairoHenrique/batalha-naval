"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Botao from "@/app/components/Botao";
import NavVoltar from "@/app/components/NavVoltar";
import { useReplay } from "@/app/hooks/useReplay";

export default function PaginaReplay() {
  const { linhas, existe, erro, carregando } = useReplay();
  const [passo, setPasso] = useState(0);
  const [automatico, setAutomatico] = useState(false);

  useEffect(() => {
    if (!automatico) {
      return undefined;
    }
    if (passo >= linhas.length) {
      setAutomatico(false);
      return undefined;
    }
    const timer = window.setTimeout(() => setPasso((atual) => atual + 1), 900);
    return () => window.clearTimeout(timer);
  }, [automatico, passo, linhas.length]);

  const visiveis = linhas.slice(0, passo);

  return (
    <>
      <NavVoltar />
      <h1>Replay</h1>
      <section className="console">
        {carregando ? <p className="vazio">Carregando...</p> : null}
        {erro ? (
          <p className="erro" role="alert">
            {erro}
          </p>
        ) : null}
        {!carregando && !erro && !existe ? (
          <p className="vazio">Nenhuma partida gravada ainda.</p>
        ) : null}
        {linhas.length > 0 ? (
          <>
            <p className="vazio">
              Jogada {Math.min(passo, linhas.length)}/{linhas.length}
            </p>
            <ol className="replay">
              {visiveis.map((linha) => (
                <li key={linha}>{linha}</li>
              ))}
            </ol>
            <div className="acoes">
              <Botao
                variante="ouro"
                disabled={passo >= linhas.length}
                onClick={() => {
                  setAutomatico(false);
                  setPasso((atual) => Math.min(linhas.length, atual + 1));
                }}
              >
                Próxima
              </Botao>
              <Botao
                disabled={passo >= linhas.length}
                onClick={() => setAutomatico((atual) => !atual)}
              >
                {automatico ? "Pausar" : "Play"}
              </Botao>
              <Link className="botao" href="/">
                Sair
              </Link>
            </div>
          </>
        ) : null}
      </section>
    </>
  );
}
