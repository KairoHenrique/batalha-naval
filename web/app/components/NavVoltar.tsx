import Link from "next/link";

type Props = {
  contexto?: string;
};

export default function NavVoltar({ contexto }: Props) {
  return (
    <div className="nav-topo">
      <Link className="voltar" href="/">
        ← Menu
      </Link>
      {contexto ? <span>{contexto}</span> : <span />}
    </div>
  );
}
