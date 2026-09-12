"use client";

import NavVoltar from "@/app/components/NavVoltar";
import { useReplay } from "@/app/hooks/useReplay";

export default function PaginaReplay() {
  const { linhas, existe, erro, carregando } = useReplay();

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
          <ol className="replay">
            {linhas.map((linha) => (
              <li key={linha}>{linha}</li>
            ))}
          </ol>
        ) : null}
      </section>
    </>
  );
}
