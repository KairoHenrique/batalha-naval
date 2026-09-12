type Dificuldade = "facil" | "medio" | "dificil";

type Props = {
  valor: Dificuldade;
  onChange: (dificuldade: Dificuldade) => void;
};

const NIVEIS: { id: Dificuldade; rotulo: string }[] = [
  { id: "facil", rotulo: "Fácil" },
  { id: "medio", rotulo: "Médio" },
  { id: "dificil", rotulo: "Difícil" },
];

export default function SeletorDificuldade({ valor, onChange }: Props) {
  return (
    <div className="rotulo-campo">
      Dificuldade
      <div className="grade-tres" role="group" aria-label="Dificuldade">
        {NIVEIS.map((nivel) => (
          <button
            key={nivel.id}
            type="button"
            className={`chip ${valor === nivel.id ? "ativo" : ""}`}
            onClick={() => onChange(nivel.id)}
          >
            {nivel.rotulo}
          </button>
        ))}
      </div>
    </div>
  );
}
