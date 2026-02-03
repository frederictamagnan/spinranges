"""Recursive tree fetcher - discovers all spots from action_solutions."""

import json
import time
from pathlib import Path

from .client import GTOWizardClient
from .html_generator import generate_matrix_html


def regenerate_html(spots_dir: str = "web/spots"):
    """Regenerate all HTML files from existing JSON files."""
    spots_path = Path(spots_dir)

    if not spots_path.exists():
        print(f"ERROR: Directory not found: {spots_dir}")
        return 0

    json_files = list(spots_path.glob("*.json"))
    if not json_files:
        print(f"No JSON files found in {spots_dir}")
        return 0

    count = 0
    for json_file in json_files:
        # Skip metadata files
        if json_file.name in ("spot_mapping.json", "action_tree.json"):
            continue

        print(f"Regenerating {json_file.stem}...")
        with open(json_file) as f:
            data = json.load(f)

        html_file = spots_path / f"{json_file.stem}.html"
        generate_matrix_html(data, str(html_file))
        count += 1

    print(f"Regenerated {count} HTML files")
    return count


def generate_spot_name(action_history: list, next_pos: str) -> str:
    """
    Generate spot name: BTN_R2--SB_F--BB_toact

    Examples:
        [] -> "BTN_toact"
        [("BTN", "R2")] -> "BTN_R2--SB_toact"
        [("BTN", "R2"), ("SB", "F")] -> "BTN_R2--SB_F--BB_toact"
    """
    if not action_history:
        return f"{next_pos}_toact"

    parts = []
    for pos, code in action_history:
        safe_code = code.replace(".", "_")
        parts.append(f"{pos}_{safe_code}")

    parts.append(f"{next_pos}_toact")
    return "--".join(parts)


def fetch_tree(
    token: str,
    output_dir: str = "web/spots",
    delay: float = 0.5,
    gametype: str = "SpinsGeneralV2",
    depth: int = 25,
    stacks: str = "25-25-25"
) -> dict:
    """
    Recursively fetch all preflop spots by following action_solutions.

    Args:
        token: GTO Wizard API token
        output_dir: Output directory for JSON/HTML files
        delay: Delay between requests (rate limiting)
        gametype: Game type (default: SpinsGeneralV2)
        depth: Stack depth in BB
        stacks: Stack sizes

    Returns:
        Mapping of action codes to spot filenames
    """
    client = GTOWizardClient(token)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    visited = set()
    # Queue: (api_actions_str, action_history_list)
    queue = [("", [])]
    spot_mapping = {}
    action_tree = {}

    while queue:
        preflop_actions, action_history = queue.pop(0)

        if preflop_actions in visited:
            continue
        visited.add(preflop_actions)

        try:
            data = client.get_spot(
                gametype=gametype,
                depth=depth,
                stacks=stacks,
                preflop_actions=preflop_actions,
            )

            active_pos = data["game"]["active_position"]
            spot_name = generate_spot_name(action_history, active_pos)

            print(f"\n=== Fetching: {spot_name} ===")
            print(f"    API actions: {preflop_actions or '(open)'}")

            # Save JSON
            json_file = output_path / f"{spot_name}.json"
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"    JSON: {json_file}")

            # Generate HTML
            html_file = output_path / f"{spot_name}.html"
            generate_matrix_html(data, str(html_file))
            print(f"    HTML: {html_file}")

            spot_mapping[preflop_actions] = spot_name

            # Build action tree entry for this spot
            spot_actions = []
            for action_sol in data.get("action_solutions", []):
                action = action_sol["action"]
                spot_actions.append({
                    "code": action["code"],
                    "type": action["simple_group"].upper(),
                    "label": action["display_name"],
                    "is_hand_end": action["is_hand_end"],
                })

            action_tree[preflop_actions] = {
                "position": active_pos,
                "spot_name": spot_name,
                "actions": spot_actions,
            }

            # Discover next spots
            for action_sol in data.get("action_solutions", []):
                action = action_sol["action"]
                code = action["code"]
                is_hand_end = action["is_hand_end"]
                next_pos = action.get("next_position")
                action_type = action["simple_group"].upper()

                next_api_actions = f"{preflop_actions}-{code}" if preflop_actions else code
                next_history = action_history + [(active_pos, code)]

                if is_hand_end:
                    print(f"    {code} ({action_type}) -> hand ends")
                    continue

                if next_api_actions in visited:
                    print(f"    {code} ({action_type}) -> already visited")
                    continue

                next_name = generate_spot_name(next_history, next_pos)
                print(f"    {code} ({action_type}) -> {next_name}")
                queue.append((next_api_actions, next_history))

            time.sleep(delay)

        except Exception as e:
            print(f"    ERROR: {e}")

    # Save mapping
    mapping_file = output_path / "spot_mapping.json"
    with open(mapping_file, 'w') as f:
        json.dump(spot_mapping, f, indent=2)
    print(f"\n=== Mapping saved: {mapping_file} ===")

    # Save action tree as JSON
    tree_file = output_path / "action_tree.json"
    with open(tree_file, 'w') as f:
        json.dump(action_tree, f, indent=2)
    print(f"=== Action tree saved: {tree_file} ===")

    # Also save as JS file for static hosting (no fetch needed)
    # Extract depth and mode from output_dir (e.g., "web/spots/25bb" or "web/spots/hu_25bb")
    folder_name = output_path.name
    is_hu = folder_name.startswith("hu_")

    if is_hu:
        depth_str = folder_name.replace("hu_", "").replace("bb", "")
        js_filename = f"action_tree_hu_{depth_str}bb.js"
        var_name = f"ACTION_TREE_HU_{depth_str}BB"
    else:
        depth_str = folder_name.replace("bb", "")
        js_filename = f"action_tree_{depth_str}bb.js"
        var_name = f"ACTION_TREE_{depth_str}BB"

    js_dir = output_path.parents[1] / "js"
    js_dir.mkdir(exist_ok=True)
    js_file = js_dir / js_filename
    with open(js_file, 'w') as f:
        f.write(f"// Auto-generated action tree for {folder_name}\n")
        f.write(f"const {var_name} = ")
        json.dump(action_tree, f, indent=2)
        f.write(";\n")
    print(f"=== Action tree JS saved: {js_file} ===")

    return spot_mapping
