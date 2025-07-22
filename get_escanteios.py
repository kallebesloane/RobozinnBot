import requests
import os

API_KEY = os.getenv("API_FOOTBALL_KEY")

def get_escanteios(fixture_id):
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics?fixture={fixture_id}"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json().get("response", [])

        if not data:
            print(f"[!] Nenhuma estatística para o jogo {fixture_id}")
            return None

        escanteios_total = 0

        for time_stats in data:
            statistics = time_stats.get("statistics", [])
            for stat in statistics:
                if stat.get("type") == "Corners" and stat.get("value") is not None:
                    escanteios_total += int(stat.get("value"))

        return escanteios_total

    except Exception as e:
        print(f"[ERRO AO BUSCAR ESCANTEIOS] {e}")
        return None
