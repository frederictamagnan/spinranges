#!/usr/bin/env python3
"""Main script to fetch all spots for multiple stack depths."""

import sys
from src import fetch_tree, regenerate_html

# Stack depths to fetch
STACK_DEPTHS = [25, 20, 15, 10]

# Game modes
GAME_MODES = {
    "3way": {
        "gametype": "SpinsGeneralV2",
        "stacks_format": "{depth}-{depth}-{depth}",
        "folder": "{depth}bb",
    },
    "hu": {
        "gametype": "HuSngGeneral_V3",
        "stacks_format": "",  # HU doesn't use stacks param
        "folder": "hu_{depth}bb",
    },
}


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python fetch.py <TOKEN> [delay]       - Fetch all spots (3-way + HU)")
        print("  python fetch.py <TOKEN> 3way [delay]  - Fetch 3-way spots only")
        print("  python fetch.py <TOKEN> hu [delay]    - Fetch HU spots only")
        print("  python fetch.py --regenerate          - Regenerate HTML from JSON")
        print("")
        print("Arguments:")
        print("  TOKEN  - API token")
        print("  delay  - Delay between requests in seconds (default: 0.3)")
        print("")
        print(f"Stack depths: {STACK_DEPTHS}")
        sys.exit(1)

    if sys.argv[1] == "--regenerate":
        print("Regenerating HTML files...")
        print("=" * 40)
        for mode in GAME_MODES:
            for depth in STACK_DEPTHS:
                folder = GAME_MODES[mode]["folder"].format(depth=depth)
                path = f"web/spots/{folder}"
                print(f"\n=== {folder} ===")
                regenerate_html(path)
        print("\nDone!")
        return

    token = sys.argv[1]

    # Parse mode and delay
    modes_to_fetch = list(GAME_MODES.keys())  # Default: fetch all
    delay = 0.3

    if len(sys.argv) > 2:
        if sys.argv[2] in GAME_MODES:
            modes_to_fetch = [sys.argv[2]]
            delay = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
        else:
            delay = float(sys.argv[2])

    print("Poker Spins Tree Fetcher")
    print("=" * 40)
    print(f"Modes: {modes_to_fetch}")
    print(f"Stack depths: {STACK_DEPTHS}")
    print(f"Delay: {delay}s between requests")

    total = 0
    for mode in modes_to_fetch:
        mode_config = GAME_MODES[mode]

        for depth in STACK_DEPTHS:
            print(f"\n{'=' * 40}")
            print(f"=== Fetching {mode.upper()} {depth}bb ===")
            print(f"{'=' * 40}")

            stacks = mode_config["stacks_format"].format(depth=depth)
            folder = mode_config["folder"].format(depth=depth)
            output_dir = f"web/spots/{folder}"

            mapping = fetch_tree(
                token,
                output_dir=output_dir,
                delay=delay,
                gametype=mode_config["gametype"],
                depth=depth,
                stacks=stacks
            )
            total += len(mapping)

    print("")
    print("=" * 40)
    print(f"Total spots fetched: {total}")
    print("")
    print("Done! The web/ folder is now ready to share.")
    print("Run 'python export.py' to create a zip file.")


if __name__ == "__main__":
    main()
