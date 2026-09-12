"use client";

import { useCallback, useEffect, useState } from "react";
import {
  obterPartida,
  type EstadoPartida,
} from "@/lib/api";

export function usePartida() {
  const [estado, setEstado] = useState<EstadoPartida | null>(null);
  const [erro, setErro] = useState("");
  const [ocupado, setOcupado] = useState(false);

  const recarregar = useCallback(async () => {
    try {
      setEstado(await obterPartida());
      setErro("");
    } catch (falha) {
      setErro(
        falha instanceof Error
          ? falha.message
          : "Partida nao encontrada. Volte ao menu.",
      );
    }
  }, []);

  useEffect(() => {
    void recarregar();
  }, [recarregar]);

  async function executar(acao: () => Promise<EstadoPartida>) {
    setOcupado(true);
    try {
      setEstado(await acao());
      setErro("");
    } catch (falha) {
      setErro(falha instanceof Error ? falha.message : "Falha na jogada.");
    } finally {
      setOcupado(false);
    }
  }

  return { estado, erro, ocupado, executar };
}
