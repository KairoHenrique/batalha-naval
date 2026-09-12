export type Celula = "~" | "N" | "X" | "O" | string;

export type NavioPendente = {
  id: string;
  tipo: "grande" | "pequeno";
  tamanho: number;
};

export type EstadoPartida = {
  fase: string;
  modo: string;
  dificuldade: string;
  nome_j1: string;
  nome_j2: string;
  mensagem: string;
  jogadas_turno: {
    valida: boolean;
    coordenada: string;
    mensagem: string;
    jogador: string;
    resultado: string;
  }[];
  aguardando_troca: boolean;
  colunas: string[];
  tabuleiro_proprio: Celula[][] | null;
  tabuleiro_tiros: Celula[][] | null;
  resumo_frota: string | null;
  vez: string | null;
  vencedor: string | null;
  total_jogadas: number;
  tempo: string;
  pode_atirar: boolean;
  restantes?: NavioPendente[];
  frota_completa?: boolean;
  pode_confirmar?: boolean;
};

const BASE = "/backend";

async function pedir<T>(caminho: string, init?: RequestInit): Promise<T> {
  const resposta = await fetch(`${BASE}${caminho}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });
  const dados = await resposta.json().catch(() => ({}));
  if (!resposta.ok) {
    const detalhe = (dados as { detail?: string }).detail;
    throw new Error(detalhe || `Erro HTTP ${resposta.status}`);
  }
  return dados as T;
}

export function novaPartida(corpo: {
  modo: "pvc" | "pvp";
  dificuldade: "facil" | "medio" | "dificil";
  nome_j1: string;
  nome_j2: string;
}) {
  return pedir<EstadoPartida>("/partidas", {
    method: "POST",
    body: JSON.stringify(corpo),
  });
}

export function obterPartida() {
  return pedir<EstadoPartida>("/partidas");
}

export function confirmarFrota() {
  return pedir<EstadoPartida>("/partidas/confirmar", { method: "POST" });
}

export function reposicionarFrota() {
  return pedir<EstadoPartida>("/partidas/reposicionar", { method: "POST" });
}

export function limparFrota() {
  return pedir<EstadoPartida>("/partidas/limpar", { method: "POST" });
}

export function posicionarNavio(corpo: {
  coordenada: string;
  horizontal: boolean;
  tipo: "grande" | "pequeno";
}) {
  return pedir<EstadoPartida>("/partidas/posicionar", {
    method: "POST",
    body: JSON.stringify(corpo),
  });
}

export function retirarNavio(coordenada: string) {
  return pedir<EstadoPartida>("/partidas/retirar", {
    method: "POST",
    body: JSON.stringify({ coordenada }),
  });
}

export function confirmarVez() {
  return pedir<EstadoPartida>("/partidas/pronto", { method: "POST" });
}

export function atirar(coordenada: string) {
  return pedir<EstadoPartida>("/partidas/jogadas", {
    method: "POST",
    body: JSON.stringify({ coordenada }),
  });
}

export function obterEstatisticas() {
  return pedir<{
    jogadores: {
      nome: string;
      partidas: number;
      vitorias: number;
      tiros: number;
      acertos: number;
      aproveitamento: number;
    }[];
  }>("/estatisticas");
}

export function obterReplay() {
  return pedir<{
    existe: boolean;
    vencedor?: string;
    total_jogadas?: number;
    duracao_segundos?: number;
    linhas: string[];
  }>("/replay");
}

export function coordenadaDeClique(linha: number, coluna: number): string {
  const letras = "ABCDEFGHIJ";
  return `${letras[coluna]}${linha + 1}`;
}
