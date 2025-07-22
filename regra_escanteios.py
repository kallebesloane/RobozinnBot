import requests
import os
from get_escanteios import get_escanteios

API_KEY = os.getenv("API_FOOTBALL_KEY")

def verificar_escanteios(jogos):
    mensagens = []

    for jogo in jogos:
        fixture = jogo.get("fixture", {})
        teams = jogo.get("teams", {})
        goals = jogo.get("goals", {})
        league = jogo.get("league", {})
        status = fixture.get("status", {})

        minutos = status.get("elapsed")
        if minutos is None:
            minutos = 0  # Corrigido aqui

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
        liga = league.get("name", "Liga Desconhecida")

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
