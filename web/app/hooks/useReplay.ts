"use client";

import { useEffect, useState } from "react";
import { obterReplay } from "@/lib/api";

export function useReplay() {
  const [linhas, setLinhas] = useState<string[]>([]);
  const [existe, setExiste] = useState(true);
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    obterReplay()
      .then((dados) => {
        setExiste(dados.existe);
        setLinhas(dados.linhas);
      })
      .catch((falha) =>
        setErro(
          falha instanceof Error ? falha.message : "Falha ao ler o replay.",
        ),
      )
      .finally(() => setCarregando(false));
  }, []);

  return { linhas, existe, erro, carregando };
}
