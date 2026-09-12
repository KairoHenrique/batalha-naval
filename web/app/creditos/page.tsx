import NavVoltar from "@/app/components/NavVoltar";

export default function PaginaCreditos() {
  return (
    <>
      <NavVoltar />
      <h1>Créditos</h1>
      <section className="console creditos">
        <p>
          <strong>Kairo Henrique Ferreira Martins</strong>
        </p>
        <p>Programação em Python — CEFET-MG Divinópolis</p>
        <p>Professor Guido Pantuza</p>
        <p>GPTech Games</p>
      </section>
    </>
  );
}
