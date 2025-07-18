import requests
import os

API_KEY = os.getenv("API_FOOTBALL_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

def pegar_escanteios_recent_games(team_id):
    url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&last=5"
    response = requests.get(url, headers=HEADERS)
    jogos = response.json().get("response", [])

    total_escanteios = 0
    jogos_validos = 0

    for jogo in jogos:
        stats_url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={jogo['fixture']['id']}"
        stats_res = requests.get(stats_url, headers=HEADERS)
        stats = stats_res.json().get("response", [])

        for team_stats in stats:
            for stat in team_stats.get("statistics", []):
                if stat["type"] == "Total Corners":
                    total_escanteios += stat["value"] or 0
                    jogos_validos += 1

    media_escanteios = total_escanteios / jogos_validos if jogos_validos else 0
    return media_escanteios

def calcular_probabilidade_escanteios(id_time_casa, id_time_fora):
    try:
        media_casa = pegar_escanteios_recent_games(id_time_casa)
        media_fora = pegar_escanteios_recent_games(id_time_fora)

        media_total = media_casa + media_fora

        # Fórmula base: Se média total >= 10 → 80% chance, se <= 4 → 30%
        if media_total >= 11:
            chance = 90
        elif media_total >= 9:
            chance = 75
        elif media_total >= 7:
            chance = 60
        elif media_total >= 5:
            chance = 45
        else:
            chance = 30

        return f"📈 Probabilidade de escanteios após 80min: {chance}%\n(Média últimas 5 partidas: {media_total:.1f})"
    except Exception as e:
        return f"⚠️ Erro ao calcular probabilidade: {e}"
