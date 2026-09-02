"""Ponto de entrada do Batalha Naval (GPTech Games).

    python main.py
"""

from __future__ import annotations

from menu import iniciar_menu


def main() -> int:
    """Abre o menu texto (RF01)."""
    try:
        iniciar_menu()
        return 0
    except KeyboardInterrupt:
        print("\nSaindo.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
