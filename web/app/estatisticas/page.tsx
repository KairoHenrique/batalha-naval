"use client";

import NavVoltar from "@/app/components/NavVoltar";
import { useEstatisticas } from "@/app/hooks/useEstatisticas";

export default function PaginaEstatisticas() {
  const { linhas, erro, carregando } = useEstatisticas();

  return (
    <>
      <NavVoltar />
      <h1>Estatísticas</h1>
      <section className="console">
        {carregando ? <p className="vazio">Carregando...</p> : null}
        {erro ? (
          <p className="erro" role="alert">
            {erro}
          </p>
        ) : null}
        {!carregando && !erro && linhas.length === 0 ? (
          <p className="vazio">Ainda não há partidas registradas.</p>
        ) : null}
        {linhas.length > 0 ? (
          <table className="tabela">
            <thead>
              <tr>
                <th>Jogador</th>
                <th>Part.</th>
                <th>Vit.</th>
                <th>Tiros</th>
                <th>Acertos</th>
                <th>Aprov.</th>
              </tr>
            </thead>
            <tbody>
              {linhas.map((linha) => (
                <tr key={linha.nome}>
                  <td>{linha.nome}</td>
                  <td>{linha.partidas}</td>
                  <td>{linha.vitorias}</td>
                  <td>{linha.tiros}</td>
                  <td>{linha.acertos}</td>
                  <td>{linha.aproveitamento.toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : null}
      </section>
    </>
  );
}
