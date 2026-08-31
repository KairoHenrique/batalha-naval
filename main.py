"""Ponto de entrada do Batalha Naval (GPTech Games).

    python main.py          # menu texto (RF01)
    python main.py --gui    # instrucoes da interface web (bonus)
"""

from __future__ import annotations

import sys

from menu import exibir_instrucoes_gui, iniciar_menu


def main(argv: list[str] | None = None) -> int:
    """Dispara o menu texto ou a opção da GUI, conforme os argumentos."""
    argumentos = sys.argv[1:] if argv is None else argv
    try:
        if "--gui" in argumentos or "-g" in argumentos:
            exibir_instrucoes_gui()
            return 0
        iniciar_menu()
        return 0
    except KeyboardInterrupt:
        print("\nSaindo.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
