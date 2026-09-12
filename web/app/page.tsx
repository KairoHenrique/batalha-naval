"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import Botao from "@/app/components/Botao";
import SeletorDificuldade from "@/app/components/SeletorDificuldade";
import SeletorModo from "@/app/components/SeletorModo";
import { novaPartida } from "@/lib/api";

export default function PaginaMenu() {
  const roteador = useRouter();
  const [modo, setModo] = useState<"pvc" | "pvp">("pvc");
  const [dificuldade, setDificuldade] = useState<"facil" | "medio" | "dificil">(
    "medio",
  );
  const [nomeJ1, setNomeJ1] = useState("");
  const [nomeJ2, setNomeJ2] = useState("");
  const [erro, setErro] = useState("");
  const [enviando, setEnviando] = useState(false);

  async function comecar(evento: FormEvent) {
    evento.preventDefault();
    setErro("");
    setEnviando(true);
    try {
      await novaPartida({
        modo,
        dificuldade,
        nome_j1: nomeJ1,
        nome_j2: modo === "pvp" ? nomeJ2 : "Computador",
      });
      roteador.push("/jogo");
    } catch (falha) {
      setErro(
        falha instanceof Error
          ? falha.message
          : "Nao foi possivel criar a partida.",
      );
    } finally {
      setEnviando(false);
    }
  }

  return (
    <section className="console console-menu" aria-labelledby="titulo-menu">
      <form className="formulario" onSubmit={comecar}>
        <h1 id="titulo-menu">Nova partida</h1>
        <SeletorModo valor={modo} onChange={setModo} />
        {modo === "pvc" ? (
          <SeletorDificuldade valor={dificuldade} onChange={setDificuldade} />
        ) : null}
        <label className="rotulo-campo">
          Nome do Jogador 1
          <input
            className="campo"
            value={nomeJ1}
            maxLength={40}
            placeholder="Nome do Jogador 1"
            autoComplete="nickname"
            onChange={(evento) => setNomeJ1(evento.target.value)}
          />
        </label>
        {modo === "pvp" ? (
          <label className="rotulo-campo">
            Nome do Jogador 2
            <input
              className="campo"
              value={nomeJ2}
              maxLength={40}
              placeholder="Nome do Jogador 2"
              autoComplete="nickname"
              onChange={(evento) => setNomeJ2(evento.target.value)}
            />
          </label>
        ) : null}
        {erro ? (
          <p className="erro" role="alert">
            {erro}
          </p>
        ) : null}
        <Botao type="submit" variante="ouro" disabled={enviando}>
          {enviando ? "Preparando frota..." : "Começar"}
        </Botao>
      </form>

      <nav className="atalhos" aria-label="Outras telas">
        <Link className="item-menu" href="/estatisticas">
          Estatísticas
        </Link>
        <Link className="item-menu" href="/replay">
          Replay
        </Link>
        <Link className="item-menu" href="/creditos">
          Créditos
        </Link>
      </nav>
    </section>
  );
}
