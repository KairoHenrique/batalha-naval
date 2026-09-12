"use client";

import { useEffect, useState } from "react";
import { obterEstatisticas } from "@/lib/api";

export type LinhaEstatistica = {
  nome: string;
  partidas: number;
  vitorias: number;
  tiros: number;
  acertos: number;
  aproveitamento: number;
};

export function useEstatisticas() {
  const [linhas, setLinhas] = useState<LinhaEstatistica[]>([]);
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    obterEstatisticas()
      .then((dados) => setLinhas(dados.jogadores))
      .catch((falha) =>
        setErro(
          falha instanceof Error
            ? falha.message
            : "Nao foi possivel ler as estatisticas.",
        ),
      )
      .finally(() => setCarregando(false));
  }, []);

  return { linhas, erro, carregando };
}
