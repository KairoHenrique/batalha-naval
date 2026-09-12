type Modo = "pvc" | "pvp";

type Props = {
  valor: Modo;
  onChange: (modo: Modo) => void;
};

export default function SeletorModo({ valor, onChange }: Props) {
  return (
    <div className="rotulo-campo">
      Modo
      <div className="grade-escolha" role="group" aria-label="Modo de jogo">
        <button
          type="button"
          className={`chip ${valor === "pvc" ? "ativo" : ""}`}
          onClick={() => onChange("pvc")}
        >
          <span className="chip-titulo">Computador</span>
          <span className="chip-nota">Um jogador</span>
        </button>
        <button
          type="button"
          className={`chip ${valor === "pvp" ? "ativo" : ""}`}
          onClick={() => onChange("pvp")}
        >
          <span className="chip-titulo">Dois jogadores</span>
          <span className="chip-nota">Mesmo computador</span>
        </button>
      </div>
    </div>
  );
}
