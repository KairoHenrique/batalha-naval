import { coordenadaDeClique, type Celula } from "@/lib/api";

export type Destaque = "preview" | "preview-erro";

export function parseCoordenada(
  texto: string,
): { linha: number; coluna: number } | null {
  const bruto = texto.trim().toUpperCase();
  const letra = bruto[0];
  const numero = Number(bruto.slice(1));
  const coluna = "ABCDEFGHIJ".indexOf(letra);
  if (coluna < 0 || !Number.isInteger(numero) || numero < 1 || numero > 10) {
    return null;
  }
  return { linha: numero - 1, coluna };
}

export function casasDoNavio(
  origem: string,
  tamanho: number,
  horizontal: boolean,
): string[] | null {
  const inicio = parseCoordenada(origem);
  if (!inicio) {
    return null;
  }
  const casas: string[] = [];
  for (let deslocamento = 0; deslocamento < tamanho; deslocamento += 1) {
    const linha = horizontal ? inicio.linha : inicio.linha + deslocamento;
    const coluna = horizontal ? inicio.coluna + deslocamento : inicio.coluna;
    if (linha < 0 || linha > 9 || coluna < 0 || coluna > 9) {
      return null;
    }
    casas.push(coordenadaDeClique(linha, coluna));
  }
  return casas;
}

export function mapaDePreview(
  origem: string | null,
  tamanho: number,
  horizontal: boolean,
  grade: Celula[][],
): Record<string, Destaque> {
  if (!origem) {
    return {};
  }
  const casas = casasDoNavio(origem, tamanho, horizontal);
  if (!casas) {
    return { [origem]: "preview-erro" };
  }
  const choca = casas.some((casa) => {
    const ponto = parseCoordenada(casa);
    return ponto !== null && grade[ponto.linha][ponto.coluna] === "N";
  });
  const marca: Destaque = choca ? "preview-erro" : "preview";
  return Object.fromEntries(casas.map((casa) => [casa, marca]));
}

export function coordenadaSobPonteiro(x: number, y: number): string | null {
  const alvo = document.elementFromPoint(x, y);
  if (!(alvo instanceof Element)) {
    return null;
  }
  const celula = alvo.closest("[data-coordenada]");
  return celula?.getAttribute("data-coordenada") ?? null;
}
