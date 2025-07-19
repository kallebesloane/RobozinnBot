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

        if not data or len(data) < 2:
            return None

        escanteios_total = 0

        for time_stats in data:
            for stat in time_stats["statistics"]:
                if stat["type"] == "Corners" and stat["value"] is not None:
                    escanteios_total += stat["value"]

        return escanteios_total

    except Exception as e:
        print(f"[ERRO AO BUSCAR ESCANTEIOS] {e}")
        return None


def verificar_escanteios(jogos):
    mensagens = []

    for jogo in jogos:
        fixture = jogo["fixture"]
        teams = jogo["teams"]
        goals = jogo["goals"]
        status = fixture["status"]
        minutos = status["elapsed"] or 0

        if minutos < 80:
            continue

        home_time = teams["home"]["name"]
        away_time = teams["away"]["name"]
        home_gols = goals["home"]
        away_gols = goals["away"]

        if home_gols >= away_gols:
            continue

        fixture_id = fixture["id"]
        liga = fixture["league"]["name"]

        escanteios = get_escanteios(fixture_id)

        if escanteios is None:
            continue

        mensagem = (
            "🟥 *ESCANTEIOS*\n"
            f"🏟️ Liga: {liga}\n"
            f"⏱ {minutos}min — {home_time} perdendo pra {away_time}\n"
            f"🔢 Placar: {home_gols} x {away_gols}\n"
            f"🚩 Número de escanteios totais: *{escanteios}*"
        )

        mensagens.append(mensagem)

    return mensagens
