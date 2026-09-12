"use client";

type Props = {
  children: React.ReactNode;
  type?: "button" | "submit";
  variante?: "padrao" | "ouro";
  disabled?: boolean;
  onClick?: () => void;
};

export default function Botao({
  children,
  type = "button",
  variante = "padrao",
  disabled,
  onClick,
}: Props) {
  const classe = variante === "ouro" ? "botao botao-ouro" : "botao";
  return (
    <button type={type} className={classe} disabled={disabled} onClick={onClick}>
      {children}
    </button>
  );
}
