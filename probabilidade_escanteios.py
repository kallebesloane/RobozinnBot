import requests
import os

API_KEY = os.getenv("API_FOOTBALL_KEY") or "SUA_CHAVE_AQUI"

def obter_ultimos_jogos(team_id, quantidade=5):
    url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&last={quantidade}"
    headers = {"x-apisports-key": API_KEY}
    res = requests.get(url, headers=headers)
    data = res.json()
    
    if data.get("response") is None:
        print(f"[ERRO] Não conseguiu buscar jogos para o time {team_id}")
        return []

    return data["response"]

def calcular_media_escanteios(jogos):
    total_escanteios = 0
    jogos_validos = 0

    for jogo in jogos:
        fixture_id = jogo['fixture']['id']
        url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"
        headers = {"x-apisports-key": API_KEY}
        res = requests.get(url, headers=headers)
        stats = res.json().get("response", [])

        if not stats:
            print(f"[AVISO] Estatísticas não disponíveis para jogo {fixture_id}")
            continue

        escanteios = 0
        for time_stats in stats:
            for stat in time_stats.get("statistics", []):
                if stat["type"] == "Total Corners" and isinstance(stat["value"], int):
                    escanteios += stat["value"]

        print(f"[INFO] Jogo {fixture_id}: {escanteios} escanteios")

        if escanteios > 0:
            total_escanteios += escanteios
            jogos_validos += 1

    if jogos_validos == 0:
        return 0.0

    media = total_escanteios / jogos_validos
    print(f"[RESULTADO] Média de escanteios: {media:.2f}")
    return media

def calcular_probabilidade_escanteios(team_home_id, team_away_id):
    print(f"[DEBUG] Calculando escanteios para times: {team_home_id} vs {team_away_id}")

    jogos_casa = obter_ultimos_jogos(team_home_id)
    jogos_fora = obter_ultimos_jogos(team_away_id)

    media_casa = calcular_media_escanteios(jogos_casa)
    media_fora = calcular_media_escanteios(jogos_fora)

    media_total = (media_casa + media_fora) / 2

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
