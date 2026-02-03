"""HTML matrix generator for GTO Wizard data."""

from .parser import RANKS, get_hand_frequencies, get_action_types

# Action colors
COLORS = {
    "FOLD": "#3F89A6",
    "RAISE": "#F25260",
    "CALL": "#2ecc71",
    "CHECK": "#2ecc71",
    "ALLIN": "#6B0F0F",
}

# Action display order for gradients
ACTION_ORDER = ["ALLIN", "RAISE", "CALL", "CHECK", "FOLD"]


def generate_matrix_html(data: dict, output_file: str = None) -> str:
    """Generate HTML matrix with colors from spot data."""

    action_types = get_action_types(data)
    hand_freqs = get_hand_frequencies(data)

    game = data.get("game", {})
    position = game.get("active_position", "?")
    pot = game.get("pot", "?")

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>GTO Wizard - {position}</title>
    <style>
        :root {{
            --color-fold: #3F89A6;
            --color-call: #2ecc71;
            --color-raise: #F25260;
            --color-allin: #6B0F0F;
            --color-bg: #1a1a2e;
            --color-bg-light: #2a2a4e;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--color-bg);
            color: white;
            padding: 15px;
        }}
        .info {{
            margin-bottom: 15px;
            color: #aaa;
            font-size: 14px;
        }}
        table {{ border-collapse: collapse; }}
        td, th {{
            width: 52px;
            height: 40px;
            text-align: center;
            font-size: 11px;
            border: 1px solid #333;
            font-family: monospace;
        }}
        th {{
            background: var(--color-bg-light);
            font-weight: 600;
        }}
        td {{ color: white; }}
        .legend {{
            margin-top: 15px;
            display: flex;
            gap: 8px;
        }}
        .legend span {{
            padding: 5px 12px;
            border-radius: 4px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="info">Position: {position} | Pot: {pot}</div>
    <table>
        <tr><th></th>"""

    for r in RANKS:
        html += f"<th>{r}</th>"
    html += "</tr>\n"

    for i, r1 in enumerate(RANKS):
        html += f"        <tr><th>{r1}</th>"
        for j, r2 in enumerate(RANKS):
            # Build hand name from matrix position
            if i == j:
                hand = f"{r1}{r1}"
            elif i < j:
                hand = f"{r1}{r2}s"
            else:
                hand = f"{r2}{r1}o"

            # Get frequencies from simple_hand_counters
            hand_info = hand_freqs.get(hand, {})
            action_freqs = hand_info.get("actions_total_frequencies", {})

            # Convert action codes to types
            freqs = {}
            for code, freq in action_freqs.items():
                action_type = action_types.get(code, code)
                if freq > 0:
                    freqs[action_type] = freqs.get(action_type, 0) + freq

            # Determine cell style
            if not freqs:
                # Hand not in range at this spot (filtered out by previous actions)
                bg_style = "background:#222"
                text = ""
                html += f'<td style="{bg_style};color:#444" title="{hand}: not in range">{hand}</td>'
                continue
            elif len(freqs) == 1:
                action_type = list(freqs.keys())[0]
                bg_style = f"background:{COLORS.get(action_type, '#666')}"
                text = f"{list(freqs.values())[0]*100:.0f}"
            else:
                # Mixed - create gradient
                sorted_freqs = sorted(
                    freqs.items(),
                    key=lambda x: ACTION_ORDER.index(x[0]) if x[0] in ACTION_ORDER else 99
                )
                gradient_parts = []
                current_pos = 0
                for action_type, freq in sorted_freqs:
                    color = COLORS.get(action_type, "#666")
                    end_pos = current_pos + freq * 100
                    gradient_parts.append(f"{color} {current_pos:.0f}% {end_pos:.0f}%")
                    current_pos = end_pos
                bg_style = f"background:linear-gradient(to right,{','.join(gradient_parts)})"
                best = max(freqs.items(), key=lambda x: x[1])
                text = f"{best[1]*100:.0f}"

            html += f'<td style="{bg_style}" title="{hand}: {text}%">{hand}<br>{text}</td>'
        html += "</tr>\n"

    # Dynamic legend based on available actions
    available_actions = set(action_types.values())
    legend_items = []
    for action in ACTION_ORDER:
        if action in available_actions:
            color_var = f"var(--color-{action.lower()})"
            legend_items.append(f'<span style="background:{color_var}">{action}</span>')

    html += f"""    </table>
    <div class="legend">
        {"".join(legend_items)}
    </div>
</body>
</html>"""

    if output_file:
        with open(output_file, 'w') as f:
            f.write(html)

    return html
