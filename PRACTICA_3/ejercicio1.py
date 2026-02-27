"""
╔══════════════════════════════════════════════════════╗
║          ROYAL POKER — Texas Hold'em                 ║
║              Simulador en Python                     ║
╚══════════════════════════════════════════════════════╝
Funcionalidades:
  · N jugadores (2-6)
  · Fichas y apuestas por ronda (check / igualar / subir / fold)
  · Cartas cubiertas en ronda 1 (privacidad entre jugadores)
  · Análisis de probabilidades (Monte Carlo) por ronda
"""

import random
import os
import sys
from itertools import combinations

# ══════════════════════════════════════
#  COLORES ANSI
# ══════════════════════════════════════
class C: #la classe C es solo para definir los códigos de colores ANSI para imprimir texto coloreado en la terminal
    RESET  = '\033[0m' 
    BOLD   = '\033[1m' 
    DIM    = '\033[2m'
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    BLUE   = '\033[94m'
    CYAN   = '\033[96m'
    WHITE  = '\033[97m'
    GOLD   = '\033[38;5;220m'

# Funciones para aplicar colores al texto
def gold(s):   return f"{C.GOLD}{C.BOLD}{s}{C.RESET}" 
def red(s):    return f"{C.RED}{C.BOLD}{s}{C.RESET}"
def green(s):  return f"{C.GREEN}{C.BOLD}{s}{C.RESET}"
def cyan(s):   return f"{C.CYAN}{s}{C.RESET}"
def dim(s):    return f"{C.DIM}{s}{C.RESET}"
def bold(s):   return f"{C.BOLD}{s}{C.RESET}"
def yellow(s): return f"{C.YELLOW}{C.BOLD}{s}{C.RESET}"

# ══════════════════════════════════════
#  ESTRUCTURAS
# ══════════════════════════════════════
class Card:
    SUITS       = {'♠': 'black', '♥': 'red', '♦': 'red', '♣': 'black'} #suits son los palos de las cartas, cada uno tiene un color asociado
    VALUE_NAMES = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}

    def __init__(self, suit: str, value: int): #suit es el palo de la carta (♠, ♥, ♦, ♣) y value es el valor numérico (1-13)
        self.suit  = suit
        self.value = value

    @property #name es una propiedad que devuelve el nombre de la carta (A, 2-10, J, Q, K) según su valor
    def name(self) -> str:
        return self.VALUE_NAMES.get(self.value, str(self.value))

    @property #is_red es una propiedad que devuelve True si la carta es de color rojo (♥ o ♦) y False si es de color negro (♠ o ♣)
    def is_red(self) -> bool:
        return self.SUITS[self.suit] == 'red'

    def __str__(self) -> str: 
        clr = C.RED if self.is_red else C.WHITE
        return f"{clr}{C.BOLD}{self.name}{self.suit}{C.RESET}"

    def __repr__(self) -> str:
        return f"{self.name}{self.suit}" 

class Player: #Representación de cada jugador
    def __init__(self, player_id: int, name: str, chips: int = 1000):
        self.id:        int   = player_id
        self.name:      str   = name
        self.chips:     int   = chips   # fichas actuales
        self.cards:     list  = []
        self.folded:    bool  = False   
        self.best_hand: str   = ''
        self.round_bet: int   = 0       # apuesta en la ronda actual
        self.total_bet: int   = 0       # apuesta total en la partida

#Estado global del juego
class GameState:
    def __init__(self):
        self.deck:          list = []
        self.community:     list = []
        self.players:       list = []
        self.pot:           int  = 0
        self.round:         int  = 0
        self.prob_history:  list = []

# ══════════════════════════════════════
#  BARAJA
# ══════════════════════════════════════
def create_deck() -> list: #Crea una baraja estándar de 52 cartas generando una lista de objetos Card para cada combinación de palo y valor. Es decir, genera las cartas del 1 al 13 para cada uno de los cuatro palos (♠, ♥, ♦, ♣) y las devuelve como una lista.
    return [Card(s, v) for s in Card.SUITS for v in range(1, 14)] # Card.SUITS es un diccionario que contiene los palos de las cartas y Card.VALUE_NAMES es un diccionario que contiene los nombres de las cartas especiales (A, J, Q, K). La función utiliza una comprensión de listas para crear una lista de objetos Card para cada combinación de palo y valor. El resultado es una lista de 52 cartas que representa una baraja estándar. Una comprensión de listas es una forma concisa de crear listas en Python utilizando una sintaxis similar a la de los bucles for. En este caso, se itera sobre cada palo en Card.SUITS y cada valor del 1 al 13 para crear un objeto Card correspondiente a esa combinación de palo y valor. El resultado es una lista de objetos Card que representa una baraja completa.
    # La función create_deck() devuelve esta lista de cartas, que luego puede ser utilizada para mezclar y repartir a los jugadores en el juego de poker.
def shuffle_deck(deck: list) -> list: #Mezcla la baraja utilizando random.shuffle() y devuelve la baraja mezclada. La función toma una lista de cartas (deck) como argumento, crea una copia de esa lista para evitar modificar la original, y luego utiliza random.shuffle() para mezclar los elementos de la lista de manera aleatoria. Finalmente, devuelve la lista mezclada.
    d = deck.copy()
    random.shuffle(d)
    return d

def deal_card(deck: list) -> Card: #Reparte una carta de la baraja. La función toma una lista de cartas (deck) como argumento, utiliza deck.pop() para eliminar y devolver el último elemento de la lista, que representa la carta que se reparte. Esto simula el acto de repartir una carta desde la parte superior de la baraja. La función devuelve el objeto Card que ha sido repartido. Es decir, cada vez que se llama a deal_card(), se elimina una carta de la baraja y se devuelve esa carta para ser asignada a un jugador o al tablero comunitario.
    return deck.pop() #deck.pop() elimina y devuelve el último elemento de la lista deck, que representa la carta que se reparte. Esto simula el acto de repartir una carta desde la parte superior de la baraja. La función deal_card() devuelve el objeto Card que ha sido repartido, lo que permite asignar esa carta a un jugador o al tablero comunitario en el juego de poker.

# ══════════════════════════════════════
#  EVALUACIÓN DE MANOS
# ══════════════════════════════════════
# 1. AS en 1 o 14 según la mano (escalera baja o alta), 2. Ordenar por valor y palo, 3. Verificar color, escalera, pares, tríos, póker, etc. para asignar ranking a la mano. 4. devolver tupla (ranking, nombre de mano, valores para desempate)
def evaluate_hand(cards: list) -> tuple: 
    vals     = sorted([14 if c.value == 1 else c.value for c in cards], reverse=True) 
    vals_low = sorted([c.value for c in cards], reverse=True) 
    suits    = [c.suit for c in cards] 

    is_flush    = len(set(suits)) == 1 
    is_straight = _check_straight(vals) or _check_straight(vals_low)

    counts: dict = {}
    for v in vals:
        counts[v] = counts.get(v, 0) + 1
    groups = sorted(counts.values(), reverse=True)

    if is_flush and _check_straight(vals) and vals[0] == 14:
        return (0, 'Corrida Real',     vals)
    if is_flush and is_straight:
        return (1, 'Corrida de Color', vals)
    if groups[0] == 4:
        return (2, 'Poker',            vals)
    if groups[0] == 3 and len(groups) > 1 and groups[1] == 2:
        return (3, 'Casa Llena',       vals)
    if is_flush:
        return (4, 'Color',            vals)
    if is_straight:
        return (5, 'Corrida',          vals)
    if groups[0] == 3:
        return (6, 'Tercia',           vals)
    if groups[0] == 2 and len(groups) > 1 and groups[1] == 2:
        return (7, 'Doble Par',        vals)
    if groups[0] == 2:
        return (8, 'Un Par',           vals)
    return     (9, 'Carta Alta',       vals)

def _check_straight(sv: list) -> bool: # Verifica si los valores de las cartas forman una escalera (secuencia de números consecutivos). La función toma una lista de valores de cartas (sv) como argumento y verifica si cada valor es exactamente 1 menos que el siguiente valor en la lista. Si esto se cumple para todos los pares de valores adyacentes, entonces la función devuelve True, indicando que los valores forman una escalera. De lo contrario, devuelve False.
    return all(sv[i] - sv[i+1] == 1 for i in range(len(sv)-1)) 

def get_best_hand(player_cards: list, community: list) -> tuple: # Dada la mano del jugador (2 cartas) y las cartas comunitarias (hasta 5 cartas), esta función evalúa todas las combinaciones posibles de 5 cartas y devuelve la mejor mano posible. La función toma dos listas como argumentos: player_cards, que contiene las cartas del jugador, y community, que contiene las cartas comunitarias en la mesa. Combina estas dos listas para obtener todas las cartas disponibles para el jugador y luego utiliza itertools.combinations para generar todas las combinaciones posibles de 5 cartas. Para cada combinación, evalúa la mano utilizando la función evaluate_hand() y mantiene un registro de la mejor mano encontrada. Finalmente, devuelve una tupla que representa la mejor mano posible para el jugador dada su mano y las cartas comunitarias.
    all_cards = player_cards + community
    best = (99, 'Nada', [])
    for combo in combinations(all_cards, 5):
        result = evaluate_hand(list(combo))
        if result[0] < best[0]:
            best = result
    return best

# ══════════════════════════════════════
#  PROBABILIDADES — Monte Carlo
# ══════════════════════════════════════
def estimate_win_probabilities(active_players: list, known_community: list,
                               remaining_deck: list, simulations: int = 600) -> dict:
    """
    Simula 'simulations' manos completando el tablero aleatoriamente.
    Retorna dict {player_id: win_pct, ..., 'tie': tie_pct}.
    """
    needed  = 5 - len(known_community)
    wins    = {p.id: 0 for p in active_players}
    ties    = 0

    for _ in range(simulations):
        sample    = random.sample(remaining_deck, needed)
        community = known_community + sample

        results = [(get_best_hand(p.cards, community), p) for p in active_players]
        best_rank = min(r[0][0] for r in results)
        candidates = [p for (r, p) in results if r[0] == best_rank]

        if len(candidates) == 1:
            wins[candidates[0].id] += 1
        else:
            # desempate por carta más alta del jugador
            best_hv = max(
                max(14 if c.value == 1 else c.value for c in p.cards)
                for p in candidates
            )
            top = [p for p in candidates
                   if max(14 if c.value == 1 else c.value for c in p.cards) == best_hv]
            if len(top) == 1:
                wins[top[0].id] += 1
            else:
                ties += 1

    total = simulations
    result = {p.id: wins[p.id] / total * 100 for p in active_players}
    result['tie'] = ties / total * 100
    return result


def prob_bar(pct: float, width: int = 18) -> str:
    filled = round(pct / 100 * width)
    bar    = '█' * filled + '░' * (width - filled)
    clr    = C.GREEN if pct >= 55 else (C.YELLOW if pct >= 35 else C.RED)
    return f"{clr}{bar}{C.RESET} {pct:5.1f}%"


def print_probabilities(state: GameState, label: str):
    active = [p for p in state.players if not p.folded]
    if len(active) < 2:
        return
    remaining = list(state.deck)
    probs = estimate_win_probabilities(active, state.community, remaining)

    state.prob_history.append({'label': label, 'probs': probs,
                                'players': [(p.id, p.name) for p in active]})

    print(f"\n  {gold('── Probabilidades de victoria ──')}  {dim(label)}")
    for p in active:
        print(f"  {p.name:<12} {prob_bar(probs[p.id])}")
    if probs.get('tie', 0) > 0.5:
        print(f"  {'Empate':<12} {prob_bar(probs['tie'])}")


def print_prob_analysis(history: list):
    if not history:
        return
    print(f"\n  {gold('╔══════════════════════════════════════════════╗')}")
    print(f"  {gold('║')}   {bold('ANALISIS DE PROBABILIDADES POR RONDA')}     {gold('║')}")
    print(f"  {gold('╚══════════════════════════════════════════════╝')}\n")
    for entry in history:
        print(f"  {cyan(entry['label'])}")
        for pid, pname in entry['players']:
            print(f"    {pname:<12} {prob_bar(entry['probs'][pid])}")
        if entry['probs'].get('tie', 0) > 0.5:
            print(f"    {'Empate':<12} {prob_bar(entry['probs']['tie'])}")
        print()

# ══════════════════════════════════════
#  DISPLAY
# ══════════════════════════════════════
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print(gold("╔══════════════════════════════════════════════════════╗"))
    print(gold("║") + f"      {C.BOLD}{C.WHITE}♠  ROYAL POKER — Texas Hold'em  ♥{C.RESET}          " + gold("║"))
    print(gold("║") + f"           {dim('Simulador · N Jugadores')}                    " + gold("║"))
    print(gold("╚══════════════════════════════════════════════════════╝"))
    print()

def print_card_box(card: Card) -> list:
    vn  = card.name
    s   = card.suit
    clr = C.RED if card.is_red else C.WHITE
    pad = ' ' if len(vn) == 1 else ''
    return [
        f"{clr}┌─────┐{C.RESET}",
        f"{clr}│{vn}{pad}   │{C.RESET}",
        f"{clr}│  {s}  │{C.RESET}",
        f"{clr}│   {pad}{vn}│{C.RESET}",
        f"{clr}└─────┘{C.RESET}",
    ]

def print_hidden_card() -> list:
    return [
        f"{C.BLUE}┌─────┐{C.RESET}",
        f"{C.BLUE}│▓▓▓▓▓│{C.RESET}",
        f"{C.BLUE}│▓ ♦ ▓│{C.RESET}",
        f"{C.BLUE}│▓▓▓▓▓│{C.RESET}",
        f"{C.BLUE}└─────┘{C.RESET}",
    ]

def print_cards_row(cards: list, hidden=False):
    if not cards:
        print(dim("  (sin cartas)"))
        return
    rows = [print_hidden_card() if hidden else print_card_box(c) for c in cards]
    for line in range(5):
        print("  " + "  ".join(r[line] for r in rows))

def print_community(community: list, total=5):
    print(gold("  ─── CARTAS COMUNITARIAS ───"))
    cards_to_show = community + [None] * (total - len(community))
    rows = []
    for c in cards_to_show:
        if c is None:
            rows.append([f"{C.DIM}┌─────┐{C.RESET}", f"{C.DIM}│     │{C.RESET}",
                         f"{C.DIM}│  ?  │{C.RESET}", f"{C.DIM}│     │{C.RESET}",
                         f"{C.DIM}└─────┘{C.RESET}"])
        else:
            rows.append(print_card_box(c))
    for line in range(5):
        print("  " + "  ".join(r[line] for r in rows))

def print_table(state: GameState, visible_id: int = -1):
    """Muestra la mesa. visible_id = id del jugador cuyas cartas se muestran (-1 = todos ocultos)."""
    clear()
    print_banner()
    print(gold(f"  {'─'*52}"))
    active_str = " · ".join(
        (green if not p.folded else dim)(p.name) for p in state.players
    )
    print(f"  {bold('RONDA')} {state.round}/4   {gold('•')}   {bold('POZO:')} {gold(f'🪙 {state.pot}')}")
    print(f"  {dim('Jugadores:')} {active_str}")
    print(gold(f"  {'─'*52}"))
    print()

    # Jugadores (todos, marcando fold)
    for p in state.players:
        status = red(" [FOLD]") if p.folded else ""
        hand_str = f"  {gold('Mano: ' + p.best_hand)}" if p.best_hand else ""
        show = (visible_id == p.id)
        label = cyan(f"{'▶ ' if show else '  '}{p.name}") + f"  {dim(f'Fichas: {p.chips}')}{status}"
        print(f"  {label}{hand_str}")
        print_cards_row(p.cards, hidden=not show)
        print()

    print_community(state.community)
    print()
    print(gold(f"  {'─'*52}"))

def press_enter(msg="  Presiona Enter para continuar..."):
    input(f"\n{dim(msg)}")

def ask_peek(player: Player):
    """Muestra las cartas del jugador después de que presione Enter."""
    print(f"\n  {bold(player.name)}: presiona Enter cuando nadie te este viendo...")
    input(f"  {gold('→')} ")

# ══════════════════════════════════════
#  SISTEMA DE APUESTAS
# ══════════════════════════════════════
def betting_turn(state: GameState, player: Player, current_bet: int) -> int:
    """
    Turno de apuesta de un jugador.
    current_bet = apuesta más alta en la ronda hasta ahora.
    Retorna la nueva apuesta total del jugador en esta ronda,
    o -1 si hace fold.
    """
    to_call = max(0, current_bet - player.round_bet)

    print(f"\n  {bold(player.name)}  |  Fichas: {gold(str(player.chips))}  |  Pozo: {gold(str(state.pot))}")
    if to_call > 0:
        print(f"  {dim(f'Para igualar necesitas: {to_call} fichas')}")

    if player.chips == 0:
        print(f"  {dim('Sin fichas — all-in automatico.')}")
        return player.round_bet

    if to_call > 0:
        print(f"  {green('[1]')} Igualar  ({to_call} fichas)")
        print(f"  {yellow('[2]')} Subir")
        print(f"  {red('[3]')} Fold (retirarse)")
    else:
        print(f"  {green('[1]')} Check (pasar)")
        print(f"  {yellow('[2]')} Apostar")
        print(f"  {red('[3]')} Fold (retirarse)")

    while True:
        choice = input(f"  {gold('→')} ").strip()
        if choice not in ('1', '2', '3'):
            print(f"  {dim('Opcion invalida.')}")
            continue

        if choice == '3':
            player.folded = True
            return -1

        if choice == '1':
            amount = min(to_call, player.chips)
            player.chips     -= amount
            player.round_bet += amount
            player.total_bet += amount
            state.pot        += amount
            action = f"iguala {amount}" if amount > 0 else "pasa (check)"
            print(f"  {green(player.name + f' {action}. Pozo: {state.pot}')}")
            return player.round_bet

        # choice == '2'
        min_raise = max(1, to_call + 1)
        print(f"  Cantidad (min {min_raise}, max {player.chips}):")
        while True:
            try:
                amt = int(input(f"  {gold('→')} ").strip())
                if amt < min_raise:
                    print(f"  {dim(f'Minimo: {min_raise}')}")
                    continue
                if amt > player.chips:
                    print(f"  {dim(f'Maximo: {player.chips}')}")
                    continue
                break
            except ValueError:
                print(f"  {dim('Ingresa un numero.')}")

        player.chips     -= amt
        player.round_bet += amt
        player.total_bet += amt
        state.pot        += amt
        print(f"  {yellow(player.name + f' apuesta/sube a {player.round_bet}. Pozo: {state.pot}')}")
        return player.round_bet


def full_betting_round(state: GameState, label: str) -> bool:
    """
    Ronda de apuestas para todos los jugadores activos.
    Permite re-apuestas si alguien sube (hasta que todos igualen).
    Retorna False si solo queda 1 jugador activo.
    """
    active = [p for p in state.players if not p.folded]
    if len(active) < 2:
        return False

    for p in active:
        p.round_bet = 0

    print(f"\n  {gold(f'── Apuestas: {label} ──')}")

    # Recorremos en orden; si alguien sube, se hace otra vuelta
    current_bet = 0
    acted = set()
    queue = list(active)

    while queue:
        player = queue.pop(0)
        if player.folded:
            continue

        print_table(state, visible_id=player.id)
        print(f"\n  {gold(f'── Apuestas: {label} ──')}")

        new_bet = betting_turn(state, player, current_bet)

        if new_bet == -1:
            print(f"\n  {red(player.name + ' se retira (fold).')}")
            press_enter()
            active = [p for p in state.players if not p.folded]
            if len(active) < 2:
                return False
            continue

        acted.add(player.id)

        if new_bet > current_bet:
            # Subida: todos los que ya actuaron deben volver a actuar
            current_bet = new_bet
            for p in state.players:
                if not p.folded and p.id != player.id and p.id in acted:
                    queue.append(p)

        press_enter("  Pasando al siguiente jugador... (Enter)")

    return True

# ══════════════════════════════════════
#  LÓGICA DE RONDAS
# ══════════════════════════════════════
def round_1(state: GameState) -> bool:
    state.round = 1

    # Cada jugador ve sus cartas en privado (cubiertas para los demás)
    for player in state.players:
        print_table(state, visible_id=-1)
        print(f"\n  {gold('── RONDA 1: Reparto inicial ──')}")
        print(f"  {dim('Cartas cubiertas — cada jugador las ve en privado.')}")
        ask_peek(player)
        print_table(state, visible_id=player.id)
        print(f"\n  {gold('── RONDA 1: Reparto inicial ──')}")
        print_probabilities(state, f'Ronda 1 — vista de {player.name}')
        press_enter("  Cubre la pantalla y pasa el turno... (Enter)")

    return full_betting_round(state, 'Ronda 1')


def round_2(state: GameState) -> bool:
    state.round = 2
    for _ in range(3):
        state.community.append(deal_card(state.deck))

    print_table(state, visible_id=-1)
    print(f"\n  {gold('── RONDA 2: El Flop (3 cartas) ──')}")
    print_probabilities(state, 'Ronda 2 — Flop')
    press_enter()
    return full_betting_round(state, 'Flop')


def round_3(state: GameState) -> bool:
    state.round = 3
    state.community.append(deal_card(state.deck))

    print_table(state, visible_id=-1)
    print(f"\n  {gold('── RONDA 3: El Turn (4ª carta) ──')}")
    print_probabilities(state, 'Ronda 3 — Turn')
    press_enter()
    return full_betting_round(state, 'Turn')


def round_4(state: GameState) -> tuple:
    state.round = 4
    state.community.append(deal_card(state.deck))

    active = [p for p in state.players if not p.folded]

    # Evaluar manos de todos los activos
    for p in active:
        _, n, _ = get_best_hand(p.cards, state.community)
        p.best_hand = n

    print_table(state, visible_id=999)   # 999 = mostrar todos
    print(f"\n  {gold('── RONDA 4: El River — SHOWDOWN ──')}")
    print_probabilities(state, 'Ronda 4 — River (showdown)')

    print(f"\n  {bold('Manos finales:')}")
    for p in active:
        print(f"    {p.name:<14} {gold(p.best_hand)}")
    press_enter()

    # Determinar ganador
    results = [(get_best_hand(p.cards, state.community), p) for p in active]
    best_rank = min(r[0][0] for r in results)
    candidates = [p for (r, p) in results if r[0] == best_rank]

    if len(candidates) == 1:
        w = candidates[0]
        loser_hand = next(n for (_, n, _), p in results if p.id != w.id) if len(active) == 2 else ''
        reason = f"{w.name} gana con {w.best_hand}" + (f" contra {loser_hand}." if loser_hand else ".")
        return w, reason, w.best_hand

    # Desempate por carta más alta personal
    best_hv = max(max(14 if c.value==1 else c.value for c in p.cards) for p in candidates)
    top = [p for p in candidates
           if max(14 if c.value==1 else c.value for c in p.cards) == best_hv]

    if len(top) == 1:
        w = top[0]
        return w, f"Empate en {w.best_hand}. {w.name} gana por carta mas alta.", w.best_hand

    names = " y ".join(p.name for p in top)
    return None, f"Empate total entre {names}.", top[0].best_hand

# ══════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════
def print_winner(winner, reason: str, hand: str = ''):
    print()
    if winner:
        print(gold("  ╔══════════════════════════════════════╗"))
        print(gold("  ║") + f"    {C.BOLD}{C.YELLOW}{winner.name.upper()} GANA!{C.RESET}                  " + gold("║"))
        if hand:
            print(gold("  ║") + f"  {green(hand):<38}" + gold("║"))
        print(gold("  ╚══════════════════════════════════════╝"))
    else:
        print(gold("  ╔══════════════════════════════════════╗"))
        print(gold("  ║") + f"    {C.BOLD}¡EMPATE!{C.RESET}                             " + gold("║"))
        print(gold("  ╚══════════════════════════════════════╝"))
    print(f"\n  {dim(reason)}\n")

# ══════════════════════════════════════
#  MAIN GAME LOOP
# ══════════════════════════════════════
# Funciones para preguntar al usuario el número de jugadores y las fichas iniciales por jugador, asegurándose de que los valores ingresados sean válidos (entre 2 y 6 jugadores, y al menos 10 fichas). Estas funciones utilizan un bucle while para solicitar la entrada del usuario hasta que se ingrese un valor válido, y manejan excepciones para asegurarse de que se ingresen números enteros.
def ask_num_players() -> int:
    print(f"  {bold('Numero de jugadores')} {dim('(2-6)')}:")
    while True:
        try:
            n = int(input(f"  {gold('→')} ").strip())
            if 2 <= n <= 6:
                return n
            print(f"  {dim('Ingresa un numero entre 2 y 6.')}")
        except ValueError:
            print(f"  {dim('Ingresa un numero.')}")


def ask_chips() -> int:
    print(f"  {bold('Fichas iniciales por jugador')} {dim('(ej. 1000)')}:")
    while True:
        try:
            n = int(input(f"  {gold('→')} ").strip())
            if n >= 10:
                return n
            print(f"  {dim('Minimo 10 fichas.')}")
        except ValueError:
            print(f"  {dim('Ingresa un numero.')}")


def play_game():
    clear()
    print_banner()
    print(f"  {bold('Bienvenido a Royal Poker — Texas Hold em')}")
    print(f"  {dim('Baraja de 52 cartas · Apuestas + Probabilidades + N jugadores')}\n")

    num_players  = ask_num_players()
    chips_start  = ask_chips()

    state         = GameState()
    state.deck    = shuffle_deck(create_deck())
    state.players = [Player(i+1, f"Jugador {i+1}", chips_start)
                     for i in range(num_players)]

    for p in state.players:
        p.cards = [deal_card(state.deck), deal_card(state.deck)]

    winner    = None
    reason    = ''
    hand_name = ''

    def sole_survivor():
        active = [p for p in state.players if not p.folded]
        return active[0] if len(active) == 1 else None

    # ── Ronda 1
    if not round_1(state):
        winner = sole_survivor()
        reason = f"Solo queda {winner.name} en la partida." if winner else "Todos se retiraron."
    # ── Ronda 2
    elif not round_2(state):
        winner = sole_survivor()
        reason = f"Solo queda {winner.name} tras el flop." if winner else "Todos se retiraron."
    # ── Ronda 3
    elif not round_3(state):
        winner = sole_survivor()
        reason = f"Solo queda {winner.name} tras el turn." if winner else "Todos se retiraron."
    # ── Showdown
    else:
        winner, reason, hand_name = round_4(state)

    if winner:
        winner.chips += state.pot

    # Mostrar todos los jugadores con cartas visibles
    for p in state.players:
        p.best_hand = p.best_hand or ''
    print_table(state, visible_id=999)
    print_winner(winner, reason, hand_name)
    print_prob_analysis(state.prob_history)

    print(f"  {bold('Fichas finales:')}")
    for p in state.players:
        gained = p.chips - chips_start
        sign   = green(f"+{gained}") if gained >= 0 else red(str(gained))
        print(f"    {p.name:<14} {gold(str(p.chips))}  ({sign})")
    print()

    print(f"  {bold('Jugar otra partida?')}  {green('[1]')} Si   {red('[2]')} No")
    if input(f"  {gold('→')} ").strip() in ('1', ''):
        play_game()
    else:
        clear()
        print_banner()
        print(f"  {gold('Gracias por jugar Royal Poker!')}\n")
        sys.exit(0)


if __name__ == '__main__':
    play_game()