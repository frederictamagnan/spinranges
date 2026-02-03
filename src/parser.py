"""GTO Wizard data parsing utilities."""

# Hand matrix constants - exact GTO Wizard API order
RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

HANDS = [
    "AA", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
    "AKo", "KK", "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
    "AQo", "KQo", "QQ", "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
    "AJo", "KJo", "QJo", "JJ", "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s", "J3s", "J2s",
    "ATo", "KTo", "QTo", "JTo", "TT", "T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "T3s", "T2s",
    "A9o", "K9o", "Q9o", "J9o", "T9o", "99", "98s", "97s", "96s", "95s", "94s", "93s", "92s",
    "A8o", "K8o", "Q8o", "J8o", "T8o", "98o", "88", "87s", "86s", "85s", "84s", "83s", "82s",
    "A7o", "K7o", "Q7o", "J7o", "T7o", "97o", "87o", "77", "76s", "75s", "74s", "73s", "72s",
    "A6o", "K6o", "Q6o", "J6o", "T6o", "96o", "86o", "76o", "66", "65s", "64s", "63s", "62s",
    "A5o", "K5o", "Q5o", "J5o", "T5o", "95o", "85o", "75o", "65o", "55", "54s", "53s", "52s",
    "A4o", "K4o", "Q4o", "J4o", "T4o", "94o", "84o", "74o", "64o", "54o", "44", "43s", "42s",
    "A3o", "K3o", "Q3o", "J3o", "T3o", "93o", "83o", "73o", "63o", "53o", "43o", "33", "32s",
    "A2o", "K2o", "Q2o", "J2o", "T2o", "92o", "82o", "72o", "62o", "52o", "42o", "32o", "22",
]


def hand_to_matrix_pos(hand: str) -> tuple:
    """Convert hand name to (row, col) position in 13x13 matrix."""
    if len(hand) == 2:  # Pair
        r = RANKS.index(hand[0])
        return (r, r)
    elif hand.endswith('s'):  # Suited (above diagonal)
        r1, r2 = RANKS.index(hand[0]), RANKS.index(hand[1])
        return (r1, r2)
    else:  # Offsuit (below diagonal)
        r1, r2 = RANKS.index(hand[0]), RANKS.index(hand[1])
        return (r2, r1)


def matrix_pos_to_hand(row: int, col: int) -> str:
    """Convert matrix position to hand name."""
    if row == col:
        return f"{RANKS[row]}{RANKS[row]}"
    elif row < col:
        return f"{RANKS[row]}{RANKS[col]}s"
    else:
        return f"{RANKS[col]}{RANKS[row]}o"


def parse_solution(data: dict) -> dict:
    """Parse API response into readable format."""
    result = {
        "game": {
            "position": data["game"]["active_position"],
            "pot": data["game"]["pot"],
            "street": data["game"]["current_street"]["type"],
            "board": data["game"]["board"] or "preflop",
        },
        "actions": {}
    }

    for action_sol in data["action_solutions"]:
        action = action_sol["action"]
        action_name = action["display_name"]
        if action["betsize"] != "0":
            action_name = f"{action['type']} {action['betsize']}"

        strategies = {}
        for i, freq in enumerate(action_sol["strategy"]):
            if freq > 0:
                strategies[HANDS[i]] = round(freq * 100, 1)

        result["actions"][action_name] = {
            "total_freq": round(action_sol["total_frequency"] * 100, 1),
            "hands": strategies
        }

    return result


def get_hand_frequencies(data: dict) -> dict:
    """Extract per-hand frequencies from simple_hand_counters."""
    active_pos = data["game"]["active_position"]

    for player_info in data["players_info"]:
        if player_info["player"]["position"] == active_pos:
            return player_info.get("simple_hand_counters", {})
    return {}


def get_action_types(data: dict) -> dict:
    """Extract action code to type mapping from action_solutions."""
    action_types = {}
    for action_sol in data.get("action_solutions", []):
        action = action_sol["action"]
        code = action["code"]
        # RAI = all-in, but API returns simple_group=RAISE for it
        if code == "RAI":
            action_type = "ALLIN"
        else:
            action_type = action["simple_group"].upper()
        action_types[code] = action_type
    return action_types
