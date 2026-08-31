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

- **Data:** 28/08/2026
- **O que foi feito:** Módulo `navios.py` com frota 2 grandes (4) + 3 pequenos (2).
  `gerar_frota()` posiciona sem sair do tabuleiro e sem overlap (RF03/RF04).
  `conferir_posicionamento()` mostra o tabuleiro e a lista de coordenadas;
  C confirma e R gera outra disposição (RF10). Demonstração: `python navios.py`.
- **Dificuldades:** Sortear início aleatório em qualquer casa gerava muitos
  rejeitos (navio saía do 10x10). Encaixar 5 navios às cegas podia falhar.
- **Como foram superadas:** O segmento já nasce cabendo no tabuleiro
  (`TAMANHO - comprimento`). Grandes são posicionados primeiro. Se um navio
  não encaixa, a frota inteira é gerada de novo (até 80 tentativas).
- **Anotações:** Conferência ainda é chamada direto pelo módulo; o T4 (menu)
  é quem vai disparar isso na partida. Validação: 40 frotas sem overlap.

### T4. `main.py` + `menu.py`

- **Data:** 28/08/2026
- **O que foi feito:** `main.py` (`python main.py` e `--gui`) e `menu.py` no
  layout do mockup 6.1 (opção extra 6 = interface web). Nova partida (RF08)
  escolhe modo 6.2, dificuldade no PvC, nomes e chama
  `conferir_posicionamento`. Créditos com autor/professor. Stats e replay
  avisam que entram no T8. O loop de tiros ainda não existe (T5).
- **Dificuldades:** O enunciado mostra só 5 itens no menu; o plano pede GUI
  web. Sem T5, “Nova partida” não pode atirar.
- **Como foram superadas:** Opção 6 documentada como bônus, sem quebrar o
  mockup. Depois da conferência o menu explica o T5 e volta — RF08 continua
  válido (sempre dá para começar de novo pela opção 1). Entradas fora da
  lista são recusadas no próprio `_ler_opcao`.
- **Anotações:** `python main.py` na pasta do projeto. Ctrl+C sai limpo.

---

## Semana 3 — Modos de jogo

### T5. Jogador x Computador + RF05/RF06

- **Data:** 31/08/2026
- **O que foi feito:** `jogador.py` e `partida.py`. Loop PvC com dois tabuleiros
  (próprio com N, inimigo só com tiros). `aplicar_tiro()` valida C5, rejeita
  repetida sem passar a vez (RN02) e imprime água / acerto / afundado (RF06).
  Computador atira ao acaso em casa livre (RN05, versão simples). Fim mostra
  vencedor, jogadas e tempo. PvP ainda avisa T6.
- **Dificuldades:** Depois de um tiro válido o turno já troca; testar RN02
  exige forçar o mesmo atacante. Mensagem de afundado precisa do tipo do navio.
- **Como foram superadas:** `Navio.acertos` + `esta_afundado()`. Teste
  automático de acerto, repetida e `K5`/`A0`. CPU só escolhe em
  `_casas_livres`.
- **Anotações:** Dificuldade do menu ainda não muda a IA (T7). `python main.py`
  → 1 → Jogador vs Computador.

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
