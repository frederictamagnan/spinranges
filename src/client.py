"""GTO Wizard API client."""

import requests


class GTOWizardClient:
    """Client for GTO Wizard API."""

    BASE_URL = "https://api.gtowizard.com/v4/solutions/spot-solution/"

    def __init__(self, token: str, client_id: str = None):
        self.token = token
        self.client_id = client_id or "gto-parser"
        self.session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "gwclientid": self.client_id,
            "origin": "https://app.gtowizard.com",
            "referer": "https://app.gtowizard.com/",
        })

    def get_spot(
        self,
        gametype: str = "SpinsGeneralV2",
        depth: int = 25,
        stacks: str = "25-25-25",
        preflop_actions: str = "",
        board: str = ""
    ) -> dict:
        """Fetch spot data from API."""
        params = {
            "gametype": gametype,
            "depth": depth,
            "stacks": stacks,
            "preflop_actions": preflop_actions,
            "flop_actions": "",
            "turn_actions": "",
            "river_actions": "",
            "board": board,
        }
        resp = self.session.get(self.BASE_URL, params=params)
        resp.raise_for_status()
        return resp.json()
