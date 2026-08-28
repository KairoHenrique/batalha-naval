# Diário de desenvolvimento — Batalha Naval

Cronograma do enunciado (item 9). Cada tarefa tem data, o que foi feito,
dificuldades e como foram superadas. Preencher no mesmo dia do código.

---

## Semana 1 — Planejamento

### T1. Arquitetura e esqueleto de pastas

- **Data:** 28/08/2026
- **O que foi feito:** Leitura do PDF, decisões de frota (2 grandes + 3 pequenos),
  IA em 3 níveis, GUI extra em localhost (FastAPI + Next.js, sem Tkinter).
  Pastas `docs/` e `data/` criadas. Escopo desta sessão limitado ao S2-T2.
- **Dificuldades:** O enunciado não define quantos navios de cada tipo existem;
  a árvore do item 5 também não cita API/web.
- **Como foram superadas:** Frota documentada como interpretação (14 casas).
  Módulos extras (`api.py`, `web/`) ficam para a Semana 4 e não substituem
  os arquivos obrigatórios. Modo texto permanece o aceite dos 100 pts.
- **Anotações:** Entrega no GitHub + SIGAA até 29/09/2026.

---

## Semana 2 — Menu e tabuleiro

### T2. `utils.py` e `tabuleiro.py`

- **Data:** 28/08/2026
- **O que foi feito:** Constantes do tabuleiro 10x10, parse de coordenada
  Letra+Número (RN01), detecção de jogada repetida (RN02), cronômetro HH:MM:SS,
  criação/marcação/impressão da matriz no layout do mockup 6.3.
  Demonstração: `python tabuleiro.py`.
- **Dificuldades:** Alinhar a linha 10 (dois dígitos) com as linhas 1–9;
  C10 tem 3 caracteres, diferente de C5.
- **Como foram superadas:** Número da linha com alinhamento `>2`. O parser
  aceita 2 ou 3 caracteres após tirar espaços (`C5` e `C10`).
- **Anotações:** `python tabuleiro.py` imprime o exemplo do enunciado
  (X em B2, navio grande em D3–G3, O em H4, navio pequeno em C6–D6).

### T3. `navios.py` — tipos, auto-place, conferência

- **Data:**
- **O que foi feito:**
- **Dificuldades:**
- **Como foram superadas:**
- **Anotações:** *(ainda não iniciado — parado no T2)*

### T4. `main.py` + `menu.py`

- **Data:**
- **O que foi feito:**
- **Dificuldades:**
- **Como foram superadas:**
- **Anotações:** *(ainda não iniciado)*

---

## Semana 3 — Modos de jogo

### T5. Jogador x Computador + RF05/RF06

- **Data:**
- **O que foi feito:**
- **Dificuldades:**
- **Como foram superadas:**
- **Anotações:** *(ainda não iniciado)*

### T6. Dois Jogadores, conferência RF10 e fim RF07

- **Data:**
- **O que foi feito:**
- **Dificuldades:**
- **Como foram superadas:**
- **Anotações:** *(ainda não iniciado)*

### T7. IA fácil / médio / difícil

- **Data:**
- **O que foi feito:**
- **Dificuldades:**
- **Como foram superadas:**
- **Anotações:** *(ainda não iniciado)*

---

## Semana 4 — Stats, replay e GUI web

### T8. `estatisticas.py` + `replay.py`

- **Data:**
- **O que foi feito:**
- **Dificuldades:**
- **Como foram superadas:**
- **Anotações:** *(ainda não iniciado)*

### T9. `partida.py` + `api.py` (localhost:8000)

- **Data:**
- **O que foi feito:**
- **Dificuldades:**
- **Como foram superadas:**
- **Anotações:** *(ainda não iniciado)*

### T10. Next.js (localhost:3000)

- **Data:**
- **O que foi feito:**
- **Dificuldades:**
- **Como foram superadas:**
- **Anotações:** *(ainda não iniciado)*

---

## Semana 5 — Documentação

### T11. README, diário completo e checklist de aceite

- **Data:**
- **O que foi feito:**
- **Dificuldades:**
- **Como foram superadas:**
- **Anotações:** *(ainda não iniciado)*
