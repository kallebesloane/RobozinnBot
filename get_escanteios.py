import requests
import os

API_KEY = os.getenv("API_FOOTBALL_KEY")

def get_escanteios_total(fixture_id):
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics?fixture={fixture_id}"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json().get("response", [])

        if not data or len(data) < 2:
            return None

        total = 0
        for time_stats in data:
            for stat in time_stats.get("statistics", []):
                if stat["type"] == "Corners" and stat["value"] is not None:
                    total += stat["value"]

        return total

    except Exception as e:
        print(f"[ERRO NO get_escanteios_total] {e}")
        return None
