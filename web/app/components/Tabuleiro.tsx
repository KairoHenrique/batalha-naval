"use client";

import { coordenadaDeClique, type Celula } from "@/lib/api";
import type { Destaque } from "@/lib/posicionamento";

const COLUNAS = "ABCDEFGHIJ".split("");

function classeCelula(
  simbolo: Celula,
  clicavel: boolean,
  destaque?: Destaque,
): string {
  const partes = [clicavel ? "celula clicavel" : "celula"];
  if (simbolo === "N") partes.push("navio");
  if (simbolo === "X") partes.push("acerto");
  if (simbolo === "O") partes.push("agua-tiro");
  if (destaque) partes.push(destaque);
  return partes.join(" ");
}

function estadoAcessivel(simbolo: Celula): string {
  if (simbolo === "N") return "navio";
  if (simbolo === "X") return "acerto";
  if (simbolo === "O") return "tiro na agua";
  return "agua";
}

type Props = {
  grade: Celula[][];
  clicavel?: boolean;
  destaques?: Record<string, Destaque>;
  onClique?: (coordenada: string) => void;
};

export default function Tabuleiro({
  grade,
  clicavel = false,
  destaques = {},
  onClique,
}: Props) {
  return (
    <div className="grade" role="grid" aria-label="Tabuleiro 10 por 10">
      <div className="rotulo" />
      {COLUNAS.map((letra) => (
        <div key={letra} className="rotulo">
          {letra}
        </div>
      ))}
      {grade.map((linha, indiceLinha) => (
        <Linha
          key={indiceLinha}
          indiceLinha={indiceLinha}
          linha={linha}
          clicavel={clicavel}
          destaques={destaques}
          onClique={onClique}
        />
      ))}
    </div>
  );
}

function Linha({
  indiceLinha,
  linha,
  clicavel,
  destaques,
  onClique,
}: {
  indiceLinha: number;
  linha: Celula[];
  clicavel: boolean;
  destaques: Record<string, Destaque>;
  onClique?: (coordenada: string) => void;
}) {
  return (
    <>
      <div className="rotulo">{indiceLinha + 1}</div>
      {linha.map((simbolo, indiceColuna) => {
        const coordenada = coordenadaDeClique(indiceLinha, indiceColuna);
        const classes = classeCelula(simbolo, clicavel, destaques[coordenada]);
        const rotulo = `${coordenada}, ${estadoAcessivel(simbolo)}`;
        if (!clicavel) {
          return (
            <div
              key={coordenada}
              className={classes}
              data-coordenada={coordenada}
              role="gridcell"
              aria-label={rotulo}
            />
          );
        }
        return (
          <button
            key={coordenada}
            type="button"
            className={classes}
            data-coordenada={coordenada}
            aria-label={rotulo}
            onClick={() => onClique?.(coordenada)}
          />
        );
      })}
    </>
  );
}
