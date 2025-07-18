# probabilidade_escanteios.py
import requests
import os

API_KEY = os.getenv("API_FOOTBALL_KEY")

def obter_ultimos_jogos(team_id, quantidade=5):
    url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&last={quantidade}"
    headers = {"x-apisports-key": API_KEY}
    res = requests.get(url, headers=headers)
    return res.json().get("response", [])

def calcular_media_escanteios(jogos):
    total_escanteios = 0
    jogos_validos = 0

    for jogo in jogos:
        fixture_id = jogo['fixture']['id']
        url_stats = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"
        headers = {"x-apisports-key": API_KEY}
        res = requests.get(url_stats, headers=headers)
        dados = res.json().get("response", [])

        if not dados:
            continue  # pula jogos sem estatísticas

        escanteios = 0
        for time_stats in dados:
            for stat in time_stats.get("statistics", []):
                if stat["type"] == "Total Corners":
                    if isinstance(stat["value"], int):
                        escanteios += stat["value"]

        if escanteios > 0:
            total_escanteios += escanteios
            jogos_validos += 1

    if jogos_validos == 0:
        return 0.0

    return total_escanteios / jogos_validos

def calcular_probabilidade_escanteios(team_home_id, team_away_id):
    jogos_casa = obter_ultimos_jogos(team_home_id)
    jogos_fora = obter_ultimos_jogos(team_away_id)

    media_casa = calcular_media_escanteios(jogos_casa)
    media_fora = calcular_media_escanteios(jogos_fora)

    media_total = (media_casa + media_fora) / 2

    # Simples escala: mais escanteios = mais chance de ter escanteio no fim
    if media_total >= 10:
        chance = "🔵 Alta (70%)"
    elif media_total >= 8:
        chance = "🟡 Moderada (50%)"
    elif media_total >= 6:
        chance = "🟠 Baixa (30%)"
    else:
        chance = "🔴 Muito Baixa (10%)"

    return (
        f"📈 Probabilidade de escanteios após 80min: {chance}\n"
        f"(Média últimas 5 partidas: {media_total:.1f})"
    )
