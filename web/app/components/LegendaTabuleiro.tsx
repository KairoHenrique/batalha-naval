export default function LegendaTabuleiro() {
  return (
    <div className="legenda" aria-hidden="true">
      <span>
        <i className="amostra agua" /> Água
      </span>
      <span>
        <i className="amostra navio" /> Navio
      </span>
      <span>
        <i className="amostra acerto" /> Acerto
      </span>
      <span>
        <i className="amostra agua-tiro" /> Tiro na água
      </span>
    </div>
  );
}
