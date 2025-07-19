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
        fixture = jogo.get("fixture", {})
        teams = jogo.get("teams", {})
        goals = jogo.get("goals", {})
        status = fixture.get("status", {})
        minutos = status.get("elapsed", 0)

        if minutos < 80:
            continue

        home = teams.get("home", {})
        away = teams.get("away", {})
        home_time = home.get("name", "Time da Casa")
        away_time = away.get("name", "Visitante")

        home_gols = goals.get("home", 0)
        away_gols = goals.get("away", 0)

        if home_gols >= away_gols:
            continue

        fixture_id = fixture.get("id")
        liga = fixture.get("league", {}).get("name", "Liga Desconhecida")

        if not fixture_id:
            continue

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
