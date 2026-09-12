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

- **Data:** 31/08/2026
- **O que foi feito:** `montar_partida_pvp` com conferência de cada um e
  “passe o computador”. Loop unificado `jogar()` (PvC e PvP). Tela de fim
  no mockup 6.5: vencedor, total de jogadas, tempo HH:MM:SS, atalhos
  replay (aviso T8) / nova partida / menu.
- **Dificuldades:** No PvP o tabuleiro exibido tem de ser o do atacante da
  vez, não sempre o jogador 1. Nova partida no fim não pode perder o menu.
- **Como foram superadas:** `_exibir_tabuleiros(partida, visao)`. Fim devolve
  `nova` ou `menu`; o menu chama `iniciar_nova_partida()` de novo se for nova.
- **Anotações:** Replay [1] ainda é stub do T8.

### T7. IA fácil / médio / difícil

- **Data:** 31/08/2026
- **O que foi feito:** `computador.py` com três níveis. Fácil: aleatório.
  Médio: hunt-and-target (fila de vizinhos após acerto; se dois acertos
  alinharem, estende o eixo). Difícil: o mesmo + parity (caça só em
  (linha+coluna) par). Afundado limpa a fila. `partida._turno_computador`
  usa a dificuldade escolhida no menu.
- **Dificuldades:** Manter a fila só com casas ainda livres; não caçar
  depois de afundar (vizinhos de um navio morto são água).
- **Como foram superadas:** `escolher_jogada` descarta alvos que já saíram
  de `livres`. `registrar_resultado_ia(..., "afundado")` zera fila e
  acertos abertos. Teste: acerto → vizinho; afundado → fila vazia; difícil
  começa em casa de paridade par.
- **Anotações:** Menu opção 1 → PvC → 1/2/3. Sem dependências extras.

---

## Semana 4 — Stats, replay e GUI web

### T8. `estatisticas.py` + `replay.py`

- **Data:** 01/09/2026
- **O que foi feito:** Persistência em `data/estatisticas.json` e
  `data/ultima_partida.json`. Menu 2 mostra partidas, vitórias, tiros,
  acertos e aproveitamento (só apelido humano; CPU não entra). Menu 3 e
  opção [1] do fim reproduzem o histórico (Enter / Q), mockup 6.6.
  `persistir_partida_encerrada` grava uma vez só.
- **Dificuldades:** Reabrir o replay no fim não pode somar de novo nas
  stats. JSON corrompido não pode derrubar o menu.
- **Como foram superadas:** Flag `partida.persistida`. Leitura trata
  arquivo ausente/inválido como vazio. Escrita via `.tmp` + `replace`.
- **Anotações:** JSON em `data/` está no `.gitignore`. Teste: vitória da
  Ana, CPU fora das stats, linha `Jogada 01/14`.

### T9. `partida.py` + `api.py` (localhost:8000)

- **Data:** 02/09/2026 (código); **12/09/2026** (aceite do professor)
- **O que foi feito:** `criar_partida` e `executar_turno_computador` em
  `partida.py` (sem I/O de terminal). `api.py` FastAPI em `:8000`: criar
  partida, posicionar/retirar frota, tiros, hotseat PvP, stats e replay.
  CORS só para localhost:3000. Menu texto ganhou opção 6 (Abrir).
- **Dificuldades:** A GUI não pode vazar o tabuleiro do oponente (`N`).
  No PvP, após o tiro o próximo jogador ainda não está na frente da tela.
- **Como foram superadas:** Estado público oculta `N` inimigo. Com
  `aguardando_troca`, a API não envia tabuleiros até `POST /partidas/pronto`.
- **Anotações:** Professor aceitou FastAPI + Next.js no lugar de
  Tkinter/Pygame. Entra no GitHub nesta data.

### T10. Next.js (localhost:3000)

- **Data:** 02/09/2026 (código); **12/09/2026** (aceite do professor)
- **O que foi feito:** App em `web/` (menu, paleta para arrastar navios,
  tabuleiro clicável 10×10, stats, replay, créditos). Proxy `/backend` →
  `127.0.0.1:8000`. Visual marinho/ouro. Menu opção 6 sobe API+Next e
  abre http://127.0.0.1:3000 no navegador.
- **Dificuldades:** Dois processos (API + Next). Clique na célula precisa
  virar `C5` como no modo texto.
- **Como foram superadas:** Rewrite no Next; `coordenadaDeClique` usa A–J
  e 1–10. Rodar: `uvicorn api:app --port 8000` e `npm run dev` em `web/`.
- **Anotações:** Aceite do professor em 12/09/2026. Commit da GUI extra.

---

## Semana 5 — Documentação

### T11. README, diário completo e checklist de aceite

- **Data:** 12/09/2026
- **O que foi feito:** Professor aceitou FastAPI + Next.js. README e diário
  atualizados. Menu texto 1–5 (mockup) + 6 Abrir (atalho da GUI).
- **Dificuldades:** O mockup 6.1 tem 5 itens; a GUI extra precisa de entrada.
- **Como foram superadas:** Opção 6 só dispara o navegador. O jogo texto
  continua nas opções 1–5. A partida web (menu, frota, tiros, stats, replay)
  roda em localhost:3000.
- **Anotações:** Modo texto cobre RF01–RF13. GUI é bônus.
